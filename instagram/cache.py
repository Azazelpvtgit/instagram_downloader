import datetime
from pymongo import MongoClient
from config import Config

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB_NAME]
        self.cache = self.db['cache']
        self.users = self.db['users']
        
        # Create TTL index if not exists
        if 'expire_at' not in self.cache.index_information():
            self.cache.create_index("expire_at", expireAfterSeconds=0)

    async def set_cache(self, key, value, expire=None):
        document = {
            '_id': key,
            'value': value,
            'created_at': datetime.datetime.utcnow()
        }
        if expire:
            document['expire_at'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expire)
        
        self.cache.replace_one({'_id': key}, document, upsert=True)

    async def get_cache(self, key):
        doc = self.cache.find_one({'_id': key})
        return doc['value'] if doc else None

    async def delete_cache(self, key):
        self.cache.delete_one({'_id': key})

    async def cache_exists(self, key):
        return self.cache.count_documents({'_id': key}) > 0

    # User management methods
    async def add_user(self, user_id):
        self.users.update_one(
            {'user_id': user_id},
            {'$set': {'user_id': user_id, 'joined_at': datetime.datetime.utcnow()}},
            upsert=True
        )

    async def get_all_users(self):
        return [user['user_id'] for user in self.users.find({})]

    async def user_exists(self, user_id):
        return self.users.count_documents({'user_id': user_id}) > 0

# Singleton instance
mongo_manager = MongoDBManager()
