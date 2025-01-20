from vstores import items_vstore
from profile_builder import ProfileBuilder


class Recommender:
    def __init__(self):
        self.profile_builder = ProfileBuilder()

    def get_recommendations(self, user_id: int | str):
        user_profile = self.profile_builder.build_user_profile(user_id)
        if user_profile is None:
            return []

        recommendations = items_vstore.similarity_search_with_score_by_vector(
            embedding=user_profile)
        if not recommendations:
            return []
        return recommendations
