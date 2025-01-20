from repository import Repository
from variables import POSTGRES_INTERACTIONS_TABLE_NAME
from models import Interaction


class InteractionsRepository(Repository):
    def add(self, interaction: Interaction):
        self.cursor.execute("INSERT INTO %s (user_id, item_id, interaction_type) VALUES (%s, %s, %s)",
                            (POSTGRES_INTERACTIONS_TABLE_NAME, interaction.user_id, interaction.item_id, interaction.interaction_type))
        self.conn.commit()

    def get_by_user_id(self, user_id: str | int):
        self.cursor.execute("SELECT item_id, interaction_type FROM %s WHERE user_id=%s",
                            (POSTGRES_INTERACTIONS_TABLE_NAME, user_id))

        interactions = self.cursor.fetchall()
        return interactions
    