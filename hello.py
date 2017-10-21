#-*- coding:utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import Flask, request,render_template
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import testing

# For Chatbot
import json
import requests

app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='hard to guess string'

class NameForm(FlaskForm):
    name=StringField('내용을 입력하세요.',validators=[Required()])
    submit=SubmitField('Submit')


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
    name=None
    form=NameForm()
    table=None
    result=None
    if form.validate_on_submit():
        name=form.name.data
        result=testing.all_new(testing.split_stock_sentence(name))
        #table=db.extracting(name)
        form.name.data=''
    return render_template('extract.html',form=form,name=name,result=result)


default = ["도와줘요홍길동"]

@app.route('/message', methods=['GET', 'POST'])
def message():
    userRequest = json.loads(request.get_data().decode('utf-8'))
    print(userRequest)
    result=None
    if userRequest['content'] == '도와줘요홍길동':
        return """{"message": {"text":"궁금하신 주식정보를 물어봐주세요"},"keyboard": {"type": "text"}}"""


    elif userRequest['content'] == '엘지전자 최저가':
        return """{"message": {"text":"삼성전자최저가는 삘릴리 입니다"},"keyboard": {"type": "text"}}"""

	
    else:
        name=userRequest['content']
        result=testing.all_new(testing.split_stock_sentence(name))
        print(result)
        return """{"message": {"text":"삼성전자최저가는 삘릴리 입니다"},"keyboard": {"type": "text"}}"""



# 챗봇 Keyboard Initialize 
@app.route('/keyboard', methods=['GET', 'POST'])
def key():
    return """{ "type" : "buttons", 
                "buttons" : """+'["'+'","'.join(default)+'"]'+"""}"""


if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0',debug=True)

