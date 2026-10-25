from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.runnables import RunnablePassthrough

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

#langchain中向量存储对象，有一个方法：as_retriever,可以返回一直Runnable接口
retriever = vector_store.as_retriever(search_kwargs={"k": 2})


#把retriever的返回值list[document]转换为字符串
def format_func(docs):
    if not docs:
        return "无相关参考资料"
    formatted_str = "["
    for doc in docs:
        formatted_str += doc.page_content
    formatted_str += "]"
    return formatted_str


def print_prompt(prompt):
    print(prompt.to_string())
    print("=" * 20)
    return prompt


# RunnablePassthrough 是个占位符，他可以拿到用户invoke的输入，用户invoke之后先给retriever,再给RunnablePassthrough
chain = {"input": RunnablePassthrough(), "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser()

res = chain.invoke(input_text)
print(res)
"""
retriever:  找源码中invoke方法可看到输入输出
    -输入：用户的提问 str
    -输出：向量库检索结果 list[document]     --这里输出的时候把用户的提问丢掉了
    
prompt：
    -输入：用户的提问 + 向量库检索的结果  dict
    -输出：完整的提示词 PromptValue
"""
