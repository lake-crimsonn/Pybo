from flask import Blueprint

bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.route('/chatgpt')
def chatgpt():
    return "chatgpt."


@bp.route('/lama2')
def lama2():
    return "lama2"
