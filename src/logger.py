import logging
import os
from datetime import datetime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

today = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%H-%M-%S")

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs", today)
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOGS_DIR, f"{timestamp}.log")

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s",
)