from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser

# JsonOutputParser可以把AImessage转换为字典
# 可以加入chain作为组件存在（Runnable接口）
json_parser = JsonOutputParser()
str_parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    "我的邻居是：{lastname}，他的爱好是：{hobby},请给他推荐一个职业，"
    "并封装为json格式返回。要求key是'job'，value是你推荐的职业。请严格遵守格式。"
)

second_prompt = PromptTemplate.from_template("职业：{job},请简要介绍这个职业优劣势。")

model = ChatTongyi(model="qwen3-max")

chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"lastname": "张", "hobby": "打篮球"}):
    print(chunk, end="", flush=True)

