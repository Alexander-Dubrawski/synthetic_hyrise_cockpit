"""Tool for executing user scenario latency benchmark."""
from calendar import timegm
from csv import writer
from datetime import datetime
from multiprocessing import Manager, Process
from os import mkdir
from statistics import mean, median
from time import gmtime

from benchmark_tools.graph_plotter import (
    plot_avg_med_bar_chart,
    plot_line_chart,
    plot_stacked_bar_chart,
)
from benchmark_tools.latency.curl_wrapper import (
    add_database,
    delete_database,
    execute_get,
    start_worker,
    start_workload,
    stop_worker,
    stop_workload,
)
from benchmark_tools.latency.print_data import print_data

RUNS = 1000
NUMBER_DATABASES = 2

GET_ENDPOINTS = [
    "queue_length",
    "storage",
    "throughput",
    "latency",
]


def print_yellow(value):
    """Print yellow colored text."""
    print("\033[93m{}\033[00m".format(value))


def get_on_endpoints(endpoint):
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    for _ in range(RUNS):
        results = execute_get(endpoint)
        server_process_times.append(results["total"] - results["pretransfer"])
        name_lookup_times.append(results["namelookup"])
        connect_times.append(results["connect"] - results["namelookup"])
    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def benchmark_get_endpoints_sequential():
    benchamrk_results = {}
    for endpoint in GET_ENDPOINTS:
        benchamrk_results[endpoint] = get_on_endpoints(endpoint)
    return benchamrk_results


def get_on_endpoint_parallel(endpoint, shared_data):
    shared_data[endpoint] = get_on_endpoints(endpoint)


def benchmark_get_endpoints_parallel():
    manager = Manager()
    shared_data = manager.dict()
    processes = [
        Process(target=get_on_endpoint_parallel, args=(endpoint, shared_data,))
        for endpoint in GET_ENDPOINTS
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        process.terminate()

    return shared_data


def post_delete_multiple_databases(handler):
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    for i in range(NUMBER_DATABASES):
        results = handler(f"db_{i}")
        server_process_times.append(results["total"] - results["pretransfer"])
        name_lookup_times.append(results["namelookup"])
        connect_times.append(results["connect"] - results["namelookup"])
    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def post_data(handler):
    server_process_times = []
    name_lookup_times = []
    connect_times = []
    results = handler()
    server_process_times.append(results["total"] - results["pretransfer"])
    name_lookup_times.append(results["namelookup"])
    connect_times.append(results["connect"] - results["namelookup"])
    return {
        "server_process_times": server_process_times,
        "name_lookup_times": name_lookup_times,
        "connect_times": connect_times,
    }


def print_results(results, results_sequential, results_parallel):
    for endpoint, result in results.items():
        print_data(endpoint, result)

    print_yellow("\nResults for sequential execution\n")

    for endpoint, result in results_sequential.items():
        print_data(endpoint, result)

    print_yellow("\nResults for parallel execution\n")

    for endpoint, result in results_parallel.items():
        print_data(endpoint, result)


def create_folder():
    ts = timegm(gmtime())
    path = f"measurements/User_scenario_latency_{datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')}"
    mkdir(path)
    mkdir(f"{path}/server_process_times")
    mkdir(f"{path}/name_lookup_times")
    mkdir(f"{path}/connect_times")
    mkdir(f"{path}/stacked")
    return path


def plot_graphs(path, results_sequential, results_parallel):
    latency_types = ["server_process_times", "name_lookup_times", "connect_times"]
    interpolation_factor = 50
    for latency_type in latency_types:
        local_path = f"{path}/{latency_type}"
        plot_line_chart(
            results_sequential,
            local_path,
            f"avg_sequential_latency_{latency_type}",
            latency_type,
            interpolation_factor,
            mean,
            "AVG",
        )
        plot_line_chart(
            results_sequential,
            local_path,
            f"med_sequential_latency_{latency_type}",
            latency_type,
            interpolation_factor,
            median,
            "MED",
        )
        plot_avg_med_bar_chart(
            results_sequential,
            local_path,
            f"sequential_{latency_type}_latency_get_endpoints",
            latency_type,
        )
    for latency_type in latency_types:
        local_path = f"{path}/{latency_type}"
        plot_line_chart(
            results_parallel,
            local_path,
            f"avg_parallel_latency_{latency_type}",
            latency_type,
            interpolation_factor,
            mean,
            "AVG",
        )
        plot_line_chart(
            results_parallel,
            local_path,
            f"med_parallel_latency_{latency_type}",
            latency_type,
            interpolation_factor,
            median,
            "MED",
        )
        plot_avg_med_bar_chart(
            results_parallel,
            local_path,
            f"sequential_{latency_type}_latency_get_endpoints",
            latency_type,
        )
    plot_stacked_bar_chart(
        results_sequential,
        f"{path}/stacked",
        "med_sequential_latency_distribution",
        median,
    )
    plot_stacked_bar_chart(
        results_parallel, f"{path}/stacked", "med_parallel_latency_distribution", median
    )
    plot_stacked_bar_chart(
        results_sequential,
        f"{path}/stacked",
        "avg_sequential_latency_distribution",
        mean,
    )
    plot_stacked_bar_chart(
        results_parallel, f"{path}/stacked", "avg_parallel_latency_distribution", mean
    )


def write_to_csv(data, path, file_name):
    latency_types = ["server_process_times", "name_lookup_times", "connect_times"]
    for latency_type in latency_types:
        with open(
            f"{path}/{latency_type}/{file_name}_{latency_type}.csv", "w", newline=""
        ) as f:
            endpoints = list(data.keys())
            filednames = list(data.keys())
            filednames.insert(0, "run")
            csv_writer = writer(f, delimiter="|")
            csv_writer.writerow(filednames)
            rows = []
            for i in range(RUNS):
                row = []
                row.append(i)
                for endpoint in endpoints:
                    row.append(data[endpoint][latency_type][i])
                rows.append(row)
            csv_writer.writerows(rows)


def run_benchmark():

    results = {}
    results["POST database"] = post_delete_multiple_databases(add_database)
    results["POST workload"] = post_data(start_workload)
    results["POST worker"] = post_data(start_worker)
    results_sequential = benchmark_get_endpoints_sequential()
    results_parallel = benchmark_get_endpoints_parallel()
    results["DELETE worker"] = post_data(stop_worker)
    results["DELETE workload"] = post_data(stop_workload)
    results["DELETE database"] = post_delete_multiple_databases(delete_database)

    print_results(results, results_sequential, results_parallel)

    path = create_folder()
    plot_graphs(path, results_sequential, results_parallel)
    write_to_csv(results_sequential, path, "sequential")
    write_to_csv(results_sequential, path, "parallel")


if __name__ == "__main__":
    run_benchmark()  # type: ignore
