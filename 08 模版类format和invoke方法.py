from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate,ChatPromptTemplate

prompt = PromptTemplate.from_template("我的邻居是：{lastname}，他的爱好是：{hobby}")

res1 = prompt.format(lastname="张大壮",hobby="打篮球")
print(res1,type(res1))

res2 = prompt.invoke({"lastname":"张大壮","hobby":"打排球"})
print(res2,type(res2))