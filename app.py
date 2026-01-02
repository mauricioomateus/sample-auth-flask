from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app) # Initialize the database with the Flask app
login_manager.init_app(app)

#view login
login_manager.login_view = 'login' # Define a rota de login

@login_manager.user_loader # Função para carregar o usuário a partir do ID armazenado na sessão
def load_user(user_id):
    return User.query.get(int(user_id)) 


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)  # Verifica se o usuário está autenticado
            return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 400


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"})


@app.route('/singup', methods=['POST'])
def singup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"message": "Usuario já existe"}), 400
        
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuario cadastrado com sucesso"}), 201
    return jsonify({"message": "Dados invalidos"}), 400


@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
    user = db.session.get(User, user_id)

    if user:
        return jsonify({"username": user.username})
    
    return jsonify({"Message": "Usuario nao encontrado"}), 404  


@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = db.session.get(User, user_id)
    data = request.json

    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": "Usuario atualizado com sucesso"})
    
    return jsonify({"Message": "Usuario nao encontrado"}), 404 


@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = db.session.get(User, user_id)

    if current_user == user.id:
        return jsonify({"message": "Delecao nao permitida"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario deletado com sucesso"})
    
    return jsonify({"message": "Usuario nao encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=9000)