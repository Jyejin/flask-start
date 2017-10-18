#-*- coding:utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask import Flask, request,render_template
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import testing

app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY']='hard to guess string'

class NameForm(FlaskForm):
    name=StringField('내용을 입력하세요.',validators=[Required()])
    submit=SubmitField('Submit')


@app.route('/',methods=['GET','POST'])
def extract():
    name=None
    form=NameForm()
    result=None
    if form.validate_on_submit():
        name=form.name.data
        result=testing.all_new(testing.split_stock_sentence(name))
        form.name.data=u''
    return render_template('extract.html',form=form,name=name,result=result)

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0',debug=True)
