from flask import Flask, render_template, request, jsonify, make_response
from neo_db.get_net import query_movie,query_book,query_cooperate
from neo_db.get_answer import Get_answer
from KGQA.question_classifier2 import AnalysisQuestion
import json
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])


def index(name=None):
    return render_template('index.html', name = name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    type = request.args.get('type')
    print(type)
    if not type:
        type = 'book'
    print(name,type)
    if str(type) == 'book':
        json_data=query_book(str(name))
    elif str(type) == 'movie':
        json_data = query_movie(str(name))
    print(json_data)
    return jsonify(json_data)


@app.route('/search2', methods=['GET', 'POST'])
def search2():
    return render_template('search_cooperation.html')


@app.route('/search_cooperation', methods=['GET', 'POST'])
def search_cooperation():
    name = request.args.get('name')
    name1,name2 = str(name).split(' ')
    print(name1,name2)
    json_data = query_cooperate(name1,name2)
    print(json_data)
    return jsonify(json_data)


@app.route('/KGQA', methods=['GET', 'POST'])
def KGQA():
    return render_template('KGQA.html')


@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params = aq.analysis_question(str(question))
    print(index, params)
    answers = ga.get_data(index, params) # 会返回一个列表
    data = ''
    for answer in answers:
        data += answer[0]+'\n'
    json_data = {'data': data}
    print(json_data)
    return jsonify(json_data)


@app.route('/KGQA_answer_list', methods=['GET', 'POST'])
def KGQA_answer_list():
    question = request.args.get('name')
    aq = AnalysisQuestion()
    ga = Get_answer()
    index, params = aq.analysis_question(str(question))
    print(index, params)
    answers = ga.get_data(index, params)  # 会返回一个列表
    newdata = {'data': [], "code": 0}
    for answer in answers:
        item = {}
        if answer[1] != -1:
            item['name'] = answer[1]
        else:
            item['name'] = answer[0]
        if answer[2] != -1:
            item['rate'] = answer[2]
        else:
            item['rate'] = answer[0]
        if answer[3] != -1:
            item['review'] = answer[3]
        else:
            item['review'] = answer[0]
        if answer[4] != -1:
            item['url'] = answer[4]
        else:
            item['url'] = answer[0]
        newdata['data'].append(item)
    print(newdata)
    rst = make_response(json.dumps(newdata))
    return rst


if __name__ == '__main__':
    app.debug=True
    app.run()
