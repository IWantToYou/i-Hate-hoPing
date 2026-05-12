# fusion_engine.py
import json
from datetime import datetime

class FusionEngine:
    def __init__(self, config_path='config.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
            
        self.umbrales = self.config['umbrales']  # {'alto': 170, 'medio': 80}
        self.co2_factor = self.config.get('co2_factor', 0.4)  # kg CO2 por kWh
        
    def decidir_estado(self, ldr_valor: int, brillo_camara: float) -> dict:
        """
        ldr_valor: 0 (LOW=hay luz) o 1 (HIGH=no hay luz)
        brillo_camara: 0-255
        Retorna: dict con estado, alerta, co2_estimado
        """
        resultado = {
            'timestamp': datetime.now().isoformat(),
            'ldr_raw': ldr_valor,
            'camara_brillo': round(brillo_camara, 2) if brillo_camara else None,
        }
        
        # Lógica de fusión
        if ldr_valor == 0:  # LOW = hay luz
            if brillo_camara and brillo_camara > self.umbrales['alto']:
                estado = 'USO_CORRECTO'
                alerta = ('verde', 800, 150)  # color, freq, duration
            elif brillo_camara and brillo_camara >= self.umbrales['medio']:
                estado = 'OPTIMIZABLE'
                alerta = ('amarillo', 1200, 400)
            else:
                # LDR dice luz pero cámara dice oscuridad → caso raro
                estado = 'DESPERDICIO'
                alerta = ('rojo', 2000, 1200)
        else:  # HIGH = no hay luz
            if brillo_camara and brillo_camara < self.umbrales['medio']:
                estado = 'DESPERDICIO'
                alerta = ('rojo', 2000, 1200)
            else:
                # Cámara detecta luz pero LDR no → confianza en cámara
                if brillo_camara and brillo_camara <= self.umbrales['alto']:
                    estado = 'OPTIMIZABLE'
                    alerta = ('amarillo', 1200, 400)
                else:
                    estado = 'USO_CORRECTO'
                    alerta = ('verde', 800, 150)
        
        resultado['estado'] = estado
        resultado['alerta'] = alerta
        
        # Estimación simple de CO2 (ajustar según tu región)
        if brillo_camara is not None:
            resultado['co2_estimado_kg'] = round((255 - brillo_camara) / 255 * 0.0004 * self.co2_factor, 6)
        else:
            resultado['co2_estimado_kg'] = 0
            
        return resultado