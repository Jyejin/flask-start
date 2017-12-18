#-*- coding:utf-8 -*-

from flask import Flask

from trend import trend
from chart import chart
from profit import profit
from fundamentalAnalysis import fundamentalanalysis
from technicalAnalysis import technicalanalysis
from groupFunc import thema

app=Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

app.register_blueprint(trend, url_prefix="/trend")
app.register_blueprint(profit, url_prefix="/profit")
app.register_blueprint(chart, url_prefix="/chart")
app.register_blueprint(fundamentalanalysis, url_prefix="/fundamentalanalysis")
app.register_blueprint(technicalanalysis, url_prefix="/technicalanalysis")
app.register_blueprint(thema, url_prefix="/")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
