from variables import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USERNAME, POSTGRES_HOST, POSTGRES_PORT
import psycopg2
from psycopg2.extras import DictCursor


class Repository:
    def __init__(self):
        self.conn = psycopg2.connect(database=POSTGRES_DB, user=POSTGRES_USERNAME,
                                     password=POSTGRES_PASSWORD, host=POSTGRES_HOST, port=POSTGRES_PORT)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
