from flask import jsonify
from flask_login import login_required, current_user
from app.models import User, Child

def get_user_children():
    user_group = current_user.group
    children_in_group = Child.query.filter_by(group=user_group).all()

    children_data = [
        {
            'id': child.id,
            'first_name': child.first_name,
            'last_name': child.last_name,
            'age': child.age,
            'group': child.group
        }
        for child in children_in_group
    ]

    return jsonify(children_data)