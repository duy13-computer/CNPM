from flask import Blueprint, request, jsonify, session
from services.watch_service import WatchService
from infrastructure.repositories.watch_repository import WatchRepository
from api.schemas.watch import WatchRequestSchema, WatchResponseSchema
from datetime import datetime
from infrastructure.databases.mssql import session

bp = Blueprint('watch', __name__, url_prefix='/watch')
watch_service = WatchService(WatchRepository(session))


# Khởi tạo service và repository (dùng memory, chưa kết nối DB thật)

request_schema = WatchRequestSchema()
response_schema = WatchResponseSchema()

@bp.route('/', methods=['GET'])
def list_watches():
    watches = watch_service.list_watches()  
    return jsonify(response_schema.dump(watches, many=True)), 200
@bp.route('/<int:watch_id>', methods=['PUT'])
def update_watch(watch_id):
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    watch = watch_service.update_watch(
        watch_id=watch_id,
        name=data['name'],
        brand=data['brand'],
        price=data['price'],
        description=data['description']
    )
    return jsonify(response_schema.dump(watch)), 200
@bp.route('/<int:watch_id>', methods=['GET'])
def get_watch(watch_id):
    watch = watch_service.get_watch(watch_id)
    if not watch:
        return jsonify({'message': 'Watch not found'}), 404
    return jsonify(response_schema.dump(watch)), 200
@bp.route('/', methods=['POST'])
def create_watch():
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    watch = watch_service.create_watch(
        name=data['name'],
        brand=data['brand'],
        price=data['price'],
        description=data['description']
    )
    return jsonify(response_schema.dump(watch)), 201
@bp.route('/<int:watch_id>', methods=['DELETE'])
def delete_watch(watch_id):
    watch_service.delete_watch(watch_id)
    return '', 204


#@bp.route('/', methods=['GET'])
#def list_todos():
#    """
#    Get all todos
#    ---
#    get:
#      summary: Get all todos
#      tags:
#        - Todos
#      responses:
#        200:
#         description: List of todos
#          content:
#            application/json:
#              schema:
#                type: array
#               items:
#                  $ref: '#/components/schemas/TodoResponse'
#    """
#    todos = todo_service.list_todos()
#    return jsonify(response_schema.dump(todos, many=True)), 200

#@bp.route('/<int:todo_id>', methods=['GET'])
#def get_todo(todo_id):
#    todo = todo_service.get_todo(todo_id)
#    if not todo:
#        return jsonify({'message': 'Todo not found'}), 404
#    return jsonify(response_schema.dump(todo)), 200

#@bp.route('/', methods=['POST'])
#def create_todo():
#    data = request.get_json()
#    errors = request_schema.validate(data)
#    if errors:
#        return jsonify(errors), 400
#    now = datetime.utcnow()
#    todo = todo_service.create_todo(
#        title=data['title'],
#        description=data['description'],
#        status=data['status'],
#        created_at=now,
#        updated_at=now
#    )
#    return jsonify(response_schema.dump(todo)), 201

#@bp.route('/<int:todo_id>', methods=['PUT'])
#def update_todo(todo_id):
#   data = request.get_json()
#    errors = request_schema.validate(data)
#    if errors:
#        return jsonify(errors), 400
#    todo = todo_service.update_todo(
#        todo_id=todo_id,
#        title=data['title'],
#        description=data['description'],
#        status=data['status'],
#        created_at=datetime.utcnow(),  # Có thể lấy từ DB nếu cần
#        updated_at=datetime.utcnow()
#    )
#   return jsonify(response_schema.dump(todo)), 200

#@bp.route('/<int:todo_id>', methods=['DELETE'])
#def delete_todo(todo_id):
#    todo_service.delete_todo(todo_id)
#    return '', 204 