import pymongo
from pymongo.errors import ServerSelectionTimeoutError

""" Expects hash value, frame number and Video name/Path from hash function"""


def connect_to_mongo_server():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        return client
    except ServerSelectionTimeoutError as e:
        print(f"Error connecting to MongoDB: {e}")


def store_video_data(col, records):

    x = col.insert_many(records)

    # create index on hash field
    col.create_index([("hash", pymongo.ASCENDING)], unique=True)


def find_by_hash(col, hash_value):
    # Perform a covered query
    result = col.find({"hash": hash_value}, {"_id": 0, "hash": 1, "frame_number": 1, "video_path": 1})

    # Get frame number and path
    result_pair = [(int(record['frame_number']), str(record['video_path'])) for record in result]

    for fn, path in result_pair:
        frame_number = fn
        video_path = path

    return frame_number, video_path


client = connect_to_mongo_server()

# Create or access DB and collection if it exists
db = client["VideoDB"]
col = db["VideoCollection"]

# Data from hash function
record1 = {"hash": "16d5030d7223545e8181f50ea4ccc4a833bf64026275bb71247efe5b296028e3",
           "frame_number": 2, "video_path": "/usr/local/video1"}

record2 = {"hash": "16d5030d7223545e8181f50ea4ccc4a833bf64026275bb71247efe5b296028e5",
           "frame_number": 3, "video_path": "/usr/local/video1"}

records = [record1, record2]


# store once
store_video_data(col, records)

# Search by index
frame_number, video_path = find_by_hash(col, "16d5030d7223545e8181f50ea4ccc4a833bf64026275bb71247efe5b296028e3")

print(frame_number)

frame_rate = 30
time = frame_number/frame_rate

print(time)

client.close()