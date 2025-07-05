# from openai import OpenAI

# client = OpenAI(
#     # base_url = "http://localhost:11434/v1",
#     base_url = "http://127.0.0.1:11434/v1", # 本地 Ollama 伺服器的 URL，預設端口為 11434
#     api_key = "ollama", # 本地 Ollama 不驗證密鑰，只要隨意填入即可，習慣使用 ollama
# )

# # 呼叫本地 Ollama 伺服器進行 Chat Completion
# response = client.chat.completions.create(
#     model="llama3.1:8b",
#     messages=[ # 設定對話內容
#         # {
#         #     "role": "system", # 設定模型行為
#         #     "content": "You are a helpful assistant.",
#         # },
#         {
#             "role": "user", # 使用者輸入的問題
#             "content": "What is the capital of France?",
#         },
#     ],
# )
# print(response.choices[0].message.content)




import requests
import json
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="llama3.1:8b", # 選擇本地模型
    messages=[
        {
            "role": "system",
            "content": (
                "You are a senior Python engineer assistant. "
                "Answer clearly with code examples if needed. "
                "If the question is unclear, ask clarifying questions first."
            )
        },
        {
            "role": "user",
            "content": "How can I read a large CSV file efficiently in Python?"
        },
        {
            "role": "assistant",
            "content": (
                "You can use the pandas library with chunksize for efficient processing. "
                "For example:\n\n"
                "```python\n"
                "import pandas as pd\n"
                "chunksize = 10 ** 6  # 1 million rows\n"
                "for chunk in pd.read_csv('large_file.csv', chunksize=chunksize):\n"
                "    process(chunk)  # your custom function\n"
                "```"
            )
        },
        {
            "role": "user",
            "content": "Can you also show me how to do it using the csv module without pandas?"
        }
    ]
)


print(response.choices[0].message.content)





'''
返回結構類似
{
    "id": "chatcmpl-1234567890abcdef",
    "object": "chat.completion",
    "created": 1700000000,
    "model": "llama3.1:8b",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "The capital of France is Paris."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 20,
        "completion_tokens": 10,
        "total_tokens": 30
    }
}
'''