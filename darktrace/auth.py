import hmac
import hashlib
from datetime import datetime, timezone
from typing import Dict

class DarktraceAuth:
    def __init__(self, public_token: str, private_token: str):
        self.public_token = public_token
        self.private_token = private_token

    def get_headers(self, request_path: str) -> Dict[str, str]:
        date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        signature = self.generate_signature(request_path, date)
        return {
            'DTAPI-Token': self.public_token,
            'DTAPI-Date': date,
            'DTAPI-Signature': signature,
            'Content-Type': 'application/json',
        }

    def generate_signature(self, request_path: str, date: str) -> str:
        message = f"{request_path}\n{self.public_token}\n{date}"
        signature = hmac.new(
            self.private_token.encode('ASCII'),
            message.encode('ASCII'),
            hashlib.sha1
        ).hexdigest()
        return signature 