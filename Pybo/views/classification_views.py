from flask import Blueprint, request
from Pybo.models import Question, Answer
from datetime import datetime
from Pybo import db
import torch
from torchvision import transforms
from PIL import Image
import numpy as np

bp = Blueprint('classification', __name__, url_prefix='/classification')

model = torch.load('Pybo/model.pt', map_location=torch.device('cpu'))  # gpu로 학습 모델은 gpu로 추론하게 되어있음.


@bp.route('/catdog')
def catdog():
    return "고양이입니다."


@bp.route('/birdflower')
def bf():
    # 질문을 등록할 때
    q = Question(subject='질문1', content='고양이 맞나여', create_date=datetime.now())  # 프라이머리키는 자동 생성
    db.session.add(q)  # 한번에 처리
    db.session.commit()  # 파일에 쓰기
    return "비둘기"


@bp.route('/get_question')
def get_question():
    # questions = Question.query.all()  # 질문객체 받아오기 [q1,q2,q3,...]
    # print('질문 갯수 :', len(questions))
    res = Question.query.filter(Question.id == 1).all()
    print(res)
    print(res[0].subject)
    print(res[0].content)

    res1 = Question.query.filter(Question.content.like('%고양이%')).all()
    print('고양이가 들어간 질문의 아이디:', res1[0].id)

    res2 = Question.query.get(1)
    res2.subject = '제목 바꿈 1'
    db.session.commit()

    db.session.delete(res2)  # 삭제할 내용 담기
    db.session.commit()
    return '질문 받아오기 성공'


@bp.route('/manwoman')
def mw():
    return "여성"


@bp.route('/makale', methods=['POST'])  # default method: get
def makale():
    print(request.files)  # 일단 print로 출력해서 파일이 잘 도착했는지 확인
    preds_arr = []

    for f in request.files:
        f = request.files[f]
        print(f.filename)
        f.save(f.filename)

        img = Image.open(f.filename)
        transforms_test = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  # 레즈넷의 노멀라이즈 값
        ])

        # (3,224,224)에 배치를 넣어줘야 함. 3차원에서 4차원으로 변환
        # 배치를 합쳐서 학습을 하니까 배치를 넣고 추론
        # 모델과 마찬가지로 이미지도 cpu를 이용해서 같은 머신을 이용하도록 한다.
        img = transforms_test(img).unsqueeze(0).to('cpu')
        print('img size: ', np.shape(img))
        with torch.no_grad():  # torch.no_grad()의 주된 목적은 autograd를 끔으로써 메모리 사용량을 줄이고 연산 속도를 높히기 위함이다.
            outputs = model(img)
            print('output: ', outputs)
            _, preds = torch.max(outputs, 1)
            classname = ['마동석', '이국주', '카리나']
            print('추론한 이름: ', classname[preds[0]])
            preds_arr.append(classname[preds[0]])

    return preds_arr
