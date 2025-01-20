from embedder import Embedder
from profile_builder import ProfileBuilder


def update_embeddings_job():
    embedder = Embedder()
    profile_builder = ProfileBuilder()
    profile_builder.build_user_profile()
    embedder.create_items_embeddings()
