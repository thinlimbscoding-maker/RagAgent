import logging

# Configure how logs look and where they go
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],  # Prints to console
)

# This is your root logger instance
logger = logging.getLogger("my_project")
