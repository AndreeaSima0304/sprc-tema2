from flask import Flask
from countries import countries
from cities import cities
from temperatures import temperatures

db_name = 'SPRC'
db_user = 'postgres'
db_pass = 'postgres123'
db_host = 'postgresql'
db_port = '5432'

server = Flask(__name__)

server.register_blueprint(countries)
server.register_blueprint(cities)
server.register_blueprint(temperatures)


if __name__ == '__main__':
    server.run('0.0.0.0', debug=False)
