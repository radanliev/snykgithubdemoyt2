import os
import subprocess
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

# User-friendly error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Page Not Found',
        'message': 'The requested resource could not be found on this server.',
        'status_code': 404,
        'available_endpoints': ['/ping', '/execute', '/file']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.',
        'status_code': 500,
        'support': 'If this problem persists, please contact support.'
    }), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        'error': 'Bad Request',
        'message': 'The request could not be understood by the server.',
        'status_code': 400,
        'hint': 'Please check your request parameters and try again.'
    }), 400

@app.route("/")
def home():
    return jsonify({
        'message': 'Welcome to Snyk Demo App 2',
        'description': 'This application demonstrates additional security vulnerabilities.',
        'endpoints': [
            '/ping',
            '/execute?cmd=<command>',
            '/file?path=<file_path>'
        ],
        'warning': 'This application contains intentional vulnerabilities for demonstration purposes.'
    })

@app.route("/ping")
def ping():
    try:
        hostname = request.args.get("host", "localhost")
        if not hostname:
            return jsonify({
                'error': 'Missing Parameter',
                'message': 'Please provide a "host" parameter to ping.',
                'example': '/ping?host=google.com'
            }), 400
        
        # Vulnerable to command injection
        result = subprocess.check_output(f"ping -c 1 {hostname}", shell=True, text=True)
        return jsonify({
            'message': 'Ping successful',
            'result': result,
            'warning': 'This endpoint is vulnerable to command injection!'
        })
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'Ping Failed',
            'message': f'Could not ping the specified host: {hostname}',
            'details': str(e),
            'hint': 'Please check if the hostname is valid and reachable.'
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Ping Error',
            'message': f'An unexpected error occurred: {str(e)}',
            'hint': 'Please try again with a different hostname.'
        }), 500

@app.route("/execute")
def execute():
    try:
        cmd = request.args.get("cmd")
        if not cmd:
            return jsonify({
                'error': 'Missing Parameter',
                'message': 'Please provide a "cmd" parameter to execute.',
                'example': '/execute?cmd=ls',
                'warning': 'This endpoint is extremely dangerous!'
            }), 400
        
        # Extremely vulnerable to command injection
        result = os.popen(cmd).read()
        return jsonify({
            'message': 'Command executed',
            'result': result,
            'warning': 'This endpoint allows arbitrary command execution!'
        })
    except Exception as e:
        return jsonify({
            'error': 'Command Execution Error',
            'message': f'Failed to execute command: {str(e)}',
            'hint': 'Please check your command syntax and permissions.'
        }), 500

@app.route("/file")
def read_file():
    try:
        file_path = request.args.get("path")
        if not file_path:
            return jsonify({
                'error': 'Missing Parameter',
                'message': 'Please provide a "path" parameter to read a file.',
                'example': '/file?path=/etc/passwd'
            }), 400
        
        # Vulnerable to path traversal
        with open(file_path, 'r') as f:
            content = f.read()
        
        return jsonify({
            'message': 'File read successfully',
            'path': file_path,
            'content': content,
            'warning': 'This endpoint is vulnerable to path traversal attacks!'
        })
    except FileNotFoundError:
        return jsonify({
            'error': 'File Not Found',
            'message': f'The file "{file_path}" could not be found.',
            'hint': 'Please check the file path and ensure the file exists.'
        }), 404
    except PermissionError:
        return jsonify({
            'error': 'Permission Denied',
            'message': f'You do not have permission to read the file "{file_path}".',
            'hint': 'Please check file permissions or try a different file.'
        }), 403
    except Exception as e:
        return jsonify({
            'error': 'File Read Error',
            'message': f'An error occurred while reading the file: {str(e)}',
            'hint': 'Please check the file path and try again.'
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
