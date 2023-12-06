import json
import sys
import time

import openai
import requests
import streamlit as st
import os
from langchain.schema import HumanMessage

from FetchNews import getNews, getStockInfo, getFundInfo

os.environ["MINIMAX_GROUP_ID"] = "1682412426347454"
os.environ["MINIMAX_API_KEY"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJOYW1lIjoic2Fuc2FuIiwiU3ViamVjdElEIjoiMTY5MTcyMzM3MDk3OTE4MSIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE2ODI0MTI0MjYzNDc0NTQiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiIiLCJDcmVhdGVUaW1lIjoiMjAyMy0wOC0xMSAxMTowOTozMCIsImlzcyI6Im1pbmltYXgifQ.FAgf5V2C9jRY5ImqchYR8gx-10AVGBZaCbMQUJf6ynUEQqpbB5KU4vSu-Xj26UceGaJRTbdgbNK1b9TAMHxvEPYH6XciPLiztv7OZoYPatiRGq1Q4ZpC7ib4OI7DmXvUU6hLNRNq3DrGfodeJcIkGBJaCIKTx76FMio1SWVl-HdUQ-ux8sgsp2k8hUSNBQtehRqdgR9hli5MMf-QAl2mYVrtQaZL2E-CjAqyR1RQQ4k9yhy9D7O0sl0IqaBbAn1oD9InTJ-wo3fm3bS5E0Jgnj8I2og2Cn67RF6hdfXhU5A38LKlMos98KSHLBDkPz3GmEIxaQdQs04W7ndXvjuLLg"

# openai.api_key = "AI-ONE-32e02ac7642e3738978d002682ab8a49"
# openai.api_base = 'https://b-openapi.basemind.com/openapi/v1'


openai.api_type = "azure"
openai.api_key = "3755a74673ba482491018ecfb4b4cc6e"
openai.api_base = "https://deepqopenai3.openai.azure.com"
openai.api_version = "2023-07-01-preview"

def get_current_weather(input):
    print(input)
    return "上海天气29度，晴"

def getBaidu(input):
    inputJson = json.loads(input)
    url = "http://api.wer.plus/api/dub?t=" + inputJson['keyword']
    response = requests.request("GET", url)
    return response.text
def get_news(input):
    inputJson = json.loads(input)
    if 'type' in inputJson.keys():
        return getNews(inputJson['date'], inputJson['type'])
    else:
        return getNews(inputJson['date'], None)
def get_report_news(input):
    inputJson = json.loads(input)
    url = "https://sq.deepq.tech/api-copilot/report/list?type=0"
    if "date" in inputJson:
        struct_time = time.strptime(inputJson['date'], '%Y-%m-%d')
        ctime = int(time.mktime(struct_time)) * 1000 + 24 * 3600 * 1000
        url += "&timestamp=" + str(ctime)
    print(url)
    response = requests.request("GET", url)
    return response.text
def get_stock_info(input):
    # print(input)
    inputJson = json.loads(input)
    # print(inputJson)
    return getStockInfo(inputJson['keyword'])


def get_fund_info(input):
    # print(input)
    inputJson = json.loads(input)
    # print(inputJson)
    return getFundInfo(inputJson['keyword'])

def select_product(input):
    inputJson = json.loads(input)
    print(inputJson)
    return ""


functions = [
{
        "name": "select_product",
        "description": "根据条件筛选产品",
        "parameters": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "产品募集方式"
                },
                "manager": {
                    "type": "string",
                    "description": "管理人"
                },
                "amount": {
                    "type": "string",
                    "description": "基金规模，单位元，大（10-100亿），中（1-10亿），小（0-1亿）",
                    "enum": ["大", "中", "小"]
                },
                "status": {
                    "type": "integer",
                    "description": "交易状态",
                    "enum": ["可交易", "暂停交易","停止交易"]
                }

            },
            "required": ["type","manager"]
        }
},
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

with st.sidebar:
    functionStr = st.text_area("方法", value = json.dumps(functions))
    st.write("### 解析后")
    functions = json.loads(functionStr)
    st.json(functions)

# st.title("💬 Chatbot")
# st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "今天是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())},
    #   {"role": "system", "content": """
    # 金融产品库：
    # 金选全球长期增长1号：该产品主要投资于全球股票，以超长周期、高仓位的方式参与具有长期成长空间的企业投资。
    # 标普500ETF发起联结 (QDII)：主要投资于美国标普500ETF，紧密跟踪标的指数。
    # 中国50-私人订制：产品围绕中金财富专业买方投顾服务体系，可按照客户需求，定制专属投资解决方案。
    # 华夏国证半导体芯片ETF：半导体是大国竞争的关键产业，政策全面扶持；低估优势明显。
    # 融通健康产业A基金：守正出奇不报团，逆向投资，严控回撤，掘金低估黑马，受机构青睐。
    # 华夏智胜先锋基金：AI量化选股，均衡配置超440只个股，被动金牛7连冠保驾护航！
    # """},
    {"role": "assistant", "content": "你好，我是IC助手，有什么可以帮您？"}]
for msg in st.session_state.messages:
    if msg["role"] != 'system':
        if "function_call" in msg.keys():
            st.chat_message("fun").write(msg["function_call"])
        elif "content" in msg.keys():
            st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input(placeholder="请输入您的问题"):
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # chat = MiniMaxChat(model_name="abab5-chat")
    # print(chat(
    #     [
    #         HumanMessage(
    #             content=prompt
    #         )
    #     ]
    # ))


    print(st.session_state.messages)

    input = []
    for msg in st.session_state.messages:
        if "content" in msg.keys():
            input.append(msg)
    response = openai.ChatCompletion.create(deployment_id="gpt-35-turbo-16k", function_call = "auto", functions = functions, messages=input)
    msg = response.choices[0].message
    # st.session_state.messages.append(msg)
    print(response)
    if "function_call" in msg.keys():
        st.chat_message("fun").write(msg.function_call)
        fun = getattr(sys.modules[__name__], msg.function_call.name)
        st.session_state.messages.append(msg)

        funReply = fun(msg.function_call.arguments)
        st.chat_message("fun").write(funReply)
        input.insert(-1, {"role": "system", "content": funReply})
        print(input)
        response = openai.ChatCompletion.create(deployment_id="gpt-35-turbo-16k", messages=input)
        replyMsg = response.choices[0].message
        if "content" in replyMsg.keys():
            st.chat_message("assistant").write(replyMsg.content)
            st.session_state.messages.append(replyMsg)


    elif "content" in msg.keys():
        print(msg)
        st.chat_message("assistant").write(msg.content)
        st.session_state.messages.append(msg)

