


# 從 langchain 引入 pdf 載入器
# from langchain.document_loaders import PyPDFLoader #! 已棄用
from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter #! 已棄用
from langchain_text_splitters import RecursiveCharacterTextSplitter

# https://python.langchain.com/docs/versions/v0_2/deprecations/

# from langchain_ollama import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
print("[1] hello.")
# import chromadb

# 使用 ollama 的 embedding 模型
embeddings_model = OllamaEmbeddings(model="llama3.1:8b")



# ***********************
# 載入 PDF 文件
loader = PyPDFLoader('./data/PDF_file.pdf')
docs = loader.load_and_split()

print("[2] hello.")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
documents = text_splitter.split_documents(docs)

print("[3] hello.")

db = Chroma.from_documents(
    documents,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db"
)
print("[4] hello.")

retriever = db.as_retriever()
query = "小王子"
docs = retriever.get_relevant_documents(query)
print("[5] hello.")

print(docs[0].page_content)

# ***********************
print("[6] hello.")














# 分割文件內容
text_splitter = RecursiveCharacterTextSplitter(
    # set the chunk size
    chunk_size=100, # 每個 chunk 的最大字元數
    chunk_overlap=20, # 每個 chunk 之間的重疊字元數
    length_function=len # 用於計算字元長度的函數，默認為 len
)


# load_and_split 可在加載時提供文本分割器
pages = loader.load_and_split(text_splitter=text_splitter)  




# 將文檔寫入 ChromaDB
vector_store = Chroma.from_documents(
    documents,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)


# # vector_store.persist()


# # # db 即是向量儲存庫，可用於相似度檢索
# # db = Chroma.from_documents(pages, embeddings_model)


# query = "小王子"

# # k=3 表示返回最相似的3個文檔
# results = vector_store.similarity_search(query, k=3)

# print(f"找到 {len(results)} 個相關文檔\n")

# print(f"\n找到 {len(results)} 個相關文檔：\n")
# for i, doc in enumerate(results, 1):
#     print(f"[{i}] {doc.page_content}\n---\n")
