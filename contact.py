""" contact.py """
from book import app, db


@app.shell_context_processor
def make_shell_context():
    """ make shell context """
    return {'db': db}
