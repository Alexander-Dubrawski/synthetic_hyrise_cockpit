"""Module for managing databases."""

from types import TracebackType
from typing import Callable, Dict, Optional, Tuple, Type

from backend.request import Body
from backend.response import Response, get_response
from backend.server import Server

from .database import Database


class DatabaseManager(object):
    """A manager for database drivers."""

    def __init__(
        self,
        db_manager_listening: str,
        db_manager_port: str,
        workload_sub_host: str,
        workload_pubsub_port: str,
    ) -> None:
        """Initialize a DatabaseManager."""
        self._workload_sub_host = workload_sub_host
        self._workload_pubsub_port = workload_pubsub_port
        self._databases: Dict[str, Database] = {}
        server_calls: Dict[
            str, Tuple[Callable[[Body], Response], Optional[Dict]]
        ] = self._get_server_calls()
        self._server = Server(db_manager_listening, db_manager_port, server_calls)

    def __enter__(self) -> "DatabaseManager":
        """Return self for a context manager."""
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Call close with a context manager."""
        self.close()
        return None

    def _get_server_calls(self,) -> Dict:
        return {
            "add database": self._call_add_database,
            "delete database": self._call_delete_database,
            "start worker": self._call_start_worker,
            "close worker": self._call_close_worker,
            "get databases": self._call_get_databases,
            "status": self._call_status,
            "execute sql query": self._call_execute_sql_query,
        }

    def _call_add_database(self, body: Body) -> Response:
        """Add database and initialize driver for it."""
        if body["id"] in self._databases:
            return get_response(400)

        db_instance = Database(
            body["id"],
            body["host"],
            body["port"],
            body["number_workers"],
            "tcp://{:s}:{:s}".format(
                self._workload_sub_host, self._workload_pubsub_port,
            ),
        )
        self._databases[body["id"]] = db_instance
        return get_response(200)

    def _call_get_databases(self, body: Body) -> Response:
        """Get list of all databases."""
        databases = [
            {
                "id": id,
                "host": database.connection_information["host"],
                "port": database.connection_information["port"],
                "number_workers": database.number_workers,
            }
            for id, database in self._databases.items()
        ]
        response = get_response(200)
        response["body"]["databases"] = databases
        return response

    def _call_delete_database(self, body: Body) -> Response:
        id: str = body["id"]
        database: Optional[Database] = self._databases.pop(id, None)
        if database:
            database.close()
            del database
            return get_response(200)
        else:
            return get_response(404)

    def _call_status(self, body: Body) -> Response:
        status = []

        for database_id, database in self._databases.items():
            status.append(
                {
                    "id": database_id,
                    "worker_pool_status": database.get_worker_pool_status(),
                }
            )
        response = get_response(200)
        response["body"]["status"] = status
        return response

    def _call_start_worker(self, body: Body) -> Response:
        for database in self._databases.values():
            if not database.start_worker():
                return get_response(400)
        return get_response(200)

    def _call_close_worker(self, body: Body) -> Response:
        for database in self._databases.values():
            if not database.close_worker():
                return get_response(400)
        return get_response(200)

    def _call_execute_sql_query(self, body: Body) -> Response:
        database_id: str = body["id"]
        query: str = body["query"]
        if database_id not in self._databases.keys():
            return get_response(404)
        results = self._databases[database_id].execute_sql_query(query)
        response = get_response(200)
        response["body"]["results"] = results
        return response

    def start(self) -> None:
        """Start the manager by starting the server."""
        self._server.start()

    def close(self) -> None:
        """Close the socket and context, exit all databases."""
        for database in self._databases.values():
            database.close()
        self._server.close()
