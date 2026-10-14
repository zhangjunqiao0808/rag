from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

model = ChatTongyi(model="qwen-plus")
str_parser = StrOutputParser()
# prompt = PromptTemplate.from_template(
#     "你需要根据历史会话回应用户问题，历史对话：{chat_history}，用户提问：{input}，请回答。"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据历史会话回应用户问题，历史对话："),
        MessagesPlaceholder("chat_history"),
        ("human","请回答如下问题：{input}")
    ]
)
#为了方便查看历史消息，打印
def print_history(prompt):
    print("=" * 20, prompt.to_string())
    return prompt
base_chain = prompt | print_history | model | str_parser

store = {}  #key就是sessionid ,value是InMemoryChatMessageHistory类对象，记录每个用户的消息历史
#实现通过会话ID获取InMemoryChatMessageHistory类对象
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

#创建一个新的链，对原有链增加历史消息功能
conversation_chain = RunnableWithMessageHistory(
    base_chain,  #原有被增强的chain
    get_history,  #通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",  #表示用户输入在模版中的占位符
    history_messages_key="chat_history"
)

if __name__ == '__main__':
    # 添加Langchain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "user_001"
        }
    }
    res = conversation_chain.invoke({"input": "小明有2只猫"}, session_config)
    print(res)
    res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    print(res)
    res = conversation_chain.invoke({"input": "请问一共有多少动物？"}, session_config)
    print(res)
