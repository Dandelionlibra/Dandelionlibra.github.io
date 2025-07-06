from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.1:8b")

# response = llm.invoke("幫我取一個文雅的中國男孩名")
response = llm.invoke("幫我取一個文雅的中國男孩名", options={"temperature": 0})
print(response)