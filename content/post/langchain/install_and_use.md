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
LangChain 中 LLM 的最基本功能是根據輸入的文本生成新的文本
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






# Reference
* https://www.youtube.com/playlist?list=PLAr9oL1AT4OElxInUijCzCgU3CpgHTjTI
