import os
import urllib

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ENTER-YOUR-SECRET-KEY'

    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or 'ENTER-YOUR-BLOB-ACCOUNT-NAME'
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or 'ENTER-YOUR-BLOB-STORAGE-KEY'
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or 'ENTER-YOUR-BLOB-CONTAINER-NAME'
    BLOB_CONNECTION_STRING = os.environ.get('BLOB_CONNECTION_STRING') or 'ENTER-YOUR-BLOB-CONNECTION-STRING'
    # Azure SQL Database
    SQL_SERVER = os.environ.get('SQL_SERVER') or 'ENTER-SQL-SERVER-NAME'
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or 'ENTER-DATABASE-NAME'
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or 'ENTER-SQL-USERNAME'
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or 'ENTER-SQL-PASSWORD'

    params = urllib.parse.quote_plus(
        f"Driver=ODBC Driver 18 for SQL Server;"
        f"Server=tcp:{SQL_SERVER},1433;"
        f"Database={SQL_DATABASE};"
        f"Uid={SQL_USER_NAME};"
        f"Pwd={SQL_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLAlchemy Engine Options (prevents dropped connections)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,      # Tests connection before using it
        "pool_recycle": 1800,       # Recycle connections every 30 minutes
        "pool_timeout": 30,         # Wait time before giving up on a connection
        "pool_size": 10,            # Number of persistent connections
        "max_overflow": 20          # Extra connections allowed during spikes
    }

    ### Info for MS Authentication ###
    ### As adapted from: https://github.com/Azure-Samples/ms-identity-python-webapp ###
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET') or 'ENTER-CLIENT-SECRET'
    # In your production app, Microsoft recommends you to use other ways to store your secret,
    # such as KeyVault, or environment variable as described in Flask's documentation here:
    # https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    # if not CLIENT_SECRET:
    #     raise ValueError("Need to define CLIENT_SECRET environment variable")

    CLIENT_ID = os.environ.get('CLIENT_ID') or 'ENTER-CLIENT-ID'

    AUTHORITY = f"https://login.microsoftonline.com/{CLIENT_ID}"  # For multi-tenant app, else put tenant name
    # AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

    REDIRECT_PATH = "/getAToken"  # Used to form an absolute URL; must match to app's redirect_uri set in AAD

    LOGOUT_URL = "/login"

    # You can find the proper permission names from this document
    # https://docs.microsoft.com/en-us/graph/permissions-reference
    SCOPE = ["User.Read"] # Only need to read user profile for this app

    SESSION_TYPE = "filesystem"  # Token cache will be stored in server-side session