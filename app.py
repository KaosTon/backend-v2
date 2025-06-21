from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/data/leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODELOS
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(30))
    origem = db.Column(db.String(100))
    operadora = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    status = db.Column(db.String(100))
    data = db.Column(db.String(20))
    corretorId = db.Column(db.Integer)
    etiquetas = db.Column(db.String(200))
    observacoes = db.Column(db.String(500))
    retorno = db.Column(db.String(20))  # NOVO: Data de retorno

class Corretor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(100))
    observacoes = db.Column(db.String(500))
    ativo = db.Column(db.Boolean, default=True)

# ROTAS
@app.route('/')
def home():
    return "Servidor Virtus CRM rodando com sucesso!"

# ================= LEADS ===================
@app.route('/leads', methods=['GET'])
def get_leads():
    leads = Lead.query.all()
    return jsonify([
        {
            'id': l.id,
            'nome': l.nome,
            'telefone': l.telefone,
            'origem': l.origem,
            'operadora': l.operadora,
            'cidade': l.cidade,
            'status': l.status,
            'data': l.data,
            'corretorId': l.corretorId,
            'etiquetas': l.etiquetas,
            'observacoes': l.observacoes,
            'retorno': l.retorno
        } for l in leads
    ])

@app.route('/leads', methods=['POST'])
def add_lead():
    data = request.get_json()
    novo_lead = Lead(
        nome=data['nome'],
        telefone=data['telefone'],
        origem=data['origem'],
        operadora=data['operadora'],
        cidade=data['cidade'],
        status=data['status'],
        data=data.get('data', datetime.now().strftime('%d/%m/%Y')),
        corretorId=data['corretorId'],
        etiquetas=data.get('etiquetas', ''),
        observacoes=data.get('observacoes', ''),
        retorno=data.get('retorno', '')
    )
    db.session.add(novo_lead)
    db.session.commit()
    return jsonify({'mensagem': 'Lead salvo com sucesso!'}), 201

@app.route('/leads/<int:id>/retorno', methods=['PUT'])
def atualizar_retorno(id):
    data = request.get_json()
    lead = Lead.query.get_or_404(id)
    lead.retorno = data.get('retorno', '')
    db.session.commit()
    return jsonify({'mensagem': 'Data de retorno atualizada com sucesso'})

# ================= CORRETORES ===================
@app.route('/corretores', methods=['GET'])
def listar_corretores():
    corretores = Corretor.query.all()
    return jsonify([
        {
            'id': c.id,
            'nome': c.nome,
            'telefone': c.telefone,
            'email': c.email,
            'observacoes': c.observacoes,
            'ativo': c.ativo
        } for c in corretores
    ])

@app.route('/corretores', methods=['POST'])
def adicionar_corretor():
    data = request.get_json()
    novo = Corretor(
        nome=data['nome'],
        telefone=data['telefone'],
        email=data['email'],
        observacoes=data.get('observacoes', ''),
        ativo=data.get('ativo', True)
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Corretor adicionado com sucesso'}), 201

@app.route('/corretores/<int:id>', methods=['PUT'])
def atualizar_corretor(id):
    data = request.get_json()
    c = Corretor.query.get_or_404(id)
    c.nome = data['nome']
    c.telefone = data['telefone']
    c.email = data['email']
    c.observacoes = data.get('observacoes', '')
    c.ativo = data.get('ativo', True)
    db.session.commit()
    return jsonify({'mensagem': 'Corretor atualizado com sucesso'})

@app.route('/corretores/<int:id>', methods=['DELETE'])
def excluir_corretor(id):
    c = Corretor.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'mensagem': 'Corretor removido com sucesso'})

# ================= EXPORTAÇÃO DE LEADS ===================
ADMIN_EMAILS = [
    "tons217@gmail.com",
    "wsantos@corretoravirtus.com.br",
    "tatiane@corretoravirtus.com.br",
    "contato@corretoravirtus.com.br"
]

@app.route('/exportar-leads', methods=['POST'])
def exportar_leads():
    data = request.get_json()
    email = data.get("email")

    if email not in ADMIN_EMAILS:
        return jsonify({"erro": "Acesso negado"}), 403

    leads = Lead.query.all()
    df = pd.DataFrame([{
        'ID': l.id,
        'Nome': l.nome,
        'Telefone': l.telefone,
        'Origem': l.origem,
        'Operadora': l.operadora,
        'Cidade': l.cidade,
        'Status': l.status,
        'Data': l.data,
        'Corretor ID': l.corretorId,
        'Etiquetas': l.etiquetas,
        'Observações': l.observacoes,
        'Retorno': l.retorno
    } for l in leads])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Leads')
    output.seek(0)

    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', download_name='leads.xlsx', as_attachment=True)

# ================= TRANSFERÊNCIA DE LEADS ===================
@app.route('/leads/<int:id>/transferir', methods=['PUT'])
def transferir_lead(id):
    data = request.get_json()
    novo_corretor_id = data.get("corretorId")
    lead = Lead.query.get_or_404(id)
    lead.corretorId = novo_corretor_id
    db.session.commit()
    return jsonify({'mensagem': 'Lead transferido com sucesso'})

# ================= MAIN ===================
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
