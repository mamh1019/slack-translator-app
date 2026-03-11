from dotenv import load_dotenv
import os
import redis

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(override=True, verbose=True, dotenv_path=dotenv_path)

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
redis_client.lpush("slack_translator_worker_push", "test")
