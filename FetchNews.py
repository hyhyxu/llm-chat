import json

import tushare as ts
import requests

ts.set_token('5f6364f5f4d6a3b0680dc2f0834de66349510efa1e0fa3b523b78382')

pro = ts.pro_api()

def getNews(date,type):
    print(date)
    if not type:
        type = '10jqka'
    df = pro.news(src=type, start_date=date+" 00:00:00", end_date=date+" 23:59:59", max_results = 10)
    # df['content'] = None
    result = df[:50].to_json(orient="records",force_ascii=False)
    print(result)
    # for record in result:
    #     result.content = None
    if type =='sina':
        result = '新浪财经资讯快讯有：' + result
    elif type == 'wallstreetcn':
        result = '华尔街新闻资讯快讯有：' + result
    elif type == '10jqka':
        result = '资讯快讯有：' + result
    return result


# getNews('2023-11-05')

def getBoMonth(date):
    return pro.bo_monthly(date=date.replace("-", ""))

def getStockCode(name):
    url = "https://suggest3.sinajs.cn/suggest/type=&key=" + name +"&name=suggestdata_1699494231150"
    response = requests.get(url)
    print(response.text)
    str = response.text.split("\"")[1]
    for record in str.split(";"):
        return record.split(",")[3]

def getFundCode(name):
    url = "https://suggest3.sinajs.cn/suggest/type=&key=" + name +"&name=suggestdata_1699494231150"
    response = requests.get(url)
    print(response.text)
    str = response.text.split("\"")[1]
    for record in str.split(";"):
        return record.split(",")[2]

def getFundInfo(name):
    code = getFundCode(name)
    print(code)
    url = "https://fund.10jqka.com.cn/data/client/myfund/" + code
    response = requests.get(url)

    result = json.loads(response.text.replace("net1","净值"))
    print(result)
    return json.dumps(result, ensure_ascii=False)
def getStockInfo(name):
    code = getStockCode(name)
    exchange = 'SZSE'
    stockCode = code[2:];
    if code.startswith("sz"):
        exchange = 'SZSE'
        stockCode+='.SZ'
    if code.startswith("sh"):
        exchange = 'SSE'
        stockCode += '.SH'
    if code.startswith("bj"):
        exchange = 'BSE'
        stockCode += '.BJ'

    df = pro.stock_company(exchange=exchange, ts_code=stockCode,fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,introduction,main_business')
    return df.to_json(orient="records",force_ascii=False)


# print(pro.stock_company(exchange='SSE', ts_code='600519.SH', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,introduction,main_business'))
# print(getStockInfo('贵州茅台'))

print(getNews("2023-11-20", "sina"))