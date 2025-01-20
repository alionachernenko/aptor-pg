from repository import Repository
from variables import POSTGRES_ITEMS_TABLE_NAME


class ItemsRepository(Repository):
    def get_all(self):
        self.cursor.execute("SELECT * FROM %s", (POSTGRES_ITEMS_TABLE_NAME))
        items = self.cursor.fetchall()
        return items
