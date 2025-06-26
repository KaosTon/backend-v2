from flask import Blueprint, request, jsonify
# ✅ Importações para JWT
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from models import db, Lead, Corretor # ✅ Importe Corretor se for usar para algo além de Foreign Key (e.g., verificar existência)

routes_leads = Blueprint('routes_leads', __name__)

# ✅ Rota para listar TODOS os leads (agora protegida e verifica admin)
@routes_leads.route("/leads", methods=["GET"])
@jwt_required() # Protege esta rota
def get_all_leads():
    claims = get_jwt()
    is_admin = claims.get("is_admin")

    if not is_admin:
        # Se não for admin, não tem permissão para ver TODOS os leads
        return jsonify({"message": "Acesso negado. Apenas administradores podem ver todos os leads."}), 403

    leads = Lead.query.all()
    # ✅ Retorna leads usando o método to_dict()
    return jsonify([lead.to_dict() for lead in leads])

# ✅ Rota para buscar um lead específico (agora protegida e verifica permissão)
@routes_leads.route("/leads/<int:id>", methods=["GET"])
@jwt_required() # Protege esta rota
def get_lead(id):
    lead = Lead.query.get_or_404(id)
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get("is_admin")

    # Verifica se o usuário é admin OU se o lead pertence ao corretor logado
    if not is_admin and lead.corretor_id != current_user_id:
        return jsonify({"message": "Acesso negado. Você não tem permissão para visualizar este lead."}), 403

    # ✅ Retorna o lead usando o método to_dict()
    return jsonify(lead.to_dict())

# ✅ Rota para criar um lead (agora protegida)
@routes_leads.route("/leads", methods=["POST"])
@jwt_required() # Protege esta rota
def create_lead():
    data = request.get_json()
    current_user_id = get_jwt_identity() # Obtém o ID do usuário logado

    # ✅ Opcional: Se a criação de leads for exclusiva para admin, ou se você quiser associar
    # o lead criado ao corretor logado automaticamente, mesmo que a request não envie corretor_id
    # claims = get_jwt()
    # is_admin = claims.get("is_admin")

    # Certifica-se que o lead tem um corretor_id. Se for admin, pode ser o fornecido.
    # Se for corretor comum, garante que o corretor_id seja o dele mesmo.
    corretor_id_para_salvar = data.get("corretor_id")
    # Se o usuário não é admin, ou se nenhum corretor_id foi fornecido na requisição,
    # atribua o lead ao corretor que está logado.
    if not claims.get("is_admin") or not corretor_id_para_salvar:
        corretor_id_para_salvar = current_user_id


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
        etiquetas=data.get("etiquetas", ""), # ✅ Adicionado campo etiquetas (frontend envia como string)
        corretor_id=corretor_id_para_salvar # ✅ Usa o corretor_id determinado acima
    )
    db.session.add(novo_lead)
    db.session.commit()
    # ✅ Retorna o lead criado usando to_dict() para consistência, e o ID gerado pelo DB
    return jsonify({"mensagem": "Lead criado com sucesso!", "lead": novo_lead.to_dict()}), 201

# ✅ Rota para atualizar um lead (agora protegida e verifica permissão)
@routes_leads.route("/leads/<int:id>", methods=["PUT"])
@jwt_required() # Protege esta rota
def update_lead(id):
    data = request.get_json()
    lead = Lead.query.get_or_404(id)
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get("is_admin")

    # Verifica se o usuário é admin OU se o lead pertence ao corretor logado
    if not is_admin and lead.corretor_id != current_user_id:
        return jsonify({"message": "Acesso negado. Você não tem permissão para atualizar este lead."}), 403

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
    lead.etiquetas = data.get("etiquetas", lead.etiquetas) # ✅ Atualiza o campo etiquetas
    lead.corretor_id = data.get("corretor_id", lead.corretor_id) # Pode ser alterado por admin

    db.session.commit()
    # ✅ Retorna o lead atualizado usando to_dict()
    return jsonify({"mensagem": "Lead atualizado com sucesso!", "lead": lead.to_dict()})

# ✅ Rota para deletar um lead (agora protegida e verifica permissão)
@routes_leads.route("/leads/<int:id>", methods=["DELETE"])
@jwt_required() # Protege esta rota
def delete_lead(id):
    lead = Lead.query.get_or_404(id)
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get("is_admin")

    # Verifica se o usuário é admin OU se o lead pertence ao corretor logado
    if not is_admin and lead.corretor_id != current_user_id:
        return jsonify({"message": "Acesso negado. Você não tem permissão para deletar este lead."}), 403

    db.session.delete(lead)
    db.session.commit()
    return jsonify({"mensagem": "Lead deletado com sucesso!"})

# ✅ NOVA ROTA: Leads específicos do corretor logado
@routes_leads.route("/leads/meus", methods=["GET"])
@jwt_required() # Esta rota exige autenticação JWT
def get_my_leads():
    # Obtém o ID do usuário (corretor) da identidade do token JWT
    current_user_id = get_jwt_identity()
    # Obtém as claims adicionais do token (para verificar se é admin)
    claims = get_jwt()
    is_admin = claims.get("is_admin")

    if is_admin:
        # Se o usuário logado é um administrador, ele pode ver todos os leads.
        # Ajuste isso se admins devem usar uma rota diferente ou se o PainelAdmin já lista tudo.
        leads = Lead.query.all()
    else:
        # Se não for admin, filtra os leads para mostrar apenas aqueles atribuídos a este corretor.
        leads = Lead.query.filter_by(corretor_id=current_user_id).all()

    # Retorna a lista de leads, usando o método to_dict() de cada Lead
    return jsonify([lead.to_dict() for lead in leads])