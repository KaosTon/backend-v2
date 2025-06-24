# routes_auth.py

from werkzeug.security import check_password_hash
from flask import Blueprint, request, jsonify
from models import Corretor
from models import db
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("🔍 Dados recebidos do frontend:", data)  # 👈 ADICIONE ESTA LINHA

    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'error': 'Email e senha obrigatórios'}), 400

    corretor = Corretor.query.filter_by(email=email).first()

    if not corretor or not check_password_hash(corretor.senha, senha):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    return jsonify({
        'id': corretor.id,
        'nome': corretor.nome,
        'email': corretor.email,
        'admin': getattr(corretor, 'admin', False)  # para evitar erro se não tiver campo admin
    })
