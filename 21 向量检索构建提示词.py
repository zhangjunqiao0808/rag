from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore

model = ChatTongyi(model="qwen-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "以我提供的已知参考资料为主，简介专业的回答用户提问。参考资料：{context}"),
        ("user", "用户提问：{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model='text-embedding-v4'))

#准备资料
#add_texts 传入一个list[str]
vector_store.add_texts(
    ["减肥就是要少吃多练", "在减脂期吃东西很重要，要少油少盐控制卡路里并运动起来。", "跑步是很好的运动"])

input_text = "怎么减肥？"

#检索向量库
result = vector_store.similarity_search(input_text, 2)
#返回值类型是[Document],我要把document里面的page_content取出来，转换为[str]
reference_text = "["
for i in result:
    reference_text += i.page_content
reference_text += "]"


def print_prompt(prompt):
    print(prompt.to_string())
    print("=" * 20)
    return prompt


chain = prompt | print_prompt | model | StrOutputParser()
res = chain.invoke({"context":reference_text,"input":input_text})
print(res)