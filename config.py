import pymongo, json
from bson import ObjectId

# connection string
# mongo_url = "mongodb+srv://.........."
# FREE SERVICE: mongodb.net
mongo_url = "mongodb://localhost:27017"

client = pymongo.MongoClient(mongo_url)
# db points to the actual data base
db = client.get_database("microSolder")


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)

        return json.JSONEncoder.default(self, o)


def parse_json(data):
    return JSONEncoder().encode(data)