import json
import requests
import http.client
from urllib.parse import urlparse

from app.interfaces.auth_client import *


class AuthClient(IAuthClient):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def verify(self, token: str, timeout: int) -> str:
        try:
            data = self._verify_requests(token, timeout)
        except:# (requests.Timeout, requests.RequestException):
            # fallback
            data = self._verify_http_client(token, timeout)

        return self._process_response(data)

    # ------------------------
    # PRIMARY: requests
    # ------------------------
    def _verify_requests(self, token: str, timeout: int) -> dict:
        url = f"{self.base_url}/verify"

        response = requests.post(
            url,
            json={"token": token},
            timeout=timeout
        )

        if response.status_code != 200:
            raise AuthServiceError(
                f"Auth service on {url} returned {response.status_code}"
            )

        return response.json()

    # ------------------------
    # FALLBACK: http.client
    # ------------------------
    def _verify_http_client(self, token: str, timeout: int) -> dict:
        parsed = urlparse(self.base_url)

        conn_cls = (
            http.client.HTTPSConnection
            if parsed.scheme == "https"
            else http.client.HTTPConnection
        )

        conn = conn_cls(parsed.netloc, timeout=timeout)

        try:
            payload = json.dumps({"token": token})
            headers = {"Content-Type": "application/json"}

            conn.request("POST", "/auth/verify", body=payload, headers=headers)

            response = conn.getresponse()

            if response.status != 200:
                raise AuthServiceError(
                    f"Auth service returned {response.status}"
                )

            raw = response.read().decode("utf-8")

            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                raise AuthServiceError("Invalid JSON from auth service")

        except TimeoutError:
            raise AuthTimeoutError("Auth service timeout")

        except Exception as e:
            raise AuthServiceError(f"http.client on {self.base_url}/verify fallback failed: {e}")

        finally:
            conn.close()

    # ------------------------
    # COMMON LOGIC
    # ------------------------
    def _process_response(self, data: dict) -> str:
        valid = data.get("valid")
        username = data.get("username")
        detail = data.get("detail")

        if not valid:
            raise InvalidTokenError(detail or "Invalid token")

        if not username:
            raise AuthServiceError("Auth response missing username")

        return username