from setting import Settings
import pandas as pd
import operator
import newFunc



settings=Settings()
data_list= settings.group_list

def group_profit(item_list):
    data = data_list[item_list].dropna()
    temp = {item:float(newFunc.profitRank_20(item)) for item in data}
    temp = sorted(temp.items(), key=operator.itemgetter(1),reverse=True)
    template = item_list +" 종목의 한달 수익률 입니다: \\n"
    result = template + str(temp)
    test = result.replace("',", '')
    test = test.replace("('", '')
    test = test.replace("),", '\\n')
    test = test.replace("[", '')
    test = test.replace(")", '')
    result = test.replace("]", '')
    return(result)
