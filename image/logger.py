import logging
import logging_loki

LOKI_URL = "http://145.14.158.1:3100"

handler = logging_loki.LokiHandler(
    url=f"{LOKI_URL}/loki/api/v1/push",
    tags={"app": "aki-bot"},
    version="1",
)

logger = logging.getLogger("my-logger")


logger.setLevel(logging.INFO)
logger.addHandler(handler)
