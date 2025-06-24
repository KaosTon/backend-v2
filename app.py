
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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

# Registro de Blueprints e inicialização
if __name__ == "__main__":
    app.register_blueprint(routes_leads)
    app.register_blueprint(routes_corretores)
    app.register_blueprint(routes_etiquetas)
    app.register_blueprint(auth_bp)

    with app.app_context():
        from models import db  # Garante que o db está sendo importado no contexto certo
        db.create_all()
        print("✅ Banco criado com sucesso!")

    app.run(debug=True)