import time
import requests
from stem import Signal
from stem.control import Controller
from domain.interfaces.tor_interface import TorInterface
from shared.config import config

class TorRotator(TorInterface):
    """
    Implementación de la interfaz TorInterface que permite rotar la IP de salida
    mediante la red TOR usando el puerto de control y el protocolo `stem`.

    Utiliza el proxy definido en la configuración y hace control activo sobre la identidad TOR.
    """

    def __init__(self, control_port=9051, wait_time=10, max_retries=3):
        """
        Constructor del rotador de IP TOR.

        Args:
            control_port (int): Puerto de control de TOR (por defecto 9051).
            wait_time (int): Tiempo de espera entre intentos de rotación (en segundos).
            max_retries (int): Número máximo de intentos para obtener una IP distinta.
        """
        self.control_port = control_port
        self.wait_time = wait_time
        self.max_retries = max_retries
        self.proxy = config.TOR_PROXY

    def get_current_ip(self) -> str:
        """
        Consulta la IP pública actual a través de la red TOR.

        Returns:
            str: IP pública actual como string. Retorna cadena vacía si falla.
        """
        try:
            response = requests.get("http://icanhazip.com", proxies=self.proxy, timeout=10)
            return response.text.strip()
        except requests.RequestException:
            return ""

    def _send_newnym(self):
        """
        Envía una señal NEWNYM al controlador de TOR para solicitar una nueva identidad (rotar IP).
        """
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

    def rotate_ip(self) -> str:
        """
        Rota la IP actual mediante la red TOR. Intenta obtener una IP distinta de la actual,
        hasta un número máximo de reintentos con pausas entre cada uno.

        Returns:
            str: Nueva IP pública si fue posible rotar, o la IP original si no hubo cambio.
        """
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
