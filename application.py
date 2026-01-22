"""
This script runs the FlaskWebProject application using a development server.
"""

from os import environ
from FlaskWebProject import app
from config import Config

    
# print("SQL_SERVER:", Config.SQL_SERVER)
# print("SQL_DATABASE:", Config.SQL_DATABASE)
# print("SQL_USER_NAME:", Config.SQL_USER_NAME)
# print("SQL_PASSWORD:", Config.SQL_PASSWORD)


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    # app.run(HOST, PORT, ssl_context='adhoc')

    app.run(HOST, PORT, debug=True)

