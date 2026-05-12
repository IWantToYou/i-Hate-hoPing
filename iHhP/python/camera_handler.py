# camera_handler.py
import cv2
import json
import numpy as np

class CameraHandler:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.camera_index = self.config['camera']['index']
        self.cap = None

    def open_camera(self):
        """Abre la cámara y verifica si está lista"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if self.cap.isOpened():
                print(f"✅ Cámara conectada (Índice: {self.camera_index})")
                return True
            else:
                print(f"❌ No se pudo abrir la cámara en índice {self.camera_index}")
                return False
        except Exception as e:
            print(f"❌ Error al inicializar cámara: {e}")
            return False

    def get_brightness(self):
        """Lee frames hasta obtener uno válido y devuelve el brillo promedio (0-255)"""
        if not self.cap or not self.cap.isOpened():
            return None
            
        # A veces el primer frame es negro, leemos un par para asegurar
        for _ in range(3):
            ret, frame = self.cap.read()
            if not ret:
                continue  # Si falla, intenta de nuevo
                
            # Si llegamos aquí, tenemos frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            return brightness
            
        return None  # Si falló 3 veces seguidas

    def release(self):
        """Libera la cámara correctamente"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
            print("📷 Cámara desconectada correctamente.")