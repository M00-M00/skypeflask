from app import app
from app.models import User, Transaction
import app.stocks as stocks

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction, 'Security': Security}
