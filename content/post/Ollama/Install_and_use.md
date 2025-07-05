---
title: How to install and use Ollama?
# image: "/unsplash.jpg"
description: 本文詳細介紹如何在本地端（Windows/Mac/Linux）安裝與使用 Ollama，適合初學者參考。
slug: Ollama
date: 2025-07-05 00:00:00+0000
categories:
    - tutorial
tags:
    - Ollama
    - AI
    - Large language model
    - LLM
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---

# 介紹 Ollama
Ollama 是一個能在 本地（Windows/Mac/Linux）執行大型語言模型（LLM）和 Vision Language Model（VLM） 的框架。

* 開源工具
* 在本地端運行大型語言模型
* 離線特性以保護隱私

# 安裝 Ollama
## Windows
至 [Ollama 官方網站](<https://ollama.com/>)
下載 windows 版本後，點擊執行檔安裝。  
安裝後於終端機中測試是否安裝成功。
```
ollama --help
```
## Mac
參考官方文件的下載指令。
```
brew install ollama
```
## Linux
參考官方文件的下載指令。
```
curl -fsSL https://ollama.com/install.sh | sh
```

# 如何使用 Ollama?
### 在本地啟動服務 
```
ollama serve
```
```
C:\Users\user>ollama serve
```

### 執行語言模型
可以參考官方文件中提供的模型 https://ollama.com/search
```
ollama run [model name]
``` 
若是第一次運行該模型則會執行下載。
minicpm-V 是可用於解說圖片的語言模型，使用 ```/bye``` 離開。
```
C:\Users\user>ollama run minicpm-v:latest
pulling manifest
pulling 262843d4806a: 100% ▕█████████████████▏ 4.4 GB
pulling f8a805e9e620: 100% ▕█████████████████▏ 1.0 GB
pulling 60ed67c565f8: 100% ▕█████████████████▏  506 B
pulling 8603ca877636: 100% ▕█████████████████▏ 5.7 KB
pulling f02dd72bb242: 100% ▕█████████████████▏   59 B
pulling 175e3bb367ab: 100% ▕█████████████████▏  566 B
verifying sha256 digest
writing manifest
success

>>> Discribe this picture "C:\Users\user\Downloads\picture.png"
Added image 'C:\Users\user\Downloads\picture.png'
This image depicts a small white rodent sitting on the ground in an
outdoor setting. The animal appears to have soft fur with light
brownish-grey patches around its eyes and ears. Its pink nose is
prominent, as are its large black eyes which stand out against its pale
face.

>>> /bye
```
終端呼叫模型並輸入指令。
```
C:\Users\user>ollama run llama3.1:8b "define what is atom"
An **atom** (from the Greek word "atomos," meaning indivisible) is the smallest
unit of a chemical element that retains its chemical properties and is
considered the fundamental building block of matter.

In simpler terms, an atom is:

1. **Indivisible**: An atom cannot be broken down into smaller particles using
any known means.
2. **Stable**: Atoms are stable entities that do not change their structure or
composition over time.
3. **Unique**: Each element has a unique set of atoms with specific properties.

... 忽略 ...

Would you like me to explain any related concepts or clarify anything about
atoms?
```

### 查看目前已安裝的語言模型
```
ollama list
```
```
C:\Users\user>ollama list
NAME                ID              SIZE      MODIFIED
minicpm-v:latest    c92bfad01205    5.5 GB    2 hours ago
llama3.1:8b         46e0c10c039e    4.9 GB    2 hours ago
```

### 刪除已安裝的語言模型
```
ollama rm [model name]
```
```
C:\Users\user>ollama rm minicpm-v:latest
deleted 'minicpm-v:latest'

C:\Users\user>ollama list
NAME           ID              SIZE      MODIFIED
llama3.1:8b    46e0c10c039e    4.9 GB    8 hours ago
```


### 
### ```role``` 的 3 個主要類型
| role        | 說明                                      |
| ----------- | --------------------------------------- |
| `system`    | 系統角色，設定「這個模型該如何表現自己」，定義整個對話的角色背景、口吻、限制。 |
| `user`      | 使用者角色，模擬真實使用者輸入的訊息。                     |
| `assistant` | 模型扮演的角色回覆。用來提供上下文（例如多輪對話）。              |


## 使用 Python 與程式串接
### 使用 requests 呼叫
``` python
import requests
import json

# API URL
url = "http://127.0.0.1:11434/v1/chat/completions"

# 請求資料
payload = {
    "model": "llama3.1:8b",  # 對應你本地拉取的模型名稱
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": "What is the population of Paris?"},
        {"role": "assistant", "content": "As of 2023, the population of Paris is about 2.1 million."},
        {"role": "user", "content": "What river flows through Paris?"}
    ]
}

# Headers
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer ollama"  # 傳遞身份驗證資訊，本地伺服器預設不驗證金鑰可省略
}

# 發送 POST 請求
response = requests.post(url, headers=headers, data=json.dumps(payload))

# 顯示結果
if response.status_code == 200: # HTTP 狀態碼 200 代表請求成功。
    data = response.json() # 解析 JSON 資料，此方法將回應內容（ex.字串）轉換成 Python 的資料結構（ex.dict）
    print(data["choices"][0]["message"]["content"])
else:
    print("Error:", response.status_code, response.text)

```

response 返回結構類似：
```
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
```

### 使用 openai SDK 呼叫
#### 安裝 openai
使用 pip 指令進行安裝。  
ps.若沒有 pip 我未來再寫一篇安裝與使用 pip 的文章 ;)
``` 
pip install openai
```
查看安裝版本 & 是否已安裝過
```
pip show openai
```

```
WARNING: Package(s) not found: openai
```

若已安裝過且版本小於 1.0.0，更新 openai 套件
```
pip install --upgrade openai

```

### 使用語言模型
``` python
from openai import OpenAI

client = OpenAI(
    # base_url = "http://localhost:11434/v1",
    base_url = "http://127.0.0.1:11434/v1", # 本地 Ollama 伺服器的 URL，預設端口為 11434
    api_key = "ollama", # 本地 Ollama 不驗證密鑰，只要隨意填入即可，習慣使用 ollama
)

# 呼叫本地 Ollama 伺服器進行 Chat Completion
response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[ # 設定對話內容
        {
            "role": "system", # 設定模型行為
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user", # 使用者輸入的問題
            "content": "What is the capital of France?",
        },
    ],
)
print(response.choices[0].message.content)
```

### 使用 Vision model
``` python
import base64
from openai import OpenAI

image_path = r"C:\圖片路徑.png"

with open(image_path, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read()).decode("utf-8")

# 建立可傳入 Ollama 的完整 URL 字串
image_b64_url = f"data:image/png;base64,{b64_string}"

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="minicpm-v",  # 支援圖片輸入的模型
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Please describe the image in detail."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_b64_url
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
```


<!-- > 
若發生套件衝突，不管當前有沒有裝 openai，也不管目前版本是否是最新版，都會重新下載最新版本並完整重新安裝覆蓋掉原本的 openai 套件。
```
pip install --upgrade --force-reinstall openai
```
-->



<!-- > 
> [文章報導](<https://humanityisland.nccu.edu.tw/qiumeihong_a/>)


## 參考內容
淺談為表情心理學：https://www.thenewslens.com/article/128732 
-->

<!-- > 
> Photo by [Pawel Czerwinski](https://unsplash.com/@pawel_czerwinski) on [Unsplash](https://unsplash.com/)
-->
