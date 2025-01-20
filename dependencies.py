from recommender import Recommender
from profile_builder import ProfileBuilder
from embedder import Embedder
from interactions_repository import InteractionsRepository


def get_recommender() -> Recommender:
    return Recommender()


def get_profile_builder() -> ProfileBuilder:
    return ProfileBuilder()


def get_interactions_repository() -> InteractionsRepository:
    return InteractionsRepository()

def get_embedder() -> Embedder:
    return Embedder()