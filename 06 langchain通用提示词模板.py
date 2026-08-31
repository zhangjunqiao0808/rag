from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "我姓{last_name},刚生了一个{gender}宝宝，你帮我取个名字，简单回答"
)

#调用.format方法注入信息
#prompt_text = prompt_template.format(last_name="张", gender="女孩")

model = Tongyi(model="qwen-max")
# res = model.invoke(input=prompt_text)
# print(res)

chain = prompt_template | model
res = chain.invoke(input={"last_name":"张","gender":"女"})
print(res)