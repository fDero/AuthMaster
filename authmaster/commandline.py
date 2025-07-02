from argparse import *

def setup_port_cli_flag(parser: ArgumentParser):
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

def setup_cli_parser_startup():
    parser = ArgumentParser()
    setup_debug_cli_flag(parser)
    setup_port_cli_flag(parser)
    return parser