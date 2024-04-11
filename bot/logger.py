import logging
import logging_loki
from config import LOKI_URL

handler = logging_loki.LokiHandler(
    url=f"{LOKI_URL}/loki/api/v1/push",
    tags={"app": "aki-bot-core"},
    version="1",
)

logger = logging.getLogger("my-logger")


logger.setLevel(logging.INFO)
logger.addHandler(handler)
