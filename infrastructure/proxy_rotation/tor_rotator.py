import time
import requests
from stem import Signal
from stem.control import Controller
from domain.interfaces.tor_interface import TorInterface
from shared.config import config

class TorRotator(TorInterface):
    def __init__(self, control_port=9051, wait_time=10, max_retries=3):
        self.control_port = control_port
        self.wait_time = wait_time
        self.max_retries = max_retries
        self.proxy = config.TOR_PROXY

    def get_current_ip(self) -> str:
        try:
            response = requests.get("http://icanhazip.com", proxies=self.proxy, timeout=10)
            return response.text.strip()
        except requests.RequestException:
            return ""

    def _send_newnym(self):
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def rotate_ip(self) -> str:
        original_ip = self.get_current_ip()
        if not original_ip:
            return ""

        for _ in range(self.max_retries):
            self._send_newnym()
            time.sleep(self.wait_time)
            new_ip = self.get_current_ip()
            if new_ip and new_ip != original_ip:
                return new_ip
        return original_ip
