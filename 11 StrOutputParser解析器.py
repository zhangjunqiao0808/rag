from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser

#可以把AImessage转换为字符串
#可以加入chain作为组件存在（Runnable接口）
parser = StrOutputParser()
prompt = PromptTemplate.from_template("我的邻居是：{lastname}，他的爱好是：{hobby},请简要告诉我他适合干什么工作。")
model = ChatTongyi(model="qwen3-max")

chain = prompt | model | parser | model | parser

res = chain.invoke({"lastname": "张", "hobby": "打篮球"})
print(res)
