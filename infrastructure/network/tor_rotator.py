import time
import requests
from stem import Signal
from stem.control import Controller
from domain.interfaces.tor_interface import TorInterface
from shared.config import config
from shared.logger.logging_config import setup_logger


logger = setup_logger(__name__)

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
            response = requests.get(config.URL_IPHAZIP, proxies=self.proxy, timeout=10)
            return response.text.strip()
        except requests.RequestException:
            return ""

    def _send_newnym(self) -> bool:
        """
        Envía una señal NEWNYM al controlador de TOR para solicitar nueva IP.
        Retorna True si se logró, False si falló.
        """
        try:
            logger.info(f"[TOR] Enviando señal NEWNYM al puerto {self.control_port}...")
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()  # Si usas clave: controller.authenticate(password='tu_clave')
                controller.signal(Signal.NEWNYM)
            return True
       
        except Exception as e:
            logger.exception(f"[TOR] Excepción inesperada al enviar NEWNYM: {e}")
        return False

    def rotate_ip(self) -> str:
        original_ip = self.get_current_ip()
        logger.info(f"[TOR] IP original antes de rotar: {original_ip}")
        if not original_ip:
            return ""

        for attempt in range(self.max_retries):
            logger.info(f"[TOR] Enviando señal NEWNYM intento {attempt + 1}")
            self._send_newnym()
            time.sleep(self.wait_time)
            new_ip = self.get_current_ip()
            logger.info(f"[TOR] Nueva IP después de rotar: {new_ip}")
            if new_ip and new_ip != original_ip:
                logger.info(f"[TOR] Rotación exitosa: {original_ip} → {new_ip}")
                return new_ip

        logger.warning("[TOR] No se logró rotar la IP después de los intentos.")
        return original_ip
