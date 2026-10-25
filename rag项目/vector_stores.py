from langchain_chroma import Chroma
from chromadb.config import Settings
import  config_data as config
class VectorStoreService:
    def __init__(self,embedding):
        """
        :param embedding:传入嵌入模型
        """
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,  # 数据库表名
            embedding_function=self.embedding,
            # 与入库端使用相同的 Python 后端，绕过 Windows 上 Rust 后端的访问冲突。
            client_settings=Settings(
                chroma_api_impl="chromadb.api.segment.SegmentAPI",
                anonymized_telemetry=False,
            ),
            persist_directory=config.persist_directory,  # 数据库存储路径
        )

    def get_retriever(self):
        """
        获取向量检索器
        :return: 向量检索器对象
        """
        return self.vector_store.as_retriever(search_kwargs={"k": config.retriever_k})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    vector_store_service = VectorStoreService(embedding=DashScopeEmbeddings(model='text-embedding-v4'))
    retriever = vector_store_service.get_retriever()
    res = retriever.invoke("dota2里面哪个英雄最强？")
    print(res)
