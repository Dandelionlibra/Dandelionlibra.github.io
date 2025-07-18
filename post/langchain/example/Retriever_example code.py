''' Relevant Dependencies Version
langchain                 0.3.26
langchain-community       0.3.27
langchain-core            0.3.69
langchain-ollama          0.3.4
langchain-text-splitters  0.3.8
langgraph                 0.5.3
langgraph-checkpoint      2.1.0
langgraph-prebuilt        0.5.2
langgraph-sdk             0.1.73
numexpr                   2.11.0
ollama                    0.5.1
'''
# https://python.langchain.com/docs/versions/v0_2/deprecations/
# 從 langchain 引入 pdf 載入器
# from langchain.document_loaders import PyPDFLoader #! 已棄用
from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter #! 已棄用
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 使用 ollama 的 embedding 模型
# embeddings_model = OllamaEmbeddings(model="llama3.1:8b")
embeddings_model = OllamaEmbeddings(base_url='http://dandelion-ollama-1:11434', model="llama3.1:8b")

# ***********************
# 載入 PDF 文件
loader = PyPDFLoader('./data/PDF_file.pdf')
docs = loader.load_and_split()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
documents = text_splitter.split_documents(docs)

# 將文檔寫入 ChromaDB
db = Chroma.from_documents(
    documents,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db"
)

retriever = db.as_retriever()
query = "小王子"
print("--------")
print("query: ", query)
print("--------")

# k=3 表示返回最相似的3個文檔
# results = db.similarity_search(query,k = 3)
results = db.similarity_search(query)

print(f"找到 {len(results)} 個相關文檔\n")

c = 1;
for r in results:
    print(f"[{c}] {r.page_content}\n---\n")
    c = c +1
    
print("--------------------------------------------------")
# The method `BaseRetriever.get_relevant_documents` was deprecated in 
# langchain-core 0.1.46 and will be removed in 1.0. Use :meth:`~invoke` instead.
# results_2 = retriever.get_relevant_documents(query)
results_2 = retriever.invoke(query)

print(f"\n找到 {len(results_2)} 個相關文檔：\n")
c = 1;
for r in results_2:
    print(f"[{c}] {r.page_content}\n---\n")
    c = c +1

