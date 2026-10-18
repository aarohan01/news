
## Structure Basic ##
NEWS -> The main folder containing utils and generic files and environment
APP -> contains all app related in one place, FastAPI convention is to include even main/crud.py here
DB -> contains database

## Struture Split ##
Fetching -> clients 
Processing -> services ----> this is the main part it calls both repo and clients
Storing/Retrieving/DB related -> repositories

## Structure ##
news/                              # Main Folder
├── app/                           # Every file related to running the app
│   ├── clients/                   # Clients and functions to fetch
│   ├── models/                    # DB models
│   ├── repositories/              # DB related i.e. storing, retrieving 
│   ├── schemas/                   # Pydantic models
│   ├── services/                  # Processing data
│   ├── database.py                # Dataabase core handling i.e. sessions, connections and Base
│   ├── dependencies.py            # Dependency mapping, context managed for FastAPI
│   ├── utils.py                   # Misc utils
│   └── main.py                    # Routes/CRUD
├── db/                            # DB storage file
└──  scripts/                      # Manual Scripts                  



### Remaining ###
# Tests
# Migration 
# Error handling
# env file




