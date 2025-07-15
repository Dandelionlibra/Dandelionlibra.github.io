# 從 langchain 引入 pdf 載入器
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

import chromadb


# 載入 PDF 文件
loader = PyPDFLoader('./data/PDF_file.pdf')
documents = loader.load()

# 分割文件內容
text_splitter = RecursiveCharacterTextSplitter(
    # set the chunk size
    chunk_size=100, # 每個 chunk 的最大字元數
    chunk_overlap=20, # 每個 chunk 之間的重疊字元數
    length_function=len # 用於計算字元長度的函數，默認為 len
)

# load_and_split 可在加載時提供文本分割器
pages = loader.load_and_split(text_splitter=text_splitter)  

# 使用 ollama 的 embedding 模型
embeddings_model = OllamaEmbeddings(model="llama3.1:8b")


# 將文檔寫入 ChromaDB
vector_store = Chroma.from_documents(
    documents=pages,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)


# 持久化
# vector_store.persist()


# # db 即是向量儲存庫，可用於相似度檢索
# db = Chroma.from_documents(pages, embeddings_model)


query = "小王子"

# k=3 表示返回最相似的3個文檔
results = vector_store.similarity_search(query, k=3)

print(f"找到 {len(results)} 個相關文檔\n")

print(f"\n找到 {len(results)} 個相關文檔：\n")
for i, doc in enumerate(results, 1):
    print(f"[{i}] {doc.page_content}\n---\n")
