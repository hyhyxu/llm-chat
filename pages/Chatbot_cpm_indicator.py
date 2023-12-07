import json
import sys
import time

import openai
import requests
import streamlit as st



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

    response = requests.post(url=url, json=inputJson, headers={"Content-Type": "application/json",
                                                               "Host": "us-b9c100eb-mo-1d3410e9-me-9706856d.user-us-b9c100eb.modelbest.com"})
    return response.text


prompt = "请尽力回答以下问题，你可以使用以下接口：[{\"name\":\"search_BI\",\"description\":\"检索公司相关的指标数据\",\"parameters\":{\"type\":\"object\",\"properties\":{\"startTime\":{\"type\":\"date\",\"description\":\"查询开始时间, yyyy-MM-dd\"},\"endTime\":{\"type\":\"date\",\"description\":\"查询结束时间, yyyy-MM-dd\"},\"useTimeDim\":{\"type\":\"boolean\",\"description\":\"是否使用时间维度\"},\"useBranchDim\":{\"type\":\"boolean\",\"description\":\"是否使用营业部维度\"},\"useDivisionDim\":{\"type\":\"boolean\",\"description\":\"是否使用事业部维度\"},\"useOpenChannelDim\":{\"type\":\"boolean\",\"description\":\"是否使用开户渠道维度\"},\"useWarZone\":{\"type\":\"boolean\",\"description\":\"是否使用战区维度\"},\"useAreaHd\":{\"type\":\"boolean\",\"description\":\"是否使用区管维总部度\"},\"branchId\":{\"type\":\"string\",\"description\":\"需要查询的营业部名称\"},\"divisionId\":{\"type\":\"string\",\"description\":\"需要查询的事业部名称\"},\"warZone\":{\"type\":\"string\",\"description\":\"需要查询的战区名称\"},\"attribute\":{\"type\":\"string\",\"description\":\"查询的指标\",\"enum\":[\"总客户数\",\"机构和产品户\",\"机构户\",\"产品户\",\"高净值户\",\"富裕户\",\"大众户\",\"新开户\",\"新开有效户\",\"新开高富户\",\"新开高净值户\",\"新开富裕户\",\"新开大众户\",\"新开两融户\",\"存量净增富裕户\",\"存量升级富裕户\",\"存量富裕户降级\",\"存量净增高净值户\",\"存量升级高净值户\",\"存量高净值户降级\",\"总资产\",\"T1资产\",\"中国50\",\"微50\",\"FoF\",\"公募50\",\"海外30\",\"T2资产\",\"证券产品\",\"公募基金\",\"私募股权\",\"固定收益\",\"结构化产品\",\"现金管理\",\"海外产品\",\"保证金产品\",\"中金宝\",\"聚金利\",\"金汇利\",\"T3资产\",\"T4资产\",\"产品资产\",\"净增总资产\",\"净增T1资产\",\"净增中国50\",\"净增微50\",\"净增FoF\",\"净增公募50\",\"净增海外30\",\"净增净增T2资产\",\"净增证券产品\",\"净增公募基金\",\"净增私募股权\",\"净增固定收益\",\"净增结构化产品\",\"净增现金管理\",\"净增海外产品\",\"净增保证金产品\",\"净增中金宝\",\"净增聚金利\",\"净增金汇利\",\"净增T3资产\",\"净增T4资产\",\"净增产品资产\",\"产品销量\",\"标准产品销量\",\"NNM\",\"个人账户数\",\"团队账户数\",\"公共账户数\",\"人均客户数\",\"人均有效户数\",\"人均富裕户数\",\"人均高净值户数\",\"人均AUM（T1+T2）\",\"人均AUM（T1+T2+T3）\",\"投顾人均新开富裕户数\",\"投顾人均新开高净值户数\",\"投顾人均净增富裕户数\",\"投顾人均净增高净值户数\",\"投顾人均净增总资产\",\"投顾人均净增产品保有量\",\"投顾人均产品销量\",\"投顾人均NNM\",\"投顾人均NNM-个人\",\"收入（管理口径）\",\"收入（财务口径）\",\"超额累进业务量\",\"我司两融余额\",\"市场两融余额\",\"我司两融市占率\",\"股基交易量\",\"市场股基交易量\",\"个人股基交易量\",\"累计养老金开户数\",\"非货ETF\",\"上证指数\",\"深证成指\",\"创业板指\",\"沪深300\",\"市场新增投资者数量\"]}},\"required\":[\"name\"]}}]"
# print(askCPM("今天天气咋么样",prompt))

