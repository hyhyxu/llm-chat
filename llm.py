import time

import requests
import json

group_id = "1682412426347454"
api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoic2Fuc2FuIiwiU3ViamVjdElEIjoiMTY5MTcyMzM3MDk3OTE4MSIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE2ODI0MTI0MjYzNDc0NTQiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiIiLCJDcmVhdGVUaW1lIjoiMjAyMy0wOC0xMSAxMTowOTozMCIsImlzcyI6Im1pbmltYXgifQ.FAgf5V2C9jRY5ImqchYR8gx-10AVGBZaCbMQUJf6ynUEQqpbB5KU4vSu-Xj26UceGaJRTbdgbNK1b9TAMHxvEPYH6XciPLiztv7OZoYPatiRGq1Q4ZpC7ib4OI7DmXvUU6hLNRNq3DrGfodeJcIkGBJaCIKTx76FMio1SWVl-HdUQ-ux8sgsp2k8hUSNBQtehRqdgR9hli5MMf-QAl2mYVrtQaZL2E-CjAqyR1RQQ4k9yhy9D7O0sl0IqaBbAn1oD9InTJ-wo3fm3bS5E0Jgnj8I2og2Cn67RF6hdfXhU5A38LKlMos98KSHLBDkPz3GmEIxaQdQs04W7ndXvjuLLg"

# 从文本中提取embedding
def get_embedding(text, emb_type):
    url = f"https://api.minimax.chat/v1/embeddings?GroupId={group_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "texts": [
            text
        ],
        "model": "embo-01",
        "type": emb_type
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    res = json.loads(response.text)['vectors'][0]
    return res


def ask(messages,functions):
    url = "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId=" + group_id

    payload = {
        "bot_setting": [
            {
                "bot_name": "IC助手",
                "content": "IC智能助理是一款辅助投顾的机器人助理",
            }
        ],
        "messages": messages,
        "reply_constraints": {"sender_type": "BOT", "sender_name": "IC助手"},
        "model": "abab5.5-chat",
        "tokens_to_generate": 16384,
        "temperature": 0.01,
        "top_p": 0.95,
    }
    if functions:
        payload['functions'] = functions
        payload['function_call'] = {"type":"auto"}
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}

    print(json.dumps(payload))
    response = requests.request("POST", url, headers=headers, json=payload)

    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def functionCall(text):
    url = "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId=" + group_id

    payload = {
        "bot_setting": [
            {
                "bot_name": "MM智能助理",
                "content": "MM智能助理是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。今天是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }
        ],
        "messages": [{"sender_type": "USER", "sender_name": "用户", "text": text}],
        "reply_constraints": {"sender_type": "BOT", "sender_name": "MM智能助理"},
        "model": "abab5.5-chat",
        "functions": [
        {
            "name": "searchWiki",
            "description": "当问到具体某个名词解释时，可以调用此方法获得解释",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "名词"
                    }
                },
                "required": [
                    "keyword"
                ]
            }
        },
            {
                "name": "searchNews",
                "description": "查询某天，某个板块或者个股相关的资讯",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "日期"
                        },
                        "industry": {
                            "type": "string",
                            "description": "行业板块"
                        },
                        "stock": {
                            "type": "string",
                            "description": "个股名称"
                        }
                    },
                    "required": [
                        "date"
                    ]
                }
            }
        ],
        "function_call": {
            "type": "auto"
        },
        "tokens_to_generate": 1034,
        "temperature": 0.01,
        "top_p": 0.95,
    }
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}

    response = requests.request("POST", url, headers=headers, json=payload)

    print(response.text)
    json_resp = response.json()
    if "function_call" in json_resp:
        print(json_resp['function_call'])
        arguments = json.loads(json_resp["function_call"]["arguments"])
        print(arguments)

functions = [
    {
        "name": "getBaidu",
        "description": "获取百科的词条解释",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "需要解释的名词"
                }
            },
            "required": ["keyword"]
        }
    },
{
        "name": "get_stock_info",
        "description": "获取公司信息，包含法人代表、总经理、注册日期、董秘、公司介绍、主营业务等",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "公司名称"
                }
            },
            "required": ["keyword"]
        }
    },
{
        "name": "get_fund_info",
        "description": "获取基金信息，包含基金的净值、基金经理等",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "基金名称"
                }
            },
            "required": ["keyword"]
        }
    },
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_report_news",
        "description": "获取某个日期前最新的研报列表",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "日期，例如2023-10-09"
                }
            }
        }
    },
{
        "name": "get_news",
        "description": "获取新浪财经(sina)、华尔街见闻（wallstreetcn）某个日期全部快讯",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "日期，例如2023-10-09"
                },"type": {
                    "type": "string",
                    "enum": ["sina", "wallstreetcn"]
                }
            }
        }
    }
]

print(ask("上海天气怎么样", functions))