from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = 'uploads/'

jwt = JWTManager(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    print('login route')
    print(username,password)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

@app.route('/upload')
# @jwt_required()
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"filename": filename}), 200

# @app.route('/uploaded/<filename>')
# @jwt_required()
# def uploaded_file(filename):
#     return render_template('uploaded.html', filename=filename)

# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# @app.route('/uploaded/<filename>')
# def uploaded_file(filename):
#     return render_template('uploaded.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
