from werkzeug.security import generate_password_hash
from models import Corretor, db
from app import app

with app.app_context():
    corretor = Corretor.query.filter_by(email='teste@virtus.com').first()
    if corretor:
        corretor.senha = generate_password_hash("123456")
        db.session.commit()
        print("✅ Senha atualizada para 123456")
    else:
        print("❌ Corretor não encontrado")
