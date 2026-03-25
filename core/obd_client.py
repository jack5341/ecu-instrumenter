# -*- coding: utf-8 -*-
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
        self._pid_map = self._setup_pid_map()

    def _setup_pid_map(self):
        """
        Map of PID hex -> Parser function
        Each parser function receives the hex values (A, B, C, D) and returns the calculated value.
        """
        def parse_speed(data):
            # A
            return int(data[0], 16)

        def parse_rpm(data):
            # (A * 256 + B) / 4
            a = int(data[0], 16)
            b = int(data[1], 16)
            return ((a * 256.0) + b) / 4.0

        def parse_throttle(data):
            # A * 100 / 255
            return (int(data[0], 16) * 100.0) / 255.0

        def parse_coolant(data):
            # A - 40
            return int(data[0], 16) - 40

        def parse_lambda(data):
            # ((A * 256) + B) / 32768
            a = int(data[0], 16)
            b = int(data[1], 16)
            return ((a * 256.0) + b) / 32768.0

        return {
            "010D": {"attr": "speed", "parser": parse_speed, "expected_len": 1},
            "010C": {"attr": "rpm", "parser": parse_rpm, "expected_len": 2},
            "0111": {"attr": "throttle", "parser": parse_throttle, "expected_len": 1},
            "0105": {"attr": "coolant", "parser": parse_coolant, "expected_len": 1},
            "0144": {"attr": "afr", "parser": lambda d: parse_lambda(d) * 14.7, "expected_len": 2},
        }

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
            cmd_str = cmd + "\r"
            if not isinstance(cmd_str, bytes) and hasattr(cmd_str, 'encode'):
                cmd_bytes = cmd_str.encode('utf-8')
            else:
                cmd_bytes = cmd_str
            
            self._sock.send(cmd_bytes)
            
            data = ""
            while ">" not in data:
                chunk = self._sock.recv(128)
                if not chunk:
                    break
                if isinstance(chunk, bytes) and hasattr(chunk, 'decode'):
                    chunk = chunk.decode('utf-8', errors='ignore')
                data += chunk
            return data.strip()
        except Exception as e:
            return ""

    def _query_pid(self, pid):
        resp = self._send(pid)
        # Expected response format: "41 XX A B ..." (where XX is PID hex)
        target_prefix = "41 " + pid[2:4]
        target_prefix_nodash = "41" + pid[2:4]
        
        if target_prefix in resp or target_prefix_nodash in resp:
            try:
                if target_prefix in resp:
                    part = resp.split(target_prefix + " ")[-1]
                else:
                    part = resp.split(target_prefix_nodash)[-1]
                
                parts = part.strip().split()
                # Also handle missing spaces in some emulators: "410C 0B E8" or "410C0BE8"
                if len(parts) == 1 and len(parts[0]) >= 2:
                    chunks = [parts[0][i:i+2] for i in range(0, len(parts[0]), 2)]
                    parts = chunks
                    
                return parts
            except:
                pass
        return None

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
                for pid, config in self._pid_map.items():
                    data = self._query_pid(pid)
                    if data and len(data) >= config["expected_len"]:
                        try:
                            val = config["parser"](data)
                            setattr(global_state.telemetry, config["attr"], val)
                        except Exception as e:
                            logger.log("warning", "Parse error for {0}: {1}".format(pid, str(e)))
                
                time.sleep(0.1)

        except Exception as e:
            logger.log("error", "Connection failed: " + str(e))
            global_state.connection_status = "failed"
        finally:
            if self._sock: self._sock.close()
            self._sock = None
            if self._running:
                global_state.connection_status = "disconnected"

obd_client = OBDClient()
