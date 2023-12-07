import json
import sys
import time

import openai
import requests
import streamlit as st

st.set_page_config(page_title="IC查询")
def askCPM(input, prompt):
    inputJson = {
	"input": "今天是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + input,
	"prompt": prompt,
        "config": {
		"infer_type": "beam_search",
		"max_length": 4096,
		"repetition_penalty": 1.05,
		"ngram_penalty": 1.02,
		"temperature": 1.0,
		"top_p": 0.5
	    }
    }
    url = "http://cpmstudio.modelbest.cn/infer"

    response = requests.post( url = url, json=inputJson, headers={"Content-Type":"application/json", "Host":"us-b9c100eb-mo-1d3410e9-me-9706856d.user-us-b9c100eb.modelbest.com"})
    return response.text

prompt = "请尽力回答以下问题，你可以使用以下接口：[{\"name\":\"product_materials_search\",\"description\":\"产品物料搜索\",\"parameters\":{\"type\":\"object\",\"properties\":{\"keyword\":{\"type\":\"string\",\"description\":\"关键词\"},\"productId\":{\"type\":\"string\",\"description\":\"产品代码\"}},\"required\":[\"keyword\"]}},{\"name\":\"product_basic_info\",\"description\":\"查看产品的基本信息\",\"parameters\":{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"需要查询的产品名称或代码\"},\"attribute\":{\"type\":\"string\",\"description\":\"查询的指标\",\"enum\":[\"产品名称\",\"产品代码\",\"产品Id\",\"产品类型\",\"组合备注\",\"组合名称\",\"标准组合名称\",\"管理人\",\"基金经理\",\"持仓客户数\",\"持仓市值\",\"购买起点\",\"风险等级\",\"最新净值\",\"净值日期\",\"今年以来收益\",\"产品阶段\",\"产品展示类型\",\"是否可对比\",\"公募还是私募产品\",\"产品成立日\"]}},\"required\":[\"name\"]}},{\"name\":\"product_hold\",\"description\":\"查看产品的持仓情况\",\"parameters\":{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"产品名称\"},\"code\":{\"type\":\"string\",\"description\":\"产品代码\"}},\"required\":[\"name\"]}},{\"name\":\"client_basic_info\",\"description\":\"查看客户的基本信息\",\"parameters\":{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"需要查询的客户名称或者编号\"},\"attribute\":{\"type\":\"string\",\"description\":\"查询的指标\",\"enum\":[\"客户号\",\"资金账号\",\"账户状态\",\"账户类别\",\"信用标志\",\"信用标志名称\",\"主账户标志\",\"主账户标志名称\",\"客户类型\",\"投资者类型CODE\",\"投资者类型\",\"性别\",\"生日\",\"年龄\",\"营业部ID\",\"学历\",\"开户日期\",\"获客来源\",\"引流渠道\",\"一级渠道\",\"二级渠道\",\"三级渠道\",\"四级渠道\",\"五级渠道\",\"客户状态\",\"反洗钱风险等级\",\"客户群列表\",\"敏感信息标记\",\"客户姓名\",\"头像\",\"手机号\",\"邮箱\",\"邮编\",\"联系人姓名\",\"联系人手机\",\"联系人固话\",\"服务手机\",\"固话\",\"证件类型\",\"证件号码\",\"证件地址\",\"发证机关\",\"证件有效期\",\"联系地址\",\"投资年限\",\"首次交易日期(我司)\",\"首次交易日期(全市场)\",\"行业类型\",\"职业类型\",\"其他职业明细\",\"工作单位\",\"积分\",\"外部资产估计\",\"沪市打新额度\",\"深市打新额度\",\"免打扰选项\",\"开发关系建立日期\",\"主投顾关系建立日期\",\"服务关系建立日期\",\"峰值资产\",\"峰值资产日期\",\"资产净流入（近一年）\",\"企业员工认证日期\",\"企微添加日期\",\"出生城市\",\"客户关系\"]}},\"required\":[\"name\"]}},{\"name\":\"client_business_info\",\"description\":\"查看客户的业务开通情况\",\"parameters\":{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"需要查询的客户名称或者编号\"}},\"required\":[\"name\"]}},{\"name\":\"client_hold_info\",\"description\":\"查看客户基金、股票、理财等持仓情况\",\"parameters\":{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\",\"description\":\"需要查询的客户名称或者编号\"}},\"required\":[\"name\"]}},{\"name\":\"product_select\",\"description\":\"产品筛选\",\"parameters\":{\"type\":\"object\",\"properties\":{\"isConsignment\":{\"type\":\"boolean\",\"description\":\"是否代销\"},\"expectRoe\":{\"type\":\"integer\",\"description\":\"预期收益率；1|0到5%；2|5-8%；3|8%以上\"},\"productLabel\":{\"type\":\"string\",\"description\":\"产品标签\"},\"isHotSearch\":{\"type\":\"boolean\",\"description\":\"是否热搜\"},\"openPurchaseDateBegin\":{\"type\":\"date\",\"description\":\"开放申购日开始, yyyy-MM-dd\"},\"openPurchaseDateEnd\":{\"type\":\"date\",\"description\":\"开放申购日结束, yyyy-MM-dd\"},\"openRedeemDateBegin\":{\"type\":\"date\",\"description\":\"开放赎回日开始, yyyy-MM-dd\"},\"openRedeemDateEnd\":{\"type\":\"date\",\"description\":\"开放赎回日结束, yyyy-MM-dd\"},\"productExpireDateBegin\":{\"type\":\"date\",\"description\":\"产品到期日开始, yyyy-MM-dd\"},\"productExpireDateEnd\":{\"type\":\"date\",\"description\":\"产品到期日结束, yyyy-MM-dd\"},\"queryType\":{\"type\":\"integer\",\"description\":\"查询类型，1|公募,2|非公募\"},\"raiseBeginDateBegin\":{\"type\":\"date\",\"description\":\"募集起始日开始, yyyy-MM-dd\"},\"raiseBeginDateEnd\":{\"type\":\"date\",\"description\":\"募集起始日结束, yyyy-MM-dd\"},\"riskLevel\":{\"type\":\"integer\",\"description\":\"产品风险等级\",\"enum\":[\"低风险\",\"中等偏低风险\",\"中风险\",\"中等偏高风险\",\"高风险\"]},\"subscribeStartPoint\":{\"type\":\"integer\",\"description\":\"认购起点\"},\"productAccumulateType\":{\"type\":\"string\",\"description\":\"产品募集方式\",\"enum\":[\"私募\",\"公募\",\"线下\",\"场内基金\",\"组合基金\"]}}}},{\"name\":\"client_select\",\"description\":\"客户筛选\",\"parameters\":{\"type\":\"object\",\"properties\":{\"totalAssetsStart\":{\"type\":\"integer\",\"description\":\"总资产下限\"},\"totalAssetsEnd\":{\"type\":\"integer\",\"description\":\"总资产上限\"},\"customerType\":{\"type\":\"string\",\"description\":\"客户类型\"},\"customerLevelName\":{\"type\":\"string\",\"description\":\"客户分层名称\"},\"riskTolerance\":{\"type\":\"string\",\"description\":\"风险等级\",\"enum\":[\"保守型(C1)\",\"谨慎型(C2)\",\"稳健型(C3)\",\"积极型(C4)\",\"激进型(C5)\",\"最低级别\"]},\"accountOpenDateBegin\":{\"type\":\"string\",\"description\":\"开户起始日期, yyyy-MM-dd\"},\"accountOpenDateEnd\":{\"type\":\"string\",\"description\":\"开户截止日期, yyyy-MM-dd\"}}}}]"
# print(askCPM("今天天气咋么样",prompt))

