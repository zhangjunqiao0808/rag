# pip install jq
from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="./data/students.json",
    jq_schema=".[]",
    text_content=False,  #告知JsonLoader 我抽取的不是字符串
    json_lines=False  #告知JsonLoader ，每一行都不是json
)

document = loader.load()
print(document)