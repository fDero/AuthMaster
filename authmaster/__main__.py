from __init__ import app
from endpoints import *
from commandline import *
from error_handling import *
from persistence import *


if __name__ == '__main__':
    parser = setup_cli_parser_startup()
    args = parser.parse_args()

    app.config['MONGODB'] = mongodb_connection_setup(args)
    app.config['SMTP'] = setup_smtp_info(args)
    app.config['OWNER'] = args.db_owner
    app.config['JWT_SECRET'] = args.jwt_secret

    app.run(
        debug=args.debug, 
        port=args.port, 
        host='0.0.0.0'
    )
