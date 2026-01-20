from Server.Domain.Observer import Observer
from flask import Flask, jsonify, request
from Server.service.UserService import UserService
from Server.service.AbsUserService import AbsUserService


class LoginController(Observer):
    def __init__(self, app, abs_user_service):
        super().__init__()
        self.app = app
        self.abs_user_service = abs_user_service

    def login(self):
        username = request.json.get('username')
        password = request.json.get('password')
        print(username, password)

        if not username or not password:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

        user_type = self.abs_user_service.get_user_type(username)
        user_type=user_type[0]['Type']
        print(user_type)
        if self.abs_user_service.check_credentials(username, password):
            return jsonify({"status": "success", "message": "Logged in successfully", "user_type": user_type}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    def update(self):
        pass


def init_login_controller(app):
    user_service: AbsUserService = UserService()
    login_controller = LoginController(app, user_service)
    app.add_url_rule('/api/login', 'login', login_controller.login, methods=['POST'])
