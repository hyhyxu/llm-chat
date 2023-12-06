import json
import sys
import time

import openai
import requests
import streamlit as st
import os
from langchain.schema import HumanMessage

import llm
from FetchNews import getNews, getStockInfo, getFundInfo

from llm import ask

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
                    "type": "integer",
                    "description": "基金规模，单位元",
                    "enum": ["0-1亿", "1-10亿", "10-100亿"]
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
        # {"sender_type": "USER", "content": "今天是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())},
        # {"sender_type": "BOT", "sender_name":"IC助手", "text": "你好，我是IC助手，有什么可以帮您？"}
    ]
for msg in st.session_state.messages:
        if "function_call" in msg.keys():
            st.chat_message(msg["sender_type"]).write(msg["function_call"])
        elif "text" in msg.keys():
            st.chat_message(msg["sender_type"]).write(msg["text"])


if prompt := st.chat_input(placeholder="请输入您的问题"):
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # openai.api_key = openai_api_key
    st.session_state.messages.append({"sender_type": "USER", "sender_name":"用户", "text": prompt})
    st.chat_message("USER").write(prompt)

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
        input.append(msg)
    response = llm.ask(input,functions)
    # response = openai.ChatCompletion.create(deployment_id="gpt-35-turbo-16k", function_call = "auto", functions = functions, messages=input)
    print(response)
    msg = response['choices'][0]['messages'][0]
    input.extend(response["choices"][0]["messages"])

    if "function_call" in msg.keys():
        st.chat_message("FUNCTION").write(msg['function_call'])
        fun = getattr(sys.modules[__name__], msg['function_call']['name'])
        st.session_state.messages.append(msg)

        funReply = fun(msg['function_call']['arguments'])
        st.chat_message("FUNCTION").write(funReply)
        input.append(
            {"sender_type": "FUNCTION", "sender_name": "IC助手", "text": funReply}
        )
        st.session_state.messages.append({"sender_type": "FUNCTION", "sender_name": "IC助手", "text": funReply})

        print(input)
        response = llm.ask(input,functions)
        replyMsg = response['choices'][0]['messages'][0]

        st.session_state.messages.append(replyMsg)
        if "text" in replyMsg.keys() and replyMsg["text"]!="":
            st.chat_message("BOT").write(replyMsg["text"])



    elif "text" in msg.keys():
        print(msg)
        st.chat_message("BOT").write(msg["text"])
        st.session_state.messages.append(msg)

