import os
import flask
from flask import request, jsonify, render_template_string

app = flask.Flask(__name__)

# Hardcoded credentials (security issue)
USERNAME = "admin"
PASSWORD = "password123"

# User-friendly error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Page Not Found',
        'message': 'The requested resource could not be found on this server.',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred. Please try again later.',
        'status_code': 500
    }), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        'error': 'Bad Request',
        'message': 'The request could not be understood by the server.',
        'status_code': 400
    }), 400

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({
        'error': 'Forbidden',
        'message': 'You do not have permission to access this resource.',
        'status_code': 403
    }), 403

@app.route("/")
def home():
    return jsonify({
        'message': 'Welcome to the Snyk Demo Application',
        'endpoints': [
            '/eval?code=<python_code>',
            '/cmd (POST with cmd parameter)',
            '/login (POST with username and password)'
        ]
    })

@app.route("/eval", methods=["GET"])
def insecure_eval():
    try:
        code = request.args.get("code")
        if not code:
            return jsonify({
                'error': 'Missing Parameter',
                'message': 'Please provide a "code" parameter to evaluate.',
                'example': '/eval?code=1+1'
            }), 400
        
        result = str(eval(code))  # ⚠️ Arbitrary code execution vulnerability
        return jsonify({
            'result': result,
            'warning': 'This endpoint is vulnerable to code injection attacks!'
        })
    except Exception as e:
        return jsonify({
            'error': 'Evaluation Error',
            'message': f'An error occurred while evaluating the code: {str(e)}',
            'hint': 'Please check your Python syntax and try again.'
        }), 400

@app.route("/cmd", methods=["POST"])
def insecure_command():
    try:
        cmd = request.form.get("cmd")
        if not cmd:
            return jsonify({
                'error': 'Missing Parameter',
                'message': 'Please provide a "cmd" parameter in the request body.',
                'example': 'POST with cmd=ls'
            }), 400
        
        result = os.system(cmd)  # ⚠️ Command injection vulnerability
        return jsonify({
            'message': 'Command executed',
            'result_code': result,
            'warning': 'This endpoint is vulnerable to command injection attacks!'
        })
    except Exception as e:
        return jsonify({
            'error': 'Command Execution Error',
            'message': f'An error occurred while executing the command: {str(e)}',
            'hint': 'Please check your command syntax and permissions.'
        }), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        user = request.form.get("username")
        pw = request.form.get("password")
        
        if not user or not pw:
            return jsonify({
                'error': 'Missing Credentials',
                'message': 'Both username and password are required.',
                'required_fields': ['username', 'password']
            }), 400
        
        if user == USERNAME and pw == PASSWORD:
            return jsonify({
                'message': 'Welcome admin',
                'status': 'success',
                'warning': 'This endpoint uses hardcoded credentials!'
            })
        
        return jsonify({
            'error': 'Authentication Failed',
            'message': 'Invalid username or password.',
            'hint': 'Please check your credentials and try again.'
        }), 401
    except Exception as e:
        return jsonify({
            'error': 'Login Error',
            'message': f'An error occurred during login: {str(e)}',
            'hint': 'Please try again or contact support.'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
