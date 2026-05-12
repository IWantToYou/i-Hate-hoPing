# serial_handler.py
import serial
import json
import time

class SerialHandler:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.port = self.config['serial']['port']
        self.baudrate = self.config['serial']['baudrate']
        self.timeout = self.config['serial']['timeout']
        self.arduino = None

    def connect(self):
        try:
            self.arduino = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Tiempo de estabilización del puerto
            print(f"✅ Conectado a Arduino en {self.port}")
            return True
        except serial.SerialException as e:
            print(f" Error al conectar con Arduino: {e}")
            print("💡 Verifica que COM3 no esté en uso por Arduino IDE o Serial Monitor.")
            return False

    def read_ldr_state(self):
        """Lee una línea del serial y devuelve 0 (hay luz) o 1 (no hay luz)"""
        if not self.arduino or not self.arduino.is_open:
            if not self.connect():
                return None
                
        try:
            line = self.arduino.readline().decode('utf-8').strip()
            if not line:
                return None
                
            # Mapeo robusto: acepta el texto que imprime tu Arduino o un 0/1 directo
            if 'USO CORRECTO' in line or line == '0':
                return 0  # LOW = hay luz (lógica invertida del módulo)
            elif 'DESPERDICIO' in line or line == '1':
                return 1  # HIGH = no hay luz
            return None
        except Exception as e:
            print(f"⚠️ Error leyendo serial: {e}")
            return None

    def close(self):
        if self.arduino and self.arduino.is_open:
            self.arduino.close()
            print(" Conexión serial cerrada correctamente.")