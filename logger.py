import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, format='{time:HH:mm} | <lvl>f</lvl> ', level='INFO')

logger = logger.

print(logger)