#encoding=utf-8

# -------------------------------------------------------libraries----------------------------------------------------------
# Standard library
from flask import jsonify, abort

# Third-party libraries
from flask_restful import Resource, reqparse


# User define module
from app.models import Permission
from app.apis.httpauth import auth, permission_required, admin_required
from app.tasks import add

# ------------------------------------------------------Global Variables----------------------------------------------------
parser = reqparse.RequestParser()
# add the parameters here
parser.add_argument("id", type=str, required=True, help="id cannot be blank!")
parser.add_argument("date", type=str)


# -----------------------------------------------------------Main-----------------------------------------------------------
class Todo(Resource):
    """An example.
    """
    @auth.login_required
    @permission_required(Permission.API)
    def get(self):
        """GET Method, get all or any items.
        """
        args = parser.parse_args()                         # parse arguments
        if not args['date'] or not args['id']:             # check if all required arguments are given
            abort(400)                                     # raise 400 error if lack any arguments
        add.delay(1, 2)
        print 'Hello world!'
        return jsonify({'message': 'get method'})

    @auth.login_required
    @permission_required(Permission.API)
    def post(self):
        """Post Method, add new items.
        """
        return jsonify({'message': 'post api'})

    @auth.login_required
    @permission_required(Permission.API)
    def put(self):
        """PUT Method, update existing items.
        """
        return jsonify({'message': 'put api'})

    @auth.login_required
    @permission_required(Permission.API)
    def delete(self):
        """DELETE Method, delete existing items.
        """
        return jsonify({'message': 'delete api'})