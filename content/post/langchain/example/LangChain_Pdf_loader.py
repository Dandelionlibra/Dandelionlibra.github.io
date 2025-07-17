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
# from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 使用 ollama 的模型
# llm_model = OllamaLLM(
#     base_url='http://dandelion-ollama-1:11434', 
#     model="llama3.1:8b"
# )

# 使用 ollama 的 embedding 模型
embeddings_model = OllamaEmbeddings(
    base_url='http://dandelion-ollama-1:11434', 
    model="bge-m3:567m",
    # model="snowflake-arctic-embed:335m",
    # model="nomic-embed-text"
)

'''
nomic-embed-text
"name": "snowflake-arctic-embed:137m",
"name": "snowflake-arctic-embed:335m",
bge-m3:567m
'''


# ***********************
# 載入 PDF 文件
loader = PyPDFLoader('./data/PDF_file.pdf')
docs = loader.load_and_split()

chunk_size = 256
chunk_overlap = 128

text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
documents = text_splitter.split_documents(docs)

# 將文檔寫入 ChromaDB
db = Chroma.from_documents(
    documents,
    embedding=embeddings_model,
    persist_directory="./bge-m3-db" # bge-m3:567m
)


retriever = db.as_retriever()
# query = "小王子"
# query = "狐狸"
# query = "玫瑰花"
query = "羊"
print("--------------------")
print("embeddings_model:", embeddings_model.model)
print(f"chunk_size: {chunk_size}\nchunk_overlap: {chunk_overlap}")
print(f"載入總頁數: {len(docs)}")
print(f"分割後的段落數量: {len(documents)}")
print("query:", query)
print("--------------------")

# k=3 表示返回最相似的3個文檔
# results = db.similarity_search(query,k = 3)
# results = db.similarity_search(query)
results = db.similarity_search_with_score(query)
# print("相似度：", results)

print(f"找到 {len(results)} 個相關文檔\n")

for i, (doc, score) in enumerate(results, 1):
    print(f"[{i}] score: {score:.4f}")
    similarity = 1 - score
    print(f"[{i}] similarity: {similarity*100:.2f}%")
    print(f"content: {doc.page_content}")
    print("---")

# for c, r in enumerate(results, 1):
#     print(f"[{c}] {r.page_content}\n---\n")
#     c = c +1

# print("--------------------------------------------------")
# # The method `BaseRetriever.get_relevant_documents` was deprecated in 
# # langchain-core 0.1.46 and will be removed in 1.0. Use :meth:`~invoke` instead.
# # results_2 = retriever.get_relevant_documents(query)
# results_2 = retriever.invoke(query)

# print(f"\n找到 {len(results_2)} 個相關文檔：\n")
# for c, r in enumerate(results_2, 1):
#     print(f"[{c}] {r.page_content}\n---\n")
#     c = c +1



print("---------------------------------------------")
vector = embeddings_model.embed_query(query)

print("Embedding 向量, 前5維：", vector[:5])
print("向量長度：", len(vector))
