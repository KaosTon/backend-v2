from werkzeug.security import generate_password_hash
from models import Corretor, db
from app import app

with app.app_context():
    # Verifica se o corretor já existe para evitar duplicidade
    existente = Corretor.query.filter_by(email='teste@virtus.com').first()
    if existente:
        print("⚠️ Corretor com esse e-mail já existe.")
    else:
        # Criação do corretor com hash da senha '123456'
        novo_corretor = Corretor(
            nome='Corretor Teste',
            email='teste@virtus.com',
            senha=generate_password_hash("123456"),
            admin=True
        )
        db.session.add(novo_corretor)
        db.session.commit()
        print("✅ Corretor criado com sucesso!")
