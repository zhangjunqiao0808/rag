from langchain_community.embeddings import DashScopeEmbeddings

##创建模型对象，默认使用text-embeddings-v1
model = DashScopeEmbeddings()

#embed_query  embed_documents
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","i love you","i like you"]))
 