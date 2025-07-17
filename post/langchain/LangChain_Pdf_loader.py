


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
# The method `BaseRetriever.get_relevant_documents` was deprecated in langchain-core 0.1.46 and will be removed in 1.0. Use :meth:`~invoke` instead.
# docs = retriever.get_relevant_documents(query)
docs = retriever.invoke(query)
print("[5] hello.")

print(docs[0].page_content)

# ***********************
print("[6] hello.")




'''


'''