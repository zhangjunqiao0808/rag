import sys

from langchain_community.document_loaders import PyPDFLoader

# 使用 UTF-8 输出；异常代理字符以 \udxxx 的转义形式显示，避免打印中断。
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

loader = PyPDFLoader(
    file_path="./data/pdf1.pdf",
    mode="page",  #默认是page模式，每个页面形成一个Document对象，
                 #single 模式是一个文档一个Document对象
    #password="xxxx"  #文件打开密码
)
for doc in loader.lazy_load():

    print(doc)
