import json
import os
import time

from openai import OpenAI
from transformers.utils.versions import require_version

require_version("openai>=1.5.0", "To fix: pip install openai>=1.5.0")

client = OpenAI(
    api_key="{}".format(os.environ.get("API_KEY", "0")),
    base_url="http://localhost:{}/v1".format(os.environ.get("API_PORT", 8000)),
)

tools_path = r"E:\Note\LLM\车家互联\data\train\json_schema_V2.json"
with open(tools_path, 'r', encoding='utf-8') as file:
    tools_temp = json.load(file)
tools = []
for item in tools_temp:
    tools.append({"type": "function", "function": item})


def chat(messages):
    result = client.chat.completions.create(messages=messages, model="test", tools=tools, temperature=0.2)
    return result


def retain_one_if_same(lst):
    return list(set(lst))[0] if len(set(lst)) == 1 else lst[0]


messages = []
while True:
    prompt = input("请输入：")
    messages = []
    messages.append({"role": "user", "content": prompt})
    start = time.time()
    result = chat(messages)
    tool_list = []
    for item in result.choices[0].message.tool_calls:
        tool_call = item.function
        tool_list.append(tool_call)
        # name, arguments = tool_call.name, json.loads(tool_call.arguments)
    print(tool_list)
    end = time.time()
    print("耗时：{}".format(end-start))



