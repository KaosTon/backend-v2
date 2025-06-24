from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, jsonify
from models import db, Corretor

routes_corretores = Blueprint("routes_corretores", __name__)

@routes_corretores.route("/corretores", methods=["GET"])
def listar_corretores():
    corretores = Corretor.query.all()
    return jsonify([{
        "id": c.id,
        "nome": c.nome,
        "email": c.email,
        "ativo": c.ativo,
        "observacoes": c.observacoes,
        "admin": c.admin # Incluindo o campo 'admin' no retorno
    } for c in corretores])

@routes_corretores.route("/corretores/<int:id>", methods=["GET"])
def buscar_corretor(id):
    c = Corretor.query.get_or_404(id)
    return jsonify({
        "id": c.id,
        "nome": c.nome,
        "email": c.email,
        "ativo": c.ativo,
        "observacoes": c.observacoes,
        "admin": c.admin # Incluindo o campo 'admin' no retorno
    })

@routes_corretores.route("/corretores", methods=["POST"])
def criar_corretor():
    data = request.get_json()
    senha_criptografada = generate_password_hash(str(data["senha"]))

    novo = Corretor(
        nome=data["nome"],
        email=data["email"],
        senha=senha_criptografada,
        ativo=True,
        observacoes=data.get("observacoes", ""),
        admin=data.get("admin", False) # Adicionado para permitir definir admin na criação
    )

    db.session.add(novo)
    db.session.commit()
    return jsonify({"mensagem": "Corretor criado com sucesso"}), 201

@routes_corretores.route("/corretores/<int:id>", methods=["PUT"])
def atualizar_corretor(id):
    data = request.get_json()
    c = Corretor.query.get_or_404(id)
    c.nome = data.get("nome", c.nome)
    c.email = data.get("email", c.email)
    c.observacoes = data.get("observacoes", c.observacoes)
    c.ativo = data.get("ativo", c.ativo) # Permitindo atualizar o status de ativo/inativo
    c.admin = data.get("admin", c.admin) # Permitindo atualizar o status de admin
    db.session.commit()
    return jsonify({"mensagem": "Corretor atualizado com sucesso"})

@routes_corretores.route("/corretores/<int:id>", methods=["DELETE"])
def deletar_corretor(id):
    c = Corretor.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"mensagem": "Corretor deletado com sucesso"})

@routes_corretores.route("/corretores/<int:id>/ativar", methods=["PUT"])
def ativar_corretor(id):
    c = Corretor.query.get_or_404(id)
    c.ativo = True
    db.session.commit()
    return jsonify({"mensagem": "Corretor ativado"})

@routes_corretores.route("/corretores/<int:id>/inativar", methods=["PUT"])
def inativar_corretor(id):
    c = Corretor.query.get_or_404(id)
    c.ativo = False
    db.session.commit()
    return jsonify({"mensagem": "Corretor inativado"})

# REMOVIDO: A rota de login foi movida para routes_auth.py para evitar duplicação.
# @routes_corretores.route("/corretores/login", methods=["POST"])
# def login_corretor():
#     data = request.get_json()
#     email = data.get("email")
#     senha = data.get("senha")

#     corretor = Corretor.query.filter_by(email=email).first()

#     if not corretor:
#         return jsonify({"erro": "Corretor não encontrado"}), 404

#     if not check_password_hash(corretor.senha, str(senha)):
#         return jsonify({"erro": "Senha incorreta"}), 401

#     return jsonify({
#         "id": corretor.id,
#         "nome": corretor.nome,
#         "email": corretor.email,
#         "ativo": corretor.ativo,
#         "observacoes": corretor.observacoes
#     }), 200