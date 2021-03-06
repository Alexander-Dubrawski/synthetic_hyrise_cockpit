"""Tool for executing wrk benchmark."""
import signal
from calendar import timegm
from datetime import datetime
from json import dumps
from multiprocessing import Manager, Process
from os import mkdir
from subprocess import check_output
from time import gmtime

from benchmark_tools.settings import BACKEND_HOST, BACKEND_PORT

from .system_benchmark import format_data, fromat_avg_data, monitor_system, write_to_csv
from .wrk_benchmark_helper import (
    add_database,
    format_results,
    print_user_results,
    remove_database,
    start_manager,
    start_workers,
    start_workload,
    start_workload_generator,
    start_wsgi_server,
    stop_workers,
    stop_workload,
    stop_wsgi_server,
)

NUMBER_CLIENTS = 1
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"
DURATION_IN_MINUTES = 60
NUMBER_DATABASES = [1, 10, 20, 40]
ENDPOINT = "manager_metric"


def create_folder(name):
    """Create folder to save benchmark results."""
    ts = timegm(gmtime())
    path = f"measurements/{name}_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    return path


def wrk_background_process(url, endpoint, shared_data):
    """Background process to execute wrk."""
    shared_data[endpoint] = check_output(
        f"numactl -m 0 --physcpubind 20-79 wrk -t{NUMBER_CLIENTS} -c{NUMBER_CLIENTS} -s ./benchmark_tools/report.lua -d{DURATION_IN_MINUTES}m --timeout 20s {url}",
        shell=True,
    ).decode("utf-8")


def create_wrk_processes(shared_data, number_client):
    """Create one wrk process per endpoint."""
    return Process(
        target=wrk_background_process,
        args=(f"{BACKEND_URL}/{ENDPOINT}", ENDPOINT, shared_data),
    )


def execute_in_user_context(number_database):
    manager = Manager()
    results = {}
    shard_dict = manager.dict()
    for i in range(number_database):
        add_database(str(i))
    start_workload()
    start_workers()
    process = create_wrk_processes(shard_dict, 8)
    process.start()
    monitor_system_data = monitor_system(DURATION_IN_MINUTES * 60)
    process.join()
    process.terminate()
    stop_workers()
    stop_workload()
    for i in range(number_database):
        remove_database(str(i))
    for key, value in shard_dict.items():
        results[key] = value
    return (results, monitor_system_data)


def run_user_benchmark(number_databases, path):
    results = {}
    system_data = {}
    for number_database in number_databases:
        print(f"Execute benchmark with {number_database} databases")
        parallel_results, monitor_system_data = execute_in_user_context(number_database)
        results[number_database] = parallel_results
        system_data[number_database] = monitor_system_data
        write_to_csv(system_data, path, [number_database])
        with open(f"{path}/{number_database}_results.txt", "+w") as file:
            file.write(dumps(parallel_results))
        with open(
            f"{path}/{number_database}_formatted_system_results.txt", "+w"
        ) as file:
            file.write(
                dumps(
                    fromat_avg_data(
                        [number_database], format_data(system_data, [number_database])
                    )
                )
            )
    return (results, system_data)


def run_benchmark():
    path = create_folder("user_wrk_benchmark")
    start_wsgi_server(1, 1)
    manager = start_manager()
    generator = start_workload_generator()
    user_results, system_data = run_user_benchmark(NUMBER_DATABASES, path)
    print_user_results(user_results)
    formatted_user_results = format_results(user_results)
    with open(f"{path}/formatted_user_results.txt", "+w") as file:
        file.write(dumps(formatted_user_results))
    stop_wsgi_server()
    manager.send_signal(signal.SIGINT)
    manager.wait()
    generator.send_signal(signal.SIGINT)
    generator.wait()


if __name__ == "__main__":
    run_benchmark()  # type: ignore
