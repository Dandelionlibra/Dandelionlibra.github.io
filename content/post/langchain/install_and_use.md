---
title: LangChain 安裝與基本使用
# image: "/unsplash.jpg"
description: 本文介紹如何安裝 LangChain，並透過簡單的範例來展示其基本用法。
slug: uselangchain
date: 2025-07-06 15:33:11+0000
categories:
    - tutorial
tags:
    - langchain
    - AI
    - Large language model
    - LLM
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---

# 安裝 LangChain
使用 pip 指令安裝 LangChain 核心套件，其中提供各組件與基本框架。  
```
pip install langchain
```

安裝 LangChain 與本地 Ollama 模型整合專用驅動，
可以在 LangChain 中使用本地 Ollama 模型作為 LLM。
LangChain 官方維護的專門用於整合本地 Ollama LLM 的插件套件。

因為 LangChain 在 0.3.1 後將原本內建於 `langchain_community.llms.Ollama` 的 Ollama 整合模組 拆分為獨立的 `langchain-ollama` 套件。
```
pip install langchain-ollama
```

# 簡單應用
## 文本生成
LangChain 中 LLM 的最基本功能是根據輸入的文本生成新的文本。

註:不清楚 Ollama 如何使用的可以去看我關於 Ollama 的基礎使用文章。
```
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")
response = llm.invoke("幫我取一個文雅的中國男孩名")
print(response)
```

temperature 用於控制 LLM 生成回答的隨機性與創造性。
| `temperature` 值 | 行為特性                            |
| --------------- | ------------------------------- |
| `0`             | 完全可重現，幾乎總是給出相同回答，適合需要準確且穩定輸出時使用 |
| `0.3 ~ 0.7`     | 中度創造性，適合一般應用                    |
| `1.0`           | 高度創造性，回答可能更多樣化與隨機               |
| `>1`            | 非常隨機，回答可能跳脫常規                   |

例如可以在剛剛的 response 中使用 options 將 temperature 設為 0，使輸出每次都會得到一樣的答案。
```
response = llm.invoke("幫我取一個文雅的中國男孩名", options={"temperature": 0})
```

## 聊天模組

```
from langchain_ollama import ChatOllama
from langchain.schema  import HumanMessage

Chatllm = ChatOllama(model="llama3.1:8b")

test = "幫我取一個文雅的中國男孩名"
messages = [HumanMessage(content=test)]
response = Chatllm.invoke(messages)
print(response)
```

### OllamaLLM vs.ChatOllama
| 項目               | **OllamaLLM**                            | **ChatOllama**                                                       |                     |
| ---------------- | ---------------------------------------- | -------------------------------------------------------------------- | ------------------- |
| **來源**           | `from langchain_ollama import OllamaLLM` | `from langchain_ollama import ChatOllama`                            |                     |
| **用途**           | 單輪文字生成（Single-turn LLM）                  | 多輪對話（Chat-based LLM）                                                 |                     |
| **典型應用場景**       | 單次回答、批次生成資料、文字生成工具                       | 聊天機器人、多輪上下文對話、Memory 結合                                              |                     |
| **輸入型態**         | `str`（純文字 prompt）                        | `List[BaseMessage]`（包含 `SystemMessage`, `HumanMessage`, `AIMessage`） |                     |
| **回傳型態**         | `str`（文字回應）                              | `AIMessage(content='...')`                                           |                     |
| **回傳內容存取**       | 直接使用 `print(response)`                   | 使用 `print(response.content)`                                         |                     |
| **是否支援多輪上下文**    | X                                  | O                                                          |                     |
| **適合結合 Agent**   | 作為推論引擎                                | 作為 Chat Agent 對話引擎                                                 |                     |
| **可搭配 Memory**   | X                                 | 可搭配 Memory 實現上下文持續對話                                               |                     |


# Reference
* https://www.youtube.com/playlist?list=PLAr9oL1AT4OElxInUijCzCgU3CpgHTjTI
