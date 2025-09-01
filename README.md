# MCP
Creating a MCP server
# Secure Mongo MCP Server

This is a secure MongoDB MCP (Model Context Protocol) server that allows querying MongoDB with API key authentication.

## Features
- API key authentication
- List collections in allowed databases
- Find documents with filters and limits
- Configurable MongoDB URI, database, and limits

## Requirements
- Python 3.9+
- MongoDB running locally or remotely

## Installation
```bash
git clone https://github.com/<your-username>/secure-mongo-mcp-server.git
cd secure-mongo-mcp-server
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

