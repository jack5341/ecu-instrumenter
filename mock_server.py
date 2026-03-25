import socket
import threading
import time
import math

class WavingEmulator:
    def __init__(self, port=35000):
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.t = 0
        
    def start(self):
        self.server.bind(("127.0.0.1", self.port))
        self.server.listen(1)
        print("Waving Emulator running on 127.0.0.1:35000")
        
        while True:
            conn, addr = self.server.accept()
            print("Client connected:", addr)
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        try:
            while True:
                data = conn.recv(1024)
                if not data: break
                
                cmd = data.decode('utf-8').strip()
                resp = ""
                
                # Update time for waving
                self.t += 0.2
                rpm = int(3000 + math.sin(self.t) * 1500)
                speed = int(60 + math.sin(self.t * 0.5) * 40)
                throttle = int(50 + math.sin(self.t * 1.5) * 40)
                coolant = int(100 + math.sin(self.t * 0.3) * 10) # 60 to 110 real temp
                ambient = coolant + 40 # to reach 100 in hex
                
                if cmd == "ATZ" or cmd == "ATE0":
                    resp = "OK"
                elif cmd == "010C":
                    val = rpm * 4
                    resp = "41 0C {:02X} {:02X}".format((val >> 8) & 0xFF, val & 0xFF)
                elif cmd == "010D":
                    resp = "41 0D {:02X}".format(speed)
                elif cmd == "0111":
                    thr_hex = int(throttle * 255 / 100)
                    resp = "41 11 {:02X}".format(thr_hex)
                elif cmd == "0105":
                    resp = "41 05 {:02X}".format(ambient)
                elif cmd == "0144":
                    lam = 1.0 + math.sin(self.t * 0.8) * 0.15
                    val = int(lam * 32768)
                    resp = "41 44 {:02X} {:02X}".format((val >> 8) & 0xFF, val & 0xFF)
                elif cmd == "":
                    continue
                else:
                    resp = "NO DATA"
                
                conn.send((resp + "\r\n>").encode('utf-8'))
        except Exception as e:
            print("Dropped:", e)
        finally:
            conn.close()

if __name__ == "__main__":
    WavingEmulator().start()
