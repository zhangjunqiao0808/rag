from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
md5_path = str(BASE_DIR / "md5_python.txt")

#Chroma数据库存储路径
collection_name = 'rag'
# Python 后端使用独立目录，保留原来的数据库。
persist_directory = str(BASE_DIR / 'chroma_db_python')

#splitter参数
chunk_size = 1000
chunk_overlap = 100
separators = ['\n\n', '\n', ' ', '','.','。','?','!',';','？','！']
max_split_char_number = 1000

#retriever参数,检索器返回的文档数量
retriever_k = 1