from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.task_reminder_controller import TaskReminderController

task_reminder_bp = Blueprint('task_reminder', __name__)
controller = TaskReminderController()

@task_reminder_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    return controller.create_task(current_user_id, request.get_json())

@task_reminder_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    return controller.get_tasks(current_user_id)

@task_reminder_bp.route('/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = get_jwt_identity()
    return controller.update_task(current_user_id, task_id, request.get_json())

@task_reminder_bp.route('/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = get_jwt_identity()
    return controller.delete_task(current_user_id, task_id)
