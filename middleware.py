# # ware functions for processing requests and responses

# from flask import  request, jsonify

# def log_request_info(app):
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Body: %s', request.get_data())

# def handle_options_request():
#     return jsonify({'message': 'CORS preflight response'}), 200

# def error_handling_ware(error):
#     response = jsonify({'error': str(error)})
#     response.status_code = 500
#     return response

# def add_custom_headers(response):
#     response.headers['X-Custom-Header'] = 'Value'
#     return response

# def setup_middleware(app):
#     @app.before_request
#     def before_request():
#         log_request_info(app)

#     @app.after_request
#     def after_request(response):
#         return add_custom_headers(response)

#     @app.errorhandler(Exception)
#     def handle_exception(error):
#         return error_handling_ware(error)

#     @app.route('/options', methods=['OPTIONS'])
#     def options_route():
#         return handle_options_request()

from flask import request, jsonify, g
import logging

def log_request_info(app):
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    app.logger.debug('Content-Type: %s', request.content_type)

def handle_options_request():
    response = jsonify({'message': 'CORS preflight response'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response, 200

def error_handling_ware(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def add_custom_headers(response):
    response.headers['X-Custom-Header'] = 'Flask-Clean-Architecture'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def validate_json_request():
    """Validate JSON requests"""
    if request.method == 'POST' and request.path.startswith('/auth/'):
        # Cho phép cả form data và JSON
        if request.content_type and 'application/json' in request.content_type:
            try:
                request.get_json(force=True)
            except Exception as e:
                return jsonify({'error': 'Invalid JSON data'}), 400
        elif request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            # Form data - OK
            pass
        else:
            # Nếu không có content-type, thử parse form data
            pass
    return None

def setup_middleware(app):
    @app.before_request
    def before_request():
        log_request_info(app)
        
        # Handle preflight requests
        if request.method == 'OPTIONS':
            return handle_options_request()
        
        # Validate JSON cho API routes
        json_error = validate_json_request()
        if json_error:
            return json_error

    @app.after_request
    def after_request(response):
        return add_custom_headers(response)

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {error}")
        return error_handling_ware(error)

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(415)
    def handle_unsupported_media_type(error):
        return jsonify({'error': 'Unsupported Media Type. Expected application/json'}), 415

