import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import AzureSearch
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Set your Azure OpenAI and Cognitive Search credentials
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://your-azure-openai-resource.openai.azure.com"
os.environ["OPENAI_API_KEY"] = "your-azure-openai-api-key"

AZURE_COGNITIVE_SEARCH_SERVICE_NAME = "your-search-service-name"
AZURE_COGNITIVE_SEARCH_INDEX_NAME = "your-search-index-name"
AZURE_COGNITIVE_SEARCH_API_KEY = "your-search-api-key"

# Initialize OpenAI embedding model
embeddings = OpenAIEmbeddings(deployment="your-embedding-deployment", chunk_size=1)

# Initialize Azure Cognitive Search as vector store
vector_store = AzureSearch(
    azure_search_endpoint=f"https://{AZURE_COGNITIVE_SEARCH_SERVICE_NAME}.search.windows.net",
    azure_search_key=AZURE_COGNITIVE_SEARCH_API_KEY,
    index_name=AZURE_COGNITIVE_SEARCH_INDEX_NAME,
    embedding_function=embeddings.embed_query,
)

# Initialize Azure OpenAI chat model
llm = AzureChatOpenAI(deployment_name="your-chat-deployment", temperature=0)

# Set up memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the conversational chain
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vector_store.as_retriever(),
    memory=memory
)

# Chat function
def chat(query: str):
    result = qa({"question": query})
    return result["answer"]

# Example usage
if __name__ == "__main__":
    print("RAG Chatbot initialized. Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        response = chat(user_input)
        print(f"Chatbot: {response}")
