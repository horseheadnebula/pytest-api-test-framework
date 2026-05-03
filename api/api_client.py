import logging
import time
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(
        self,
        url: str,
        timeout: tuple[int, int] = (3, 10),
        retries: int = 3,
        backoff_factor: float = 1.0,
    ):
        self.url = url
        self.timeout = timeout
        self.session = requests.Session()

        RETRY_STATUSES = (500, 502, 503, 504)

        retry_strategy = Retry(
            total=retries,  # сколько попыток
            backoff_factor=backoff_factor,  # задержка между повторами
            status_forcelist=RETRY_STATUSES,  # когда делать retry
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _request(self, method: str, path: str, **kwargs):
        full_url = f"{self.url}{path}"
        logger.info("--> %s %s", method, full_url)

        start = time.monotonic()
        response = self.session.request(
            method=method,
            url=full_url,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs,
        )
        elapsed = time.monotonic() - start

        logger.info("<-- %s %s (%.3fs)", response.status_code, full_url, elapsed)
        if not response.ok:
            logger.warning("Response body: %s", response.text[:500])

        return response

    def get(self, path: str, params: Optional[dict] = None):
        return self._request("GET", path, params=params)

    def post(self, path: str, json: dict):
        return self._request("POST", path, json=json)

    def put(self, path: str, json: dict):
        return self._request("PUT", path, json=json)

    def delete(self, path: str):
        return self._request("DELETE", path)
