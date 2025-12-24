from dotenv import load_dotenv
import os
load_dotenv()
env = os.getenv("ENVIRONMENT", "development")

if env == "production":
    load_dotenv(".env.production", override=True)
else:
    load_dotenv(".env.development", override=True)
