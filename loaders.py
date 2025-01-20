from langchain_astradb import AstraDBLoader
from variables import ASTRA_DB_API_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_VSTORE_ITEMS_COLLECTION_NAME

items_embeddings_loader = AstraDBLoader(collection_name=ASTRA_DB_VSTORE_ITEMS_COLLECTION_NAME,
                                        token=ASTRA_DB_APPLICATION_TOKEN, api_endpoint=ASTRA_DB_API_ENDPOINT, namespace=None)


def get_items_vstore_loader(filter_criteria):
    items_embeddings_loader = AstraDBLoader(collection_name=ASTRA_DB_VSTORE_ITEMS_COLLECTION_NAME, token=ASTRA_DB_APPLICATION_TOKEN,
                                            api_endpoint=ASTRA_DB_API_ENDPOINT, namespace=None, filter_criteria=filter_criteria)
    return items_embeddings_loader
