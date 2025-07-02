import logging
import sys

# Create a logger
logger = logging.getLogger("rag_app")
logger.setLevel(logging.INFO)

# Create a handler and set the format
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
