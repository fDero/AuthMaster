from __init__ import app
from endpoints import *
from commandline import *
from error_handling import *
from persistence import *

if __name__ == '__main__':
    parser = setup_cli_parser_startup()
    args = parser.parse_args()

    MONGODB_CONNECTION_STRING = args.mongodb_connection_string
    MONGODB_COLLECTION_NAME = args.mongodb_collection_name
    MONGODB_DATABASE_NAME = args.mongodb_database_name
    AUTHMASTER_OWNER = "authmaster"
    
    app.run(
        debug=args.debug, 
        port=args.port, 
        host='0.0.0.0'
    )
