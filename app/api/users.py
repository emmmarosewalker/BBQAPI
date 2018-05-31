from app.api import bp
from app.models import User
from flask import jsonify

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user_info = User.query.get_or_404(id).to_dict()
    return jsonify(user_info)

@bp.route('/users', methods=['GET'])
def get_users():
    pass

@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass

@bp.route('/users', methods=['POST'])
def new_user():
    pass

