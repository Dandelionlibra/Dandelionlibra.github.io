---
title: LangChain 記憶型檢索問答：《小王子》文本互動實踐
# image: "/unsplash.jpg"
description: 以 LangChain 記憶型檢索問答實現《小王子》文本互動
slug: retrieverQA-2
date: 2025-07-18 8:39:00+0800
categories:
    - example
tags:
    - langchain
    - Ollama
    - Conversation
    - AI
    - Large language model
    - LLM
weight: 1 
---

## 以 LangChain 記憶型檢索問答實現《小王子》文本互動

本文介紹如何利用 LangChain 框架，結合 Ollama Embeddings、ChromaDB 與記憶型問答鏈（RunnableWithMessageHistory），實現能記住上下文的互動式檢索問答。以《小王子》文本為例，展示記憶型問答與一般檢索問答的差異。

### 一、記憶型問答鏈設計

LangChain 提供 `RunnableWithMessageHistory`，可根據 session_id 保存對話歷程，讓模型具備「記憶」功能。核心流程如下：

1. **建立 InMemoryHistory 類**：用於儲存每個 session 的訊息。
2. **載入 PDF 並分割文本**：使用 `PyPDFLoader` 和 `RecursiveCharacterTextSplitter`。
3. **建立向量資料庫**：用 Ollama Embeddings 將文本轉向量，存入 ChromaDB。
4. **設計 Prompt 與 Chain**：結合歷史訊息與提問，串接 LLM。
5. **啟動記憶型問答鏈**：每次提問都能保留上下文，實現多輪互動。


<!-- ### 所需依賴套件

請確保安裝以下 Python 套件：

```bash
pip install langchain langchain_chroma pypdf ollama
```

- `langchain`：核心框架，實現記憶型問答鏈與檢索功能。
- `langchain_chroma`：向量資料庫，用於儲存文本向量。
- `pypdf`：PDF 解析工具，載入文本內容。
- `ollama`：本地 LLM 與 Embeddings 支援。 -->

#### 主要程式片段

完整程式碼請參考：[GitHub 範例程式](https://github.com/Dandelionlibra/Dandelionlibra.github.io/blob/main/content/post/langchain/example/LangChain_memory_ask_via_pdf.ipynb)

```python
# 建立記憶管理器
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)
    def clear(self) -> None:
        self.messages = []

store = {}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

# 啟動記憶型問答鏈
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)
```

### 二、互動範例

#### 問答一：你看過經典故事小王子嗎？
模型回答：
> 我看過《小王子》！這是個非常著名的小說，作者是安托瓦內·德·聖-埃克絮佩里。故事充滿哲理與寓意，讓人思考生命、愛情和友誼。

#### 問答二：啟蒙了你什麼？
模型回答：
> 小王子和這個故事都啟蒙了我對生命、愛情和友誼的看法。它教會我要珍惜生命、關心他人和追求夢想。

#### 問答三：你覺得小王子是個怎樣的人？
模型回答：
> 小王子是一個獨特、敏感和浪漫的年輕人。他能看到世界的美麗和價值，願意為之付出努力，但也有些缺乏勇氣承認自己的情感。

#### 問答四：續寫第二部小王子
模型回答：
> 根據小王子的故事，我們可以繼續他的冒險旅程。他想探索更大的世界，沿途遇到許多新奇的生物和景色，對每件事都充滿好奇和興趣。

### 三、記憶型問答 VS 一般檢索問答

- **記憶型問答**：能保留上下文，支持多輪互動，回答更貼合對話脈絡。
- **一般檢索問答**：每次提問獨立，無法記住前文，回答較為片段。

#### 一般檢索問答範例

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=ollama_llm,
    retriever=vector_db.as_retriever(),
)
qa_chain.invoke('你看過經典故事小王子嘛？')
# 回答：是的，我看過《小王子》。
```

### 四、總結

結合 LangChain 記憶型問答鏈，可針對文本進行多輪互動，模型能記住上下文，回答更自然且具延續性。適合用於深入文本探索、故事續寫等場景。

## 參考資料
- [LangChain RunnableWithMessageHistory 官方文件](https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.history.RunnableWithMessageHistory.html)
- [LangChain 檢索問答基礎篇](https://dandelionlibra.github.io/post/langchain/retrieverqa-1/)