from langchain_community.chat_models.tongyi import ChatTongyi

'''
使用langchain调用通义千问,AIMessage是模拟的AI回复
'''
model = ChatTongyi(model="qwen3-max")
# messages = [
#     SystemMessage(content="你是一个边塞诗人"),
#     HumanMessage(content="写一首唐诗"),
#     AIMessage(content="窗前明月光，疑是地上霜。举头望明月，低头思故乡。"),
#     HumanMessage(content="再写一首")
# ]
'''
利用元组简写消息,简写形式支持填充{变量}占位，运行时自动替换变量
'''

message = [
    ("system", "你是一个边塞诗人"),
    ("human", "写一首唐诗"),
    ("ai", "窗前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "再写一首")
]

response = model.stream(input=message)

for chunk in response:
    print(chunk.content,end="",flush=True)