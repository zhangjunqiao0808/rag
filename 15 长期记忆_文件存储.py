import json
import os.path
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id, storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        #完整的文件路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        #确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        #Sequence序列类似List，Tuple
        all_messages = list(self.messages)  #已有的消息列表
        all_messages.extend(messages)  #新的消息和已有的消息融合

        #要将消息同步写入到本地文件中，为了方便，可以将BaseMessage消息转为字典存入本地文件
        #官方message_to_dict：将单个消息对象（BaseMessage）转为字典
        new_messages = [message_to_dict(message) for message in all_messages]
        #将数据写入到文件中
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property  #@property装饰器将messages方法变为成员变量使用
    def messages(self) -> list[BaseMessage]:
        #当前文件内：list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8", ) as f:
                messages = json.loads(f.read())
            return messages_from_dict(messages)  #转换为list[BaseMassages]
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(os.path.join(self.file_path), "w") as f:
            f.write("[]")


####################验证代码######################################

model = ChatTongyi(model="qwen-plus")
str_parser = StrOutputParser()
# prompt = PromptTemplate.from_template(
#     "你需要根据历史会话回应用户问题，历史对话：{chat_history}，用户提问：{input}，请回答。"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据历史会话回应用户问题，历史对话："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)


#为了方便查看历史消息，打印
def print_history(prompt):
    print("=" * 20, prompt.to_string())
    return prompt


base_chain = prompt | print_history | model | str_parser


def get_history(session_id):
    return FileChatMessageHistory(session_id, "./chat_history")


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
    #res = conversation_chain.invoke({"input": "小明有2只猫"}, session_config)
    #print(res)
    #res = conversation_chain.invoke({"input": "小刚有1只狗"}, session_config)
    #print(res)
    res = conversation_chain.invoke({"input": "请问一共有多少动物？"}, session_config)
    print(res)
