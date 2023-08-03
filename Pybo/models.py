from Pybo import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 외래키는 다른 테이블의 프라이머리키와 연결
    # cascade는 질문을 삭제하면 답변도 삭제되도록 설정해준다.
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    # 답변모델에서 질문모델을 참고하기 위해서 relationship을 사용한다.
    # 역으로 질문모델에서 답변모델을 참조하기 위해 backref를 이용한다. 답변은 여러개일 수도 있으니 answer_set
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
