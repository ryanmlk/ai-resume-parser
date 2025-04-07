import json
from pymongo import MongoClient

def extract_objects(file_path: str):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["jobs_data"]
    collection = db["jobs"]
    # Test the connection
    try:
        client.admin.command('ping')
        print("Connection to MongoDB is successful.")
    except Exception as e:
        print(f"An error occurred: {e}")

    with open(file_path, "r", encoding="utf-8") as f:
        line_count = 0
        fail = 0
        for line_count, line in enumerate(f, start=1):
            try:
                json_object = json.loads(line)
                if '_id' in json_object and '$oid' in json_object['_id']:
                    json_object['_id'] = json_object['_id']['$oid']
                collection.insert_one(json_object)
                print(f"Inserted record {line_count}")
            except Exception as e:
                fail += 1
                print(f"An error occurred at line {line_count}: {e}")
                
    print(f"Total records inserted: {line_count - fail}")
    print(f"Total records failed: {fail}")

    client.close()

file_path = "data/raw/techmap-jobs_us_2023-05-05.json"

extract_objects(file_path)