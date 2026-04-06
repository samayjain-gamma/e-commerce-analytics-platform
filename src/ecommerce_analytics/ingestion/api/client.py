import time
from typing import Any, Dict, Optional

import requests

from ecommerce_analytics.common.config import config
from ecommerce_analytics.common.logger import logger


class APIClient:
    def __init__(self, base_url: str, timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    self.base_url, params=params, timeout=self.timeout
                )

                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                logger.error(f"API request failed (attempt {attempt}): {e}")

                if attempt == self.max_retries:
                    raise

                time.sleep(2**attempt)
