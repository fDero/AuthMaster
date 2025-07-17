from argparse import *
from commons import *


def setup_port_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "-p", "--port",
        type=int,
        choices=[80, 443, 8080, 5000],
        default=5000,
        help="Port to run the server on (default: 8080)"
    )


def setup_db_owner_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--db-owner",
        type=str,
        default="authmaster",
        help="Database owner name (default: authmaster)"
    )


def setup_smtp_server_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--smtp-server",
        type=str,
        default="smtp.gmail.com",
        help="SMTP server address (default: smtp.gmail.com)"
    )


def setup_smtp_port_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--smtp-port",
        type=int,
        choices=[587, 465],
        default=587,
        help="SMTP server port (default: 587)"
    )


def setup_smtp_email_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--smtp-email",
        type=str,
        required=True,
        help="Email address to use for sending emails"
    )


def setup_smtp_creds_cli_param(parser: ArgumentParser):
    parser.add_argument(
        "--smtp-passw",
        type=str,
        required=True,
        help="Credentials for the SMTP server (e.g., password or app password)"
    )



def setup_smtp_info(args) -> dict:
    return {
        "server": args.smtp_server,
        "port": args.smtp_port,
        "email": args.smtp_email,
        "creds": args.smtp_passw
    }


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


def setup_jwt_secret_cli_param(parser: ArgumentParser):
    default_jwt_secret = get_random_string(32)
    parser.add_argument(
        "--jwt-secret",
        type=str,
        default=default_jwt_secret,
        help="Secret key for JWT token generation (default: randomly generated)"
    )

def setup_cli_parser_startup():
    parser = ArgumentParser()
    setup_debug_cli_flag(parser)
    setup_port_cli_param(parser)

    setup_mongodb_connection_string_cli_param(parser)
    setup_mongodb_database_name_cli_param(parser)
    setup_mongodb_collection_name_cli_param(parser)
    
    setup_smtp_creds_cli_param(parser)
    setup_smtp_email_cli_param(parser)
    setup_smtp_server_cli_param(parser)
    setup_smtp_port_cli_param(parser)
    setup_jwt_secret_cli_param(parser)

    setup_db_owner_cli_param(parser)
    return parser