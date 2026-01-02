from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# no terminal digite:
# flask shell
# db.create_all() - Importante destacar que quando cria o banco, se utiliza sessao
# db.session.commit() - para salvar as alteracoes no banco


# >>> user = User(username="admin", password="123")
# >>> user
# >>> user.username
# >>> user.password
# >>> db.session.add(user)
# >>> db.session.commit()