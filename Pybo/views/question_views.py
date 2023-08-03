from flask import Blueprint, render_template

from Pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def q_list():
    question_list = Question.query.order_by(Question.create_date.desc())  # 날짜 정렬순으로 데이터 가져오기
    # jinja2는 jsx처럼 html안에서 파이썬을 사용할 수 있음
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    print(question_id)
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)
