from flask import Flask
from flask_cors import CORS

from Server.Controller.EmployeeController import EmployeeController
from Server.Controller.LoginController import init_login_controller
from Server.Controller.ClientController import ClientController

app = Flask(__name__)
CORS(app)

init_login_controller(app)
with app.app_context():
    client_controller = ClientController(app)
    employee_controller = EmployeeController(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)