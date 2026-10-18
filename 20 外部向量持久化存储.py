import faulthandler
from pathlib import Path

from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

faulthandler.enable()
BASE_DIR = Path(__file__).resolve().parent

vector_store = Chroma(
    collection_name="test",
    embedding_function=DashScopeEmbeddings(),
    # Windows 上绕过默认 Rust 后端的原生访问冲突。
    client_settings=Settings(
        chroma_api_impl="chromadb.api.segment.SegmentAPI",
        anonymized_telemetry=False,
    ),
    # 独立建库，保留原来的 Rust 后端数据库。
    persist_directory=str(BASE_DIR / "chromadb_python")
)
loader = CSVLoader(
    file_path=str(BASE_DIR / "data" / "csvloader_test.csv"),
    encoding="utf-8"
)
documents = loader.load()
#向量库新增、删除、检索
vector_store.add_documents(
    documents=documents,
    ids=["id"+ str(i) for i in range(1,len(documents)+1)]
)
#删除，传入[id1,id2]
#vector_store.delete(["id1","id2"])
#检索，返回类型list[document]
result=vector_store.similarity_search(
    "python元组有什么特点",
    2,
)

print(result)


