---
title: 使用 Langchain 框架進行檢索提問
# image: "/unsplash.jpg"
description: 以小王子的文本為例，進行檢索提問。
slug: retrieverQA-1
date: 2025-07-18 10:59:00+0000
categories:
    - example
tags:
    - langchain
    - Ollama
    - AI
    - Large language model
    - LLM
weight: 1 
---
## 程式運行詳細步驟
以下以 Jupyter Notebook 格式，記錄如何使用 LangChain 框架結合 Ollama Embeddings 與 ChromaDB，實現 PDF 文件的檢索式問答。  
詳細程式參考：[GitHub 範例程式](https://github.com/Dandelionlibra/Dandelionlibra.github.io/blob/main/content/post/langchain/example/LangChain_ask_via_pdf.ipynb)

### 1. 載入必要套件與初始化 Embedding 模型

```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 初始化 Ollama Embeddings
embeddings_model = OllamaEmbeddings(
    base_url='http://dandelion-ollama-1:11434',
    model="bge-m3:567m",
)
```

### 2. 載入 PDF 文件並分割文本

```python
# 載入 PDF
loader = PyPDFLoader('./data/PDF_file.pdf')
docs = loader.load_and_split()

# 設定分段參數
chunk_size = 256
chunk_overlap = 128

text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
documents = text_splitter.split_documents(docs)
```

### 3. 建立 Chroma 向量資料庫

```python
db = Chroma.from_documents(
    documents,
    embedding=embeddings_model,
    persist_directory="./story-db"
)
```

### 4. 啟動檢索式問答鏈 (RetrievalQA Chain)

```python
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

ollama_llm = OllamaLLM(
    base_url='http://dandelion-ollama-1:11434',
    model="llama3.1:8b",
    temperature=0.0,
    num_predict=512
)

qa_chain = RetrievalQA.from_chain_type(
    llm=ollama_llm,
    retriever=db.as_retriever(),
)
```

### 5. 問答範例及模型回答

以下僅列出部分問答範例，其餘可自行嘗試：

---

```python
query = "玫瑰是誰？"
result = qa_chain.invoke(query)
print(result)
```
**模型回答：**
```
{'query': '玫瑰是誰？', 'result': '玫瑰是小王子的玫瑰花，還有園中其他五千朵玫瑰花（但小王子的玫瑰花是獨一無二的）。'}
```

---

```python
qa_chain.invoke('小王子的來歷是什？')
```
**模型回答：**
```
{'query': '小王子的來歷是什？', 'result': '小王子所來自的那個星球是小行星B612。'}
```

---

```python
qa_chain.invoke('你覺得小王子是個怎樣的人？')
```
**模型回答：**
```
{'query': '你覺得小王子是個怎樣的人？', 'result': '根據文中描述，小王子的性格可以看出來。他似乎是一個敏感、浪漫、獨立的年輕人。他對他所遇到的陌生人的評價很細致，能夠看穿別人的真實面目。他也顯示出對自由和自主的渴望。'}
```

---

> 更多問題可依據文本內容自由發揮，探索不同答案。

### 筆記重點

- 透過 `PyPDFLoader` 讀取 PDF，並用 `RecursiveCharacterTextSplitter` 分割文本，利於後續檢索。
- 使用 Ollama Embeddings 將文本轉為向量，存入 ChromaDB。
- 結合 Ollama LLM 與 RetrievalQA Chain，實現自然語言問答。
- 可針對文本內容進行多樣化提問，快速獲得答案。

