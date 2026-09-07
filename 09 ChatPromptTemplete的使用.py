from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是个会写诗的人"),
    MessagesPlaceholder("history"),
    ("human", "給我写一首诗")
])

history_messages = [
    ("human", "给我写一首诗"),
    ("ai", "窗前明月光，疑是地上霜。举头望明月，低头思故乡。"),
    ("human", "再来一首"),
    ("ai", "白发三千丈，高挂云间。疑是银河落九天。")
]

promptText = chat_prompt.invoke({"history": history_messages})

model = ChatTongyi(model="qwen3-max")
res = model.invoke(promptText)
print(res.content)

