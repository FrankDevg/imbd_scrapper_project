import socket
import time
import requests
from stem import Signal
from stem.control import Controller
from domain.interfaces.tor_interface import TorInterface
from shared.config import config
from shared.logger.logging_config import setup_logger
import logging # Importar logging si no está ya

logger = logging.getLogger(__name__)

class TorRotator(TorInterface):
    """
    Implementación de la interfaz TorInterface que permite rotar la IP de salida
    mediante la red TOR usando el puerto de control y el protocolo `stem`.
    """

    def __init__(self):
        """
        Constructor del rotador de IP TOR.
        Lee la configuración desde el objeto 'config' centralizado.
        """
        self.control_port = config.TOR_CONTROL_PORT
        self.wait_time = config.TOR_WAIT_AFTER_ROTATION
        self.max_retries = config.MAX_RETRIES
        self.proxy = config.TOR_PROXY
        self.host = config.TOR_HOST

    def get_current_ip(self) -> str:
        """
        Consulta la IP pública actual a través de la red TOR.
        """
        try:
            response = requests.get(config.URL_IPINFO, proxies=self.proxy, timeout=10)
            response.raise_for_status()
            return response.json().get("ip", "")
        except requests.RequestException as e:
            logger.warning(f"[TOR] No se pudo obtener la IP actual: {e}")
            return ""

    def _send_newnym(self) -> bool:
        """
        Envía una señal NEWNYM al controlador de TOR para solicitar una nueva IP.
        """
        try:
            tor_ip = socket.gethostbyname(self.host)
            logger.info(f"[TOR] Intentando conectar al puerto de control en {self.host} ({tor_ip}:{self.control_port})...")           
         
            # Se especifica la dirección (address) del contenedor de TOR.
            with Controller.from_port(address=tor_ip , port=self.control_port) as controller:
                controller.authenticate()  # Asume que no hay contraseña, como configuramos en Docker.
                controller.signal(Signal.NEWNYM)
            
            return True
        except Exception as e:
            # Captura errores de conexión (ej. Connection refused)
            logger.error(f"[TOR] No se pudo conectar al puerto de control de TOR: {e}", exc_info=False)
            return False

    def rotate_ip(self) -> str:
        """
        Intenta rotar la IP de TOR, reintentando si la nueva IP es la misma que la original.
        """
        original_ip = self.get_current_ip()
        logger.info(f"[TOR] IP original antes de rotar: {original_ip}")
        if not original_ip:
            logger.error("[TOR] No se pudo obtener la IP original. Abortando rotación.")
            return ""

        for attempt in range(self.max_retries):
            logger.info(f"[TOR] Enviando señal NEWNYM (Intento {attempt + 1}/{self.max_retries})")
            if not self._send_newnym():
                # Si no se puede conectar al control port, no tiene sentido seguir intentando.
                return original_ip

            time.sleep(self.wait_time)
            new_ip = self.get_current_ip()
            
            if new_ip and new_ip != original_ip:
                logger.info(f"[TOR] Rotación exitosa: {original_ip} → {new_ip}")
                return new_ip
            else:
                logger.warning(f"[TOR] La IP no cambió. Nueva IP obtenida: {new_ip}")

        logger.warning("[TOR] No se logró rotar la IP después de todos los intentos.")
        return original_ip