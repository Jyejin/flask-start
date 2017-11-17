#-*- coding:utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import Flask, request,render_template
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from pandas import DataFrame
import pandas as pd
import testing
import drawing_test

# For Chatbot
import json
import requests

app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

class NameForm(FlaskForm):
    name = StringField('내용을 입력하세요.',validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/base',methods=['GET','POST'])
def index():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=u''
    return render_template('index.html',form=form,name=name)

@app.route('/',methods=['GET','POST'])
def extract():
    name = None
    form = NameForm()
    result = None
    if form.validate_on_submit():
        name = form.name.data
        result = testing.all_function(name)
        form.name.data = u''
    return render_template('extract.html',form=form,name=name,result=result)


default = ["동철님절키워주세요", "예진이도왔니", "재환이형만족하시죠?"]



@app.route('/message', methods=['GET', 'POST'])
def message():
    userRequest = json.loads(request.get_data().decode('utf-8'))

    print("유저ID:",userRequest['user_key'])
    print("메시지:",userRequest['content'])
    print("Request:",userRequest)

    result=None
    if userRequest['content'] == '동철님절키워주세요' or userRequest['content'] == '예진이도왔니' or userRequest['content'] == '재환이형만족하시죠?':
        return "{\"message\": {\"text\":\"궁금하신 주식정보를 물어봐주세요\"},\"keyboard\": {\"type\": \"text\"}}"

    elif userRequest['content'] == '도와줘요':
        return "{\"message\": {\"text\":\"\\n현재 증권친구 홍길동에서는\\n아래의 기능들을 써볼 수 있다네\\n\\n전일가\\n현재가\\n시가\\n저가\\n고가\\n거래대금(백만)\\n52주최고가\\n52주최저가\\n상장주식수\\n시가총액\\n자본금\\nPER\\nEPS\\n외국인현재\\n액면가\\n상한가\\n하한가\\n거래량\\n등락률\\n전일대비\"},\"keyboard\": {\"type\": \"text\"}}"


    else:
        sentence=userRequest['content']
        result=testing.all_function(sentence)
        print(result)

        return "{\"message\": {\"text\":\"" + result + "\"},\"keyboard\": {\"type\": \"text\"}}"


# 챗봇 Keyboard Initialize
@app.route('/keyboard', methods=['GET', 'POST'])
def key():
    return """{ "type" : "buttons",
                "buttons" : """+'["'+'","'.join(default)+'"]'+"""}"""

@app.route('/data/')
@app.route('/data/<name>')
def data(name):
    data = drawing_test.pullStockData(name)
    data = data.loc['2017']
    data = drawing_test.df_to_np(data)

    return data

@app.route('/chart/<name>')
def chart(name):
    return render_template("chart.html",name=name)

if __name__ == "__main__":
    app.run(port=8080,host='0.0.0.0',debug=True)
