"""
基于Streamlit完成WEB网页上传服务
pip install streamlit
"""
import streamlit as st
from  kownledge_base import KnowledgeBase

#添加网页标题
st.title("知识库更新服务")

#file_uploader
uploader_file = st.file_uploader(
    "请上传文件",
    type=['txt'],
    accept_multiple_files=False
)

#session_state 就是一个字典，存储了所有的状态信息
if 'service' not in st.session_state:
    st.session_state['service'] = KnowledgeBase()


if uploader_file is not None:
    #提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type} | 大小：{file_size / 1024:.2f}KB")

    #get_value -> bytes -> decode('utf-8')
    try:
        text = uploader_file.getvalue().decode('utf-8-sig')
        if not text.strip():
            st.warning("文件内容为空，请选择有内容的 TXT 文件。")
        else:
            with st.spinner("正在分块、生成向量并写入知识库……"):
                result = st.session_state['service'].add_knowledge(text, file_name)
            st.write(result)
    except UnicodeDecodeError:
        st.error("文件编码无法识别，请将 TXT 文件另存为 UTF-8 编码后上传。")
    except Exception as exc:
        st.error(f"知识库写入失败：{exc}")
