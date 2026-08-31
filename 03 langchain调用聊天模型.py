from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

'''
使用langchain调用通义千问,AIMessage是模拟的AI回复
'''
model = ChatTongyi(model="qwen3-max")
messages = [
    SystemMessage(content="你是一个边塞诗人"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="窗前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    HumanMessage(content="再写一首")
]
response = model.stream(input=messages)

for chunk in response:
    print(chunk.content,end="",flush=True)