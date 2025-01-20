from langchain_astradb import AstraDBVectorStore
from variables import ASTRA_DB_API_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN, ASTRA_DB_VSTORE_USER_PROFILES_COLLECTION_NAME
from langchain_huggingface import HuggingFaceEmbeddings
import weights
from langchain_core.documents import Document
import numpy as np
from interactions_repository import InteractionsRepository
from embedder import Embedder


class ProfileBuilder:
    def __init__(self):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vstore = AstraDBVectorStore(embedding=embeddings, collection_name=ASTRA_DB_VSTORE_USER_PROFILES_COLLECTION_NAME,
                                         token=ASTRA_DB_APPLICATION_TOKEN, api_endpoint=ASTRA_DB_API_ENDPOINT, namespace=None)

        self.interactions_repository = InteractionsRepository()
        self.embedder = Embedder()

    def build_user_profile(self, user_id: str | int):
        interactions = self.interactions_repository.get_by_user_id(user_id)

        item_ids = [interaction["item_id"] for interaction in interactions]

        embeddings_dict = self.embedder.retrieve_item_embeddings_batch(
            item_ids)

        accumulated_vector = None
        total_weight = 0

        for interaction in interactions:
            weight = weights.get(interaction["interaction_type"], 0)
            embedding = embeddings_dict.get(interaction["item_id"])

            if embedding:
                embedding_array = np.array(embedding)
                if accumulated_vector is None:
                    accumulated_vector = weight * embedding_array
                else:
                    accumulated_vector += weight * embedding_array
                total_weight += weight

        if accumulated_vector is not None and total_weight > 0:
            user_profile = user_profile / \
                np.linalg.norm(accumulated_vector / total_weight)
            doc = Document(page_content=f"user {user_id} profile", metadata={
                "user_id": str(user_id)}, embedding=user_profile.tolist())
            self.vstore.add_documents([doc], ids=[user_id])
            return user_profile.tolist()

        return None
