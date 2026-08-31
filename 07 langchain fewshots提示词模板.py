from langchain_core.prompts import FewShotPromptTemplate,PromptTemplate
from langchain_community.llms.tongyi import Tongyi
#示例模版
promptTemplate = PromptTemplate.from_template(
    "单词：{word},反义词：{antonym}"
)

#示例数据，列表套字典
examples = [
    {"word": "开心", "antonym": "难过"},
    {"word": "高", "antonym": "矮"},
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=promptTemplate,        #示例模版
    examples=examples,                    #示例数据
    prefix="告知我单词的反义词，我提供如下示例：",                      #示例之前的提示词
    suffix="请根据示例的格式，给出单词：{input_word}的反义词：",        #示例之后的提示词
    input_variables=["input_word"]        #输入变量
)

prompt_text = few_shot_template.invoke(input={"input_word":"自卑"}).to_string()

model = Tongyi(model="qwen-max")

for chunk in model.stream(input=prompt_text):
    print(chunk,end="",flush=True)