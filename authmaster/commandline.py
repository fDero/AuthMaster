from argparse import *

def setup_port_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "-p", "--port",
        type=int,
        choices=[80, 443, 8080, 5000],
        default=5000,
        help="Port to run the server on (default: 8080)"
    )

def setup_debug_cli_flag(parser: ArgumentParser):
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        default=False,
        help="Enable debug mode"
    )

def setup_mongodb_connection_string_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--mongodb-connection-string",
        type=str,
        default="mongodb://localhost:27017",
        help="MongoDB connection string (default: mongodb://localhost:27017)"
    )

def setup_mongodb_database_name_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--mongodb-database-name",
        type=str,
        default="authmaster",
        help="MongoDB database name (default: authmaster)"
    )

def setup_mongodb_collection_name_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--mongodb-collection-name",
        type=str,
        default="users",
        help="MongoDB collection name (default: users)"
    )

def setup_cli_parser_startup():
    parser = ArgumentParser()
    setup_debug_cli_flag(parser)
    setup_port_cli_param(parser)
    setup_mongodb_connection_string_cli_param(parser)
    setup_mongodb_database_name_cli_param(parser)
    setup_mongodb_collection_name_cli_param(parser)
    return parser