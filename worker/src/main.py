from dotenv import load_dotenv
import os
import traceback
from libs.logger import Logger

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(current_dir, ".env")
load_dotenv(override=True, verbose=True, dotenv_path=dotenv_path)

from worker import SlackTranslatorWorker

try:
    Logger.log("info", "start server")
    SlackTranslatorWorker().run()

except Exception as e:
    response_message = {
        "traceback": str(traceback.format_exc()),
    }
    print(response_message)