functions = [{"name": "search_BI", "description": "检索公司相关的指标数据", "parameters": {"type": "object",
                                                                                           "properties": {"startTime": {
                                                                                               "type": "date",
                                                                                               "description": "查询开始时间, yyyy-MM-dd"},
                                                                                                          "endTime": {
                                                                                                              "type": "date",
                                                                                                              "description": "查询结束时间, yyyy-MM-dd"},
                                                                                                          "useTimeDim": {
                                                                                                              "type": "boolean",
                                                                                                              "description": "是否使用时间维度"},
                                                                                                          "useBranchDim": {
                                                                                                              "type": "boolean",
                                                                                                              "description": "是否使用营业部维度"},
                                                                                                          "useDivisionDim": {
                                                                                                              "type": "boolean",
                                                                                                              "description": "是否使用事业部维度"},
                                                                                                          "useOpenChannelDim": {
                                                                                                              "type": "boolean",
                                                                                                              "description": "是否使用开户渠道维度"},
                                                                                                          "useWarZone": {
                                                                                                              "type": "boolean",
                                                                                                              "description": "是否使用战区维度"},
                                                                                                          "useAreaHd": {
                                                                                                              "type": "boolean",
                                                                                                              "description": "是否使用区管维总部度"},
                                                                                                          "branchId": {
                                                                                                              "type": "string",
                                                                                                              "description": "需要查询的营业部名称"},
                                                                                                          "divisionId": {
                                                                                                              "type": "string",
                                                                                                              "description": "需要查询的事业部名称"},
                                                                                                          "warZone": {
                                                                                                              "type": "string",
                                                                                                              "description": "需要查询的战区名称"},
                                                                                                          "attribute": {
                                                                                                              "type": "string",
                                                                                                              "description": "查询的指标",
                                                                                                              "enum": [
                                                                                                                  "总客户数",
                                                                                                                  "机构和产品户",
                                                                                                                  "机构户",
                                                                                                                  "产品户",
                                                                                                                  "高净值户",
                                                                                                                  "富裕户",
                                                                                                                  "大众户",
                                                                                                                  "新开户",
                                                                                                                  "新开有效户",
                                                                                                                  "新开高富户",
                                                                                                                  "新开高净值户",
                                                                                                                  "新开富裕户",
                                                                                                                  "新开大众户",
                                                                                                                  "新开两融户",
                                                                                                                  "存量净增富裕户",
                                                                                                                  "存量升级富裕户",
                                                                                                                  "存量富裕户降级",
                                                                                                                  "存量净增高净值户",
                                                                                                                  "存量升级高净值户",
                                                                                                                  "存量高净值户降级",
                                                                                                                  "总资产",
                                                                                                                  "T1资产",
                                                                                                                  "中国50",
                                                                                                                  "微50",
                                                                                                                  "FoF",
                                                                                                                  "公募50",
                                                                                                                  "海外30",
                                                                                                                  "T2资产",
                                                                                                                  "证券产品",
                                                                                                                  "公募基金",
                                                                                                                  "私募股权",
                                                                                                                  "固定收益",
                                                                                                                  "结构化产品",
                                                                                                                  "现金管理",
                                                                                                                  "海外产品",
                                                                                                                  "保证金产品",
                                                                                                                  "中金宝",
                                                                                                                  "聚金利",
                                                                                                                  "金汇利",
                                                                                                                  "T3资产",
                                                                                                                  "T4资产",
                                                                                                                  "产品资产",
                                                                                                                  "净增总资产",
                                                                                                                  "净增T1资产",
                                                                                                                  "净增中国50",
                                                                                                                  "净增微50",
                                                                                                                  "净增FoF",
                                                                                                                  "净增公募50",
                                                                                                                  "净增海外30",
                                                                                                                  "净增净增T2资产",
                                                                                                                  "净增证券产品",
                                                                                                                  "净增公募基金",
                                                                                                                  "净增私募股权",
                                                                                                                  "净增固定收益",
                                                                                                                  "净增结构化产品",
                                                                                                                  "净增现金管理",
                                                                                                                  "净增海外产品",
                                                                                                                  "净增保证金产品",
                                                                                                                  "净增中金宝",
                                                                                                                  "净增聚金利",
                                                                                                                  "净增金汇利",
                                                                                                                  "净增T3资产",
                                                                                                                  "净增T4资产",
                                                                                                                  "净增产品资产",
                                                                                                                  "产品销量",
                                                                                                                  "标准产品销量",
                                                                                                                  "NNM",
                                                                                                                  "个人账户数",
                                                                                                                  "团队账户数",
                                                                                                                  "公共账户数",
                                                                                                                  "人均客户数",
                                                                                                                  "人均有效户数",
                                                                                                                  "人均富裕户数",
                                                                                                                  "人均高净值户数",
                                                                                                                  "人均AUM（T1+T2）",
                                                                                                                  "人均AUM（T1+T2+T3）",
                                                                                                                  "投顾人均新开富裕户数",
                                                                                                                  "投顾人均新开高净值户数",
                                                                                                                  "投顾人均净增富裕户数",
                                                                                                                  "投顾人均净增高净值户数",
                                                                                                                  "投顾人均净增总资产",
                                                                                                                  "投顾人均净增产品保有量",
                                                                                                                  "投顾人均产品销量",
                                                                                                                  "投顾人均NNM",
                                                                                                                  "投顾人均NNM-个人",
                                                                                                                  "收入（管理口径）",
                                                                                                                  "收入（财务口径）",
                                                                                                                  "超额累进业务量",
                                                                                                                  "我司两融余额",
                                                                                                                  "市场两融余额",
                                                                                                                  "我司两融市占率",
                                                                                                                  "股基交易量",
                                                                                                                  "市场股基交易量",
                                                                                                                  "个人股基交易量",
                                                                                                                  "累计养老金开户数",
                                                                                                                  "非货ETF",
                                                                                                                  "上证指数",
                                                                                                                  "深证成指",
                                                                                                                  "创业板指",
                                                                                                                  "沪深300",
                                                                                                                  "市场新增投资者数量"]}},
                                                                                           "required": ["name"]}}
             ]

st.set_page_config(page_title="指标查询")

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
