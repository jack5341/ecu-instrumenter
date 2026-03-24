import socket
import threading
import time
from core.logger import logger
from core.state import global_state

class OBDClient:
    def __init__(self):
        self._thread = None
        self._running = False
        self._sock = None

    def start(self, ip, port):
        self.stop()
        self._running = True
        self._thread = threading.Thread(target=self._run, args=(ip, port))
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except:
                pass
        if self._thread:
            self._thread.join(1.0)
            self._thread = None

    def _send(self, cmd):
        if not self._sock: return ""
        try:
            self._sock.send(cmd + "\r")
            data = ""
            while ">" not in data:
                chunk = self._sock.recv(128)
                if not chunk:
                    break
                data += chunk
            return data.strip()
        except:
            return ""

    def _run(self, ip, port):
        global_state.connection_status = "connecting"
        msg = "Connecting to {0}:{1}...".format(ip, port)
        logger.log("connection", msg)
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.settimeout(5.0)
            self._sock.connect((ip, port))
            self._sock.settimeout(2.0)
            logger.log("connection", "Connected.")
            global_state.connection_status = "connected"

            self._send("ATZ")
            self._send("ATE0")

            while self._running:
                # Mock polling
                time.sleep(1.0)

        except Exception as e:
            logger.log("error", "Connection failed: " + str(e))
            global_state.connection_status = "failed"
        finally:
            if self._sock: self._sock.close()
            self._sock = None
            if self._running:
                global_state.connection_status = "disconnected"

obd_client = OBDClient()
