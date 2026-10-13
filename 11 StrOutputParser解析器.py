import sys
import dashscope
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser

# Windows 终端使用 UTF-8，支持模型输出中的 emoji。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

#可以把AImessage转换为字符串
#可以加入chain作为组件存在（Runnable接口）
parser = StrOutputParser()
prompt = PromptTemplate.from_template("我的邻居是：{lastname}，他的爱好是：{hobby},请简要告诉我他适合干什么工作。")
# 使用与 02 示例相同的工作空间；DashScope 地址以 /api/v1 结尾。
dashscope.base_http_api_url = "https://llm-6c17orz0lf15g1ku.cn-beijing.maas.aliyuncs.com/api/v1"
model = ChatTongyi(model="qwen-plus")

chain = prompt | model | parser | model | parser

res = chain.invoke({"lastname": "张", "hobby": "打篮球"})
print(res)
