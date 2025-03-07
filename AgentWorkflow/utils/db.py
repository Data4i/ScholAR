from langchain_community.utilities import SQLDatabase
from decouple import config

# Get your database URI from environment variables (or .env)
DB_URI = config('DB_URI')
db = SQLDatabase.from_uri(DB_URI)

