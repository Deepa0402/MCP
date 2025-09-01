import os
import json
from pymongo import MongoClient
from fastmcp import FastMCP

MONGO_URI: str = "mongodb://localhost:27017/"
MONGO_DB: str = "ADM"
API_KEY: str = "ImStrong"

DEFAULT_LIMIT: int = 25
MAX_LIMIT: int = 100
READ_ONLY: bool = True
DB_ALLOWLIST: list[str] = ["ADM"]


# MongoDB client
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]


# MCP Server
server = FastMCP(name="secure-mongo-gate")

# Authentication check
def check_auth(api_key: str) -> None:
    if not api_key or api_key != API_KEY:
        raise PermissionError("Invalid or missing API key.")

# List collections tool
@server.tool()
def list_collections(api_key: str) -> dict:
    """List collections in allowed databases."""
    check_auth(api_key)
    allowed_dbs = DB_ALLOWLIST 
    collections_info: dict[str, list[str]] = {}
    for db_name in allowed_dbs:
        collections_info[db_name] = client[db_name].list_collection_names()
    return {"collections": collections_info}


# Find documents tool
@server.tool()
def find_many(api_key: str, collection: str, filter: str = "{}", limit: int = DEFAULT_LIMIT) -> dict:
    """Find documents in a collection with optional filter."""
    check_auth(api_key)
    limit = min(limit, MAX_LIMIT)
    try:
        filter_dict = json.loads(filter)
    except json.JSONDecodeError:
        filter_dict = {}
    if collection not in db.list_collection_names():
        return {"error": "Collection not found."}
    docs = list(db[collection].find(filter_dict, {"_id": 0}).limit(limit))
    return {"documents": docs}


# Main entry
if __name__ == "__main__":
    print(f"Starting Secure Mongo MCP Server for DB: {MONGO_DB} ...")
    server.run()
