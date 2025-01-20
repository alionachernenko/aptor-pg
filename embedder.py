from variables import POSTGRES_PRIMARY_KEY_NAME
from vstores import items_vstore
from langchain_core.documents import Document
from datetime import datetime
from items_repository import ItemsRepository
import json
from loaders import get_items_vstore_loader


class Embedder:
    def __init__(self):
        self.items_repository = ItemsRepository()

    def create_items_embeddings(self):
        items = self.items_repository.get_all()

        docs = []
        ids = []
        for item in items:
            for key, value in item.items():
                if isinstance(value, datetime):
                    item[key] = value.isoformat()

            item_dict = dict(item)
            item_dict.pop(POSTGRES_PRIMARY_KEY_NAME)

            feature_text = self.prepare_features(item_dict)

            doc = Document(page_content=feature_text, metadata=dict(item))
            docs.append(doc)
            ids.append(item[POSTGRES_PRIMARY_KEY_NAME])
        items_vstore.add_documents(docs, ids=ids)

    def prepare_features(self, lead: dict) -> str:
        features = []
        for key, value in lead.items():
            if key is isinstance(value, (list, tuple)):
                formatted_value = ', '.join(str(v) for v in value)
            elif key is isinstance(value, str) and value.startswith('['):
                try:
                    import json
                    parsed_value = json.loads(value)
                    formatted_value = ', '.join(
                        str(v) for v in parsed_value)
                except json.JSONDecodeError:
                    formatted_value = value
            else:
                formatted_value = str(value)

            features.append(
                f"{key.replace('_', ' ').title()}: {formatted_value}")

        return ' '.join(features)

    def retrieve_item_embeddings_batch(item_ids: list[str | int], batch_size: int = 100):
        embeddings_dict = {}
        for i in range(0, len(item_ids), batch_size):
            batch = item_ids[i:i + batch_size]
            items_vstore_loader = get_items_vstore_loader(
                filter_criteria={"_id": {"$in": batch}})
            items_embeddings = items_vstore_loader.load()

            for item in items_embeddings:
                vector = json.loads(item.page_content)["$vector"]
                item_id = json.loads(item.page_content)["_id"]
                embeddings_dict[item_id] = vector

        return embeddings_dict
