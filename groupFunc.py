from setting import Settings
import pandas as pd
import operator
from flask import Blueprint
import json
import re
import trend
import profit
import fundamentalAnalysis
import technicalAnalysis

settings=Settings()
data_list= settings.group_lists
thema = Blueprint('thema',__name__)


@thema.route('/<item_list>/<function>')
def groupfunc(item_list, function):
    datas= data_list[item_list].dropna()
    values = [json.loads(eval(settings.lopesStockFunctions.loc[function,'functions']+'('+'\''+item+'\''+')'))['numValue'] for item in datas]
    values = [data.replace('%','') for data in values]
    if '.' in values[0]:
        reg_values = [float(re.findall(r'^([+-]?\d+\.?\d*)$',data)[0]) for data in values]
    else:
        reg_values = [float(data.replace(',','')) for data in values]

    temp=dict(zip(datas,reg_values))
    temp = sorted(temp.items(), key=operator.itemgetter(1),reverse=True)
    template = item_list+" 종목의 "+function+" 입니다: \\n"
    result = template + str(temp)
    test = result.replace("',", '')
    test = test.replace("('", '')
    test = test.replace("),", '\\n')
    test = test.replace("[", '')
    test = test.replace(")", '')
    result = test.replace("]", '')

    return json.dumps({'result':result},ensure_ascii=False)
