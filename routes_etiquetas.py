from flask import Blueprint, request, jsonify
from models import db, Etiqueta

routes_etiquetas = Blueprint("routes_etiquetas", __name__)

@routes_etiquetas.route("/etiquetas", methods=["GET"])
def listar_etiquetas():
    etiquetas = Etiqueta.query.all()
    return jsonify([{
        "id": e.id,
        "nome": e.nome,
        "cor": e.cor
    } for e in etiquetas])

@routes_etiquetas.route("/etiquetas", methods=["POST"])
def criar_etiqueta():
    data = request.get_json()
    nova = Etiqueta(
        nome=data["nome"],
        cor=data["cor"]
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({"mensagem": "Etiqueta criada com sucesso"}), 201

@routes_etiquetas.route("/etiquetas/<int:id>", methods=["PUT"])
def editar_etiqueta(id):
    data = request.get_json()
    etiqueta = Etiqueta.query.get_or_404(id)
    etiqueta.nome = data.get("nome", etiqueta.nome)
    etiqueta.cor = data.get("cor", etiqueta.cor)
    db.session.commit()
    return jsonify({"mensagem": "Etiqueta atualizada com sucesso"})

@routes_etiquetas.route("/etiquetas/<int:id>", methods=["DELETE"])
def deletar_etiqueta(id):
    etiqueta = Etiqueta.query.get_or_404(id)
    db.session.delete(etiqueta)
    db.session.commit()
    return jsonify({"mensagem": "Etiqueta deletada com sucesso"})
