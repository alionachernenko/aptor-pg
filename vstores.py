from langchain_astradb import AstraDBVectorStore
from variables import ASTRA_DB_API_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_VSTORE_ITEMS_COLLECTION_NAME, ASTRA_DB_VSTORE_USER_PROFILES_COLLECTION_NAME
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
items_vstore = AstraDBVectorStore(embedding=embeddings, collection_name=ASTRA_DB_VSTORE_ITEMS_COLLECTION_NAME, token=ASTRA_DB_APPLICATION_TOKEN, api_endpoint=ASTRA_DB_API_ENDPOINT, namespace=None)
user_profiles_store = AstraDBVectorStore(embedding=embeddings, collection_name=ASTRA_DB_VSTORE_USER_PROFILES_COLLECTION_NAME, token=ASTRA_DB_APPLICATION_TOKEN, api_endpoint=ASTRA_DB_API_ENDPOINT, namespace=None)
