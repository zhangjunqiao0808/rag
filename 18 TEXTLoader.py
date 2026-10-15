from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader(
    file_path="./data/python.txt",
    encoding="utf-8"
)

document= loader.load()
print(len(document))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  #分段的最大字符数
    chunk_overlap=50,  #分段之间允许重叠的字符数
    #文本分段依据
    separators=["\n\n","\n","。","？","！",".","?","!"," ",""],
    #字符统计依据（函数）
    length_function=len
)

split_docs = splitter.split_documents(document)
print(split_docs,len(split_docs))
