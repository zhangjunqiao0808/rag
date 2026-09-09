from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

model = ChatTongyi(model="qwen3-max")
str_parser = StrOutputParser()
firstPrompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},请帮忙起名字，仅生成一个名字，并告知我，不要加其他信息"
)

secondPrompt = PromptTemplate.from_template(
    "请根据{name}，简单解析这个名字的含义"
)

#需要一个函数传入链中，把AImessage变为字典，{"name":"xxx"}
func = RunnableLambda(lambda ai_msg:{"name":ai_msg.content})

chain = firstPrompt | model | func | secondPrompt | model | str_parser

for chunk in chain.stream({"lastname":"张","gender":"女儿"}):
    print(chunk)