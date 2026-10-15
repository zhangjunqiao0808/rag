from langchain_community.document_loaders import CSVLoader
#不管什么加载器，输出的都是document类型对象
loder = CSVLoader(
    file_path="./data/csvloader_test.csv",
    csv_args={
        "delimiter": ",",  #指定分隔符
        "quotechar": '"',  #指定带有分隔符的文本是
        "filednames": ['a',' b','c'] #指定表头
    },
    encoding="utf-8"
)

#load方法是批量加载，内存大可以，内存小用lazyload
# documents = loder.load()
# for doc in documents:
#     print(doc)

for doc in loder.lazy_load():
    print(doc)