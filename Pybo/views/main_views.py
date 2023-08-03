from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
import json

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def index():
    # url_for는 블루프린트의 이름 아래 있는 함수의 주소를 찾아준다.
    return redirect(url_for('question.q_list'))


@bp.route('/react')
def users():
    payloads = {
        "members": [{"id": 1, "name": "hehe"}, {"id": 2, "name": "haha"}]
    }
    return json.dumps(payloads)


@bp.route('/meta')
def hello_meta():
    return "메타버스아카데미 ai2"
