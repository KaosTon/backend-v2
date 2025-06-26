from werkzeug.security import check_password_hash
from flask import Blueprint, request, jsonify
from models import Corretor
# from models import db # Não é estritamente necessário aqui se Corretor já importa db indiretamente
# import hashlib # Não usado, pode ser removido

from flask_jwt_extended import create_access_token # ✅ Importe create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("🔍 Dados recebidos do frontend:", data) # Boa para depuração, remova em produção.

    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'error': 'Email e senha obrigatórios'}), 400

    corretor = Corretor.query.filter_by(email=email).first()

    if not corretor or not check_password_hash(corretor.senha, senha):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    # ✅ Crie o token de acesso
    # 'identity' é o valor que identifica o usuário (geralmente o ID do usuário)
    # 'additional_claims' pode incluir quaisquer dados adicionais que você queira no token
    additional_claims = {"is_admin": corretor.admin}
    access_token = create_access_token(identity=corretor.id, additional_claims=additional_claims)

    return jsonify({
        'message': 'Login bem-sucedido',
        'access_token': access_token, # ✅ Retorne o token para o frontend
        'id': corretor.id,
        'nome': corretor.nome,
        'email': corretor.email,
        'admin': corretor.admin # Continua retornando para o frontend se ele precisar logo na resposta inicial
    }), 200