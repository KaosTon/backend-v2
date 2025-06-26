from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Corretor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)
    admin = db.Column(db.Boolean, default=False)

    leads = db.relationship('Lead', backref='corretor', lazy=True, cascade="all, delete-orphan")

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origem = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    cidade = db.Column(db.String(100))
    idade = db.Column(db.String(10))
    plano_atual = db.Column(db.String(120))
    cnpj = db.Column(db.String(20))
    cpf = db.Column(db.String(20))
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(50))
    etiquetas = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    corretor_id = db.Column(db.Integer, db.ForeignKey('corretor.id'))

    # ✅ NOVO MÉTODO: to_dict() para serialização do objeto Lead para JSON
    def to_dict(self):
        return {
            "id": self.id,
            "origem": self.origem,
            "nome": self.nome,
            "telefone": self.telefone,
            "email": self.email,
            "cidade": self.cidade,
            "idade": self.idade,
            "plano_atual": self.plano_atual,
            "cnpj": self.cnpj,
            "cpf": self.cpf,
            "observacoes": self.observacoes,
            "status": self.status,
            # Converte a string de etiquetas (armazenada no DB) para uma lista no retorno JSON,
            # como o frontend espera para manipulação. Se for None, retorna uma lista vazia.
            "etiquetas": self.etiquetas.split(', ') if self.etiquetas else [],
            # Retorna a data no formato ISO 8601 (string), que é fácil de usar no JavaScript.
            # O nome da chave é "data" para corresponder ao que o frontend espera.
            "data": self.data_criacao.isoformat(),
            "corretor_id": self.corretor_id,
        }

class Etiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(20), nullable=False)

class LeadEtiqueta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    etiqueta_id = db.Column(db.Integer, db.ForeignKey('etiqueta.id'))