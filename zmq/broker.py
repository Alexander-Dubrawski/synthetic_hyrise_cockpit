# type: ignore
# flake8: noqa
import time
from multiprocessing import Process
from threading import Thread

import zmq

NUMBER_WORKER = 4
NUMBER_THREADS = 4


def thread_routine(url_thread, thread_id, worker_id):
    """Worker task, using a REQ socket to do load-balancing."""
    context = zmq.Context.instance()
    socket = context.socket(zmq.REQ)
    socket.connect(url_thread)
    # Tell broker we're ready for work
    socket.send(b"READY")

    while True:
        (
            broker_address,
            empty_frame,
            client_address,
            empty_frame,
            client_request,
        ) = socket.recv_multipart()
        socket.send_multipart(
            [
                broker_address,
                b"",
                client_address,
                b"",
                f"w{worker_id} t{thread_id}".encode(),
            ]
        )


def worker(broker_id, worker_id):
    context = zmq.Context.instance()
    broker = context.socket(zmq.ROUTER)
    byte_worker_id = f"WORKER_{worker_id}".encode()
    broker.setsockopt(zmq.IDENTITY, byte_worker_id)
    broker.connect("tcp://127.0.0.1:5007")
    thread = context.socket(zmq.ROUTER)
    thread.bind("inproc://threads")

    threads_obj = []
    for i in range(NUMBER_THREADS):
        t = Thread(target=thread_routine, args=("inproc://threads", i, worker_id))
        t.start()
        threads_obj.append(t)

    poller = zmq.Poller()
    poller.register(thread, zmq.POLLIN)
    threads = []
    broker.send_multipart([broker_id, b"", b"READY"])
    poller.register(broker, zmq.POLLIN)

    while True:
        sockets = dict(poller.poll())

        if thread in sockets:
            # Handle worker activity on the backend
            request = thread.recv_multipart()
            # we need to unpack the last three values. This is the inner envelop
            thread_address, empty_frame, broker_address = request[:3]
            threads.append(thread_address)
            if broker_address != b"READY" and len(request) > 3:
                # If client reply, send rest back to broker
                (
                    thread_address,
                    empty_frame,
                    broker_address,
                    empty_frame,
                    client_address,
                    empty_frame,
                    cleint_reply,
                ) = request
                broker.send_multipart(
                    [broker_address, b"", client_address, b"", cleint_reply]
                )

        if broker in sockets:
            # Get next client request, route to last-used worker
            message = broker.recv_multipart()
            (
                broker_address,
                empty_frame,
                client_address,
                empty_frame,
                client_request,
            ) = message
            thread_address = threads.pop(0)
            if threads:
                broker.send_multipart([broker_id, b"", b"READY"])
            thread.send_multipart(
                [
                    thread_address,
                    b"",
                    broker_address,
                    b"",
                    client_address,
                    b"",
                    client_request,
                ]
            )


def main():
    """Load balancer main loop."""
    # Prepare context and sockets
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://127.0.0.1:5555")
    backend = context.socket(zmq.ROUTER)
    backend.setsockopt(zmq.IDENTITY, b"BROKER")
    backend.bind("tcp://127.0.0.1:5007")

    worker_processes = []
    for i in range(NUMBER_WORKER):
        process = Process(target=worker, args=(b"BROKER", i))
        process.start()

    poller = zmq.Poller()
    poller.register(backend, zmq.POLLIN)
    workers = []

    while True:
        sockets = dict(poller.poll())

        if backend in sockets:
            # Handle worker activity on the backend
            request = backend.recv_multipart()
            # we need to unpack the last three values. This is the inner envelop
            worker_address, empty_frame, client_adress = request[:3]
            if not workers:
                # Poll for clients now that a worker is available
                poller.register(frontend, zmq.POLLIN)
            workers.append(worker_address)
            if client_adress != b"READY" and len(request) > 3:
                # If client reply, send rest back to front end
                empty_frame, cleint_reply = request[3:]
                frontend.send_multipart([client_adress, b"", cleint_reply])

        if frontend in sockets:
            # Get next client request, route to last-used worker
            message = frontend.recv_multipart()
            client_adress, empty_frame, client_request = message
            worker_address = workers.pop(0)
            backend.send_multipart(
                [worker_address, b"", client_adress, b"", client_request]
            )
            if not workers:
                # Don't poll clients if no workers are available
                poller.unregister(frontend)

    # Clean up
    backend.close()
    frontend.close()
    context.term()


if __name__ == "__main__":
    main()
