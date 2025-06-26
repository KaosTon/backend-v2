from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager # ✅ Importe JWTManager

from models import db, Lead, Corretor, Etiqueta, LeadEtiqueta

# Blueprints
from routes_leads import routes_leads
from routes_corretores import routes_corretores
from routes_etiquetas import routes_etiquetas
from routes_auth import auth_bp

app = Flask(__name__)
CORS(app)

# Configurações do banco
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'leads.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.config["JWT_SECRET_KEY"] = "virtus-super-secret-key"  # ✅ Adicione sua chave secreta aqui
jwt = JWTManager(app) # ✅ Inicialize o JWTManager

# Registro de Blueprints
app.register_blueprint(routes_leads)
app.register_blueprint(routes_corretores)
app.register_blueprint(routes_etiquetas)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    # Lembre-se: db.create_all() deve ser removido ou usado apenas para criar o DB inicial
    # e não para migrações contínuas. As migrações (`flask db upgrade`) lidam com atualizações.
    # with app.app_context():
    #     db.create_all()
    #     print("✅ Banco criado com sucesso!")

    app.run(debug=True)