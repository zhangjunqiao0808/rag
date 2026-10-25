"""
知识库
"""
import hashlib
import os
import config_data as config
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str: str):
    """
    检查传入的md5字符串是否已经存在了
    :param md5_str:
    :return: False(未处理过) True(已经处理过，已有记录)
    """
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w", encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False


def save_md5(md5_str: str):
    """
    将传入的md5字符串，记录到文件内保存
    :param md5_str:
    :return:
    """
    with open(config.md5_path, 'a', encoding='utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str: str):
    """
    将传入的字符串转换为md5,如果两个文件md5值一样，说明知识库已经存在这个文件了
    :param input_str:
    :return:
    """

    #将字符串转换为btyes字节数组
    str_bytes = input_str.encode(encoding='utf-8')
    #创建md5对象
    md5_obj = hashlib.md5()  #得到md5对象
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()

    return md5_hex


class KnowledgeBase(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,  #数据库表名
            embedding_function=DashScopeEmbeddings(model='text-embedding-v4'),
            client_settings=Settings(
                chroma_api_impl="chromadb.api.segment.SegmentAPI",
                anonymized_telemetry=False,
            ),
            persist_directory=config.persist_directory  #数据库本地存储路径
        )  #向量存储的实例 Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  #分隔后的每个文本块的最大长度
            chunk_overlap=config.chunk_overlap,  #分隔后的文本块之间的重叠长度
            separators=config.separators,  #自然段落划分的符号
            length_function=len
        )

    def add_knowledge(self, knowledge_str: str, filename):
        """
        将传入的字符串，进行向量化，添加至知识库
        :param filename:
        :param knowledge_str:
        :return:
        """
        #先计算知识库的md5值，判断是否已经存在了
        md5_str = get_string_md5(knowledge_str)
        if check_md5(md5_str):
            return "[跳过]知识库已经存在，文件名：{}".format(filename)

        if len(knowledge_str) > config.max_split_char_number:
            #分隔知识库文本
            knowledge_chunks: list[str] = self.spliter.split_text(knowledge_str)
        else:
            knowledge_chunks = [knowledge_str]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "create_user": "zjq"
        }

        #内容加载到向量库
        self.chroma.add_texts(
            #iterable - list[str]  文本列表
            texts=knowledge_chunks,
            #metadata - list[dict]  元数据列表
            metadatas=[metadata for _ in knowledge_chunks]
        )

        #保存md5记录
        save_md5(md5_str)
        return "[成功]知识库添加成功，文件名：{}".format(filename)


if __name__ == '__main__':
    service = KnowledgeBase()
    service.add_knowledge("减肥就是要少吃多练", "test.txt")
