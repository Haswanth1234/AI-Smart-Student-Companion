from flask import jsonify
from app.models.task_reminder import Task
from bson import ObjectId

class TaskReminderController:
    def __init__(self):
        self.task_model = Task()

    def create_task(self, user_id, data):
        """Create a new task"""
        try:
            # Validate required fields
            required_fields = ['title', 'due_date']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            task_data = {
                'user_id': ObjectId(user_id),
                'title': data['title'],
                'description': data.get('description', ''),
                'due_date': data['due_date'],
                'priority': data.get('priority', 'medium'),  # low, medium, high
                'status': data.get('status', 'pending'),      # pending, completed
                'is_ai_generated': data.get('is_ai_generated', False)
            }

            task_id = self.task_model.create(task_data)
            
            return jsonify({
                'message': 'Task created successfully',
                'task_id': str(task_id)
            }), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_tasks(self, user_id):
        """Get all tasks for a user"""
        try:
            tasks = self.task_model.find_by_user(user_id)
            
            # Convert ObjectId to string for JSON serialization
            serialized_tasks = []
            for task in tasks:
                task['_id'] = str(task['_id'])
                task['user_id'] = str(task['user_id'])
                serialized_tasks.append(task)
                
            return jsonify(serialized_tasks), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def update_task(self, user_id, task_id, data):
        """Update a task"""
        try:
            # Check if task exists and belongs to user
            existing_task = self.task_model.find_by_id(task_id)
            if not existing_task:
                return jsonify({'error': 'Task not found'}), 404
                
            if str(existing_task['user_id']) != user_id:
                return jsonify({'error': 'Unauthorized'}), 403

            # Allowed update fields
            allowed_fields = ['title', 'description', 'due_date', 'priority', 'status']
            update_data = {k: v for k, v in data.items() if k in allowed_fields}
            
            if not update_data:
                return jsonify({'message': 'No valid fields to update'}), 400

            result = self.task_model.update(task_id, user_id, update_data)
            
            if result.modified_count > 0:
                return jsonify({'message': 'Task updated successfully'}), 200
            else:
                return jsonify({'message': 'No changes made'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_task(self, user_id, task_id):
        """Delete a task"""
        try:
            result = self.task_model.delete(task_id, user_id)
            
            if result.deleted_count > 0:
                return jsonify({'message': 'Task deleted successfully'}), 200
            else:
                return jsonify({'error': 'Task not found or unauthorized'}), 404

        except Exception as e:
            return jsonify({'error': str(e)}), 500