functions = [{
    "name": "product_materials_search",
    "description": "产品物料搜索",
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "关键词"
            },
            "productId": {
                "type": "string",
                "description": "产品代码"
            }
        },
        "required": [
            "keyword"
        ]
    }
}, {
    "name": "product_basic_info",
    "description": "查看产品的基本信息",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "需要查询的产品名称或代码"
            },
            "attribute": {
                "type": "string",
                "description": "查询的指标",
                "enum": ["产品名称", "产品代码", "产品Id", "产品类型", "组合备注", "组合名称", "标准组合名称", "管理人",
                         "基金经理", "持仓客户数", "持仓市值", "购买起点", "风险等级", "最新净值", "净值日期",
                         "今年以来收益", "产品阶段", "产品展示类型", "是否可对比", "公募还是私募产品", "产品成立日"]
            }
        },
        "required": [
            "name"
        ]
    }
},
    {
        "name": "product_hold",
        "description": "查看产品的持仓情况",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "产品名称"
                },
                "code": {
                    "type": "string",
                    "description": "产品代码"
                }
            },
            "required": [
                "name"
            ]
        }
    }, {
        "name": "client_basic_info",
        "description": "查看客户的基本信息",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "需要查询的客户名称或者编号"
                },
                "attribute": {
                    "type": "string",
                    "description": "查询的指标",
                    "enum": ["客户号", "资金账号", "账户状态", "账户类别", "信用标志", "信用标志名称", "主账户标志",
                             "主账户标志名称", "客户类型", "投资者类型CODE", "投资者类型", "性别", "生日", "年龄",
                             "营业部ID", "学历", "开户日期", "获客来源", "引流渠道", "一级渠道", "二级渠道", "三级渠道",
                             "四级渠道", "五级渠道", "客户状态", "反洗钱风险等级", "客户群列表", "敏感信息标记",
                             "客户姓名", "头像", "手机号", "邮箱", "邮编", "联系人姓名", "联系人手机", "联系人固话",
                             "服务手机", "固话", "证件类型", "证件号码", "证件地址", "发证机关", "证件有效期",
                             "联系地址", "投资年限", "首次交易日期(我司)", "首次交易日期(全市场)", "行业类型",
                             "职业类型", "其他职业明细", "工作单位", "积分", "外部资产估计", "沪市打新额度",
                             "深市打新额度", "免打扰选项", "开发关系建立日期", "主投顾关系建立日期", "服务关系建立日期",
                             "峰值资产", "峰值资产日期", "资产净流入（近一年）", "企业员工认证日期", "企微添加日期",
                             "出生城市", "客户关系"]
                }
            },
            "required": [
                "name"
            ]
        }
    },
    {
        "name": "client_business_info",
        "description": "查看客户的业务开通情况",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "需要查询的客户名称或者编号"
                }
            },
            "required": [
                "name"
            ]
        }
    },
    {
        "name": "client_hold_info",
        "description": "查看客户基金、股票、理财等持仓情况",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "需要查询的客户名称或者编号"
                }
            },
            "required": [
                "name"
            ]
        }
    },
    {"name": "product_select", "description": "产品筛选", "parameters": {"type": "object", "properties": {
        "isConsignment": {"type": "boolean", "description": "是否代销"},
        "expectRoe": {"type": "integer", "description": "预期收益率；1|0到5%；2|5-8%；3|8%以上"},
        "productLabel": {"type": "string", "description": "产品标签"},
        "isHotSearch": {"type": "boolean", "description": "是否热搜"},
        "openPurchaseDateBegin": {"type": "date", "description": "开放申购日开始, yyyy-MM-dd"},
        "openPurchaseDateEnd": {"type": "date", "description": "开放申购日结束, yyyy-MM-dd"},
        "openRedeemDateBegin": {"type": "date", "description": "开放赎回日开始, yyyy-MM-dd"},
        "openRedeemDateEnd": {"type": "date", "description": "开放赎回日结束, yyyy-MM-dd"},
        "productExpireDateBegin": {"type": "date", "description": "产品到期日开始, yyyy-MM-dd"},
        "productExpireDateEnd": {"type": "date", "description": "产品到期日结束, yyyy-MM-dd"},
        "queryType": {"type": "integer", "description": "查询类型，1|公募,2|非公募"},
        "raiseBeginDateBegin": {"type": "date", "description": "募集起始日开始, yyyy-MM-dd"},
        "raiseBeginDateEnd": {"type": "date", "description": "募集起始日结束, yyyy-MM-dd"},
        "riskLevel": {"type": "integer", "description": "产品风险等级",
                      "enum": ["低风险", "中等偏低风险", "中风险", "中等偏高风险", "高风险"]},
        "subscribeStartPoint": {"type": "integer", "description": "认购起点"},
        "productAccumulateType": {"type": "string", "description": "产品募集方式",
                                  "enum": ["私募", "公募", "线下", "场内基金", "组合基金"]}}}},
    {"name": "client_select", "description": "客户筛选", "parameters": {"type": "object", "properties": {
        "totalAssetsStart": {"type": "integer", "description": "总资产下限"},
        "totalAssetsEnd": {"type": "integer", "description": "总资产上限"},
        "customerType": {"type": "string", "description": "客户类型"},
        "customerLevelName": {"type": "string", "description": "客户分层名称"},
        "riskTolerance": {"type": "string", "description": "风险等级",
                          "enum": ["保守型(C1)", "谨慎型(C2)", "稳健型(C3)", "积极型(C4)", "激进型(C5)", "最低级别"]},
        "accountOpenDateBegin": {"type": "string", "description": "开户起始日期, yyyy-MM-dd"},
        "accountOpenDateEnd": {"type": "string", "description": "开户截止日期, yyyy-MM-dd"}}}}
]

with st.sidebar:
    functionStr = st.text_area("方法", value=json.dumps(functions))
    st.write("### 解析后")
    functions = json.loads(functionStr)
    st.json(functions)


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "今天是" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())},
        {"role": "assistant", "content": "你好，我是IC助手，有什么可以帮您？"}]
for msg in st.session_state.messages:
    if msg["role"] != 'system':
        if "content" in msg.keys():
            st.chat_message(msg["role"]).write(msg["content"])

if input := st.chat_input(placeholder="请输入您的问题"):
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": input})
    st.chat_message("user").write(input)

    response = askCPM(input, prompt)
    print(response)

    msg = {"role": "assistant", "content": response}
    print(msg)

    st.chat_message("assistant").write(msg['content'])
    st.session_state.messages.append(msg)
