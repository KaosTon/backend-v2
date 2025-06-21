# ✅ Modelagem inicial do banco de dados com SQLAlchemy (Virtus CRM)

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializa o SQLAlchemy
db = SQLAlchemy()

# 🔹 Modelo de Corretor
class Corretor(db.Model):
    __tablename__ = 'corretores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text)

    leads = db.relationship('Lead', backref='corretor', lazy=True)

# 🔹 Modelo de Etiqueta
class Etiqueta(db.Model):
    __tablename__ = 'etiquetas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(20))

# 🔹 Modelo de Lead
class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    origem = db.Column(db.String(100))
    email = db.Column(db.String(100))
    cidade_regiao = db.Column(db.String(100))
    idade = db.Column(db.String(10))
    plano_atual = db.Column(db.String(100))
    cnpj = db.Column(db.String(30))
    cpf_titular = db.Column(db.String(30))
    observacoes = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Novo')

    corretor_id = db.Column(db.Integer, db.ForeignKey('corretores.id'))
    etiqueta_id = db.Column(db.Integer, db.ForeignKey('etiquetas.id'))

    etiqueta = db.relationship('Etiqueta')
