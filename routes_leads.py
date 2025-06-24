from flask import Blueprint, request, jsonify
from models import db, Lead

routes_leads = Blueprint('routes_leads', __name__)

@routes_leads.route("/leads", methods=["GET"])
def get_all_leads():
    leads = Lead.query.all()
    return jsonify([{
        "id": lead.id,
        "origem": lead.origem,
        "nome": lead.nome,
        "telefone": lead.telefone,
        "email": lead.email,
        "cidade": lead.cidade,
        "idade": lead.idade,
        "plano_atual": lead.plano_atual,
        "cnpj": lead.cnpj,
        "cpf": lead.cpf,
        "observacoes": lead.observacoes,
        "status": lead.status,
        "corretor_id": lead.corretor_id,
        "data_criacao": lead.data_criacao.isoformat()
    } for lead in leads])

@routes_leads.route("/leads/<int:id>", methods=["GET"])
def get_lead(id):
    lead = Lead.query.get_or_404(id)
    return jsonify({
        "id": lead.id,
        "origem": lead.origem,
        "nome": lead.nome,
        "telefone": lead.telefone,
        "email": lead.email,
        "cidade": lead.cidade,
        "idade": lead.idade,
        "plano_atual": lead.plano_atual,
        "cnpj": lead.cnpj,
        "cpf": lead.cpf,
        "observacoes": lead.observacoes,
        "status": lead.status,
        "corretor_id": lead.corretor_id,
        "data_criacao": lead.data_criacao.isoformat()
    })

@routes_leads.route("/leads", methods=["POST"])
def create_lead():
    data = request.get_json()
    novo_lead = Lead(
        origem=data.get("origem"),
        nome=data.get("nome"),
        telefone=data.get("telefone"),
        email=data.get("email"),
        cidade=data.get("cidade"),
        idade=data.get("idade"),
        plano_atual=data.get("plano_atual"),
        cnpj=data.get("cnpj"),
        cpf=data.get("cpf"),
        observacoes=data.get("observacoes"),
        status=data.get("status"),
        corretor_id=data.get("corretor_id")
    )
    db.session.add(novo_lead)
    db.session.commit()
    return jsonify({"mensagem": "Lead criado com sucesso!"}), 201

@routes_leads.route("/leads/<int:id>", methods=["PUT"])
def update_lead(id):
    data = request.get_json()
    lead = Lead.query.get_or_404(id)
    lead.origem = data.get("origem", lead.origem)
    lead.nome = data.get("nome", lead.nome)
    lead.telefone = data.get("telefone", lead.telefone)
    lead.email = data.get("email", lead.email)
    lead.cidade = data.get("cidade", lead.cidade)
    lead.idade = data.get("idade", lead.idade)
    lead.plano_atual = data.get("plano_atual", lead.plano_atual)
    lead.cnpj = data.get("cnpj", lead.cnpj)
    lead.cpf = data.get("cpf", lead.cpf)
    lead.observacoes = data.get("observacoes", lead.observacoes)
    lead.status = data.get("status", lead.status)
    lead.corretor_id = data.get("corretor_id", lead.corretor_id)
    db.session.commit()
    return jsonify({"mensagem": "Lead atualizado com sucesso!"})

@routes_leads.route("/leads/<int:id>", methods=["DELETE"])
def delete_lead(id):
    lead = Lead.query.get_or_404(id)
    db.session.delete(lead)
    db.session.commit()
    return jsonify({"mensagem": "Lead deletado com sucesso!"})
