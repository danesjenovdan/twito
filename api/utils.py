import logging
from datetime import datetime
from config import CACHE_CONFIG

logger = logging.getLogger(__name__)


def calculate_date_cache_key(date):
  logger.info(f'Calculating cache key for {date}')
  if datetime.now().date() <= datetime.strptime(date, '%Y-%m-%d').date():
    period = int(int(datetime.strftime(datetime.now(), '%M')) / 15)
    calculated_cache_key = datetime.strftime(datetime.now(), f'%Y-%m-%d %H {period}')
  else:
    calculated_cache_key = date
  logger.info(f'CALCULATED CACHE KEY: {calculated_cache_key}')
  return calculated_cache_key


def get_cache_ttl(date):
    if date.today:
        return 10 * 60
    return CACHE_CONFIG.get('CACHE_DEFAULT_TIMEOUT')
