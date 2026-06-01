import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests

from bot.logging_config import setup_logger

TESTNET_BASE_URL = "https://testnet.binancefuture.com"

logger = setup_logger()


class BinanceClientError(Exception):
    pass


class BinanceClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = TESTNET_BASE_URL):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        signed_params = self._sign(params)

        logger.debug(f"POST {url} | params: { {k: v for k, v in signed_params.items() if k != 'signature'} }")

        try:
            response = self.session.post(url, data=signed_params, timeout=10)
            logger.debug(f"Response [{response.status_code}]: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network error connecting to {url}: {e}")
            raise BinanceClientError(f"Network error: {e}")
        except requests.exceptions.Timeout:
            logger.error(f"Request to {url} timed out.")
            raise BinanceClientError("Request timed out. Check your internet connection.")
        except requests.exceptions.HTTPError as e:
            try:
                err_data = response.json()
                msg = err_data.get("msg", str(e))
                code = err_data.get("code", "unknown")
                logger.error(f"API error {code}: {msg}")
                raise BinanceClientError(f"API error [{code}]: {msg}")
            except Exception:
                logger.error(f"HTTP error: {e}")
                raise BinanceClientError(f"HTTP error: {e}")

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        time_in_force: str = "GTC",
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force

        return self._post("/fapi/v1/order", params)
