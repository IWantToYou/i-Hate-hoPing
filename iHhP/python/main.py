# main.py
import sys
import time
import winsound
import csv
import os
from serial_handler import SerialHandler
from camera_handler import CameraHandler
from fusion_engine import FusionEngine

def reproducir_alerta_solo_desperdicio():
    """Solo reproduce beep cuando hay DESPERDICIO real"""
    try:
        # Beep largo y molesto SOLO para desperdicio
        winsound.Beep(2000, 1200)  # 2000Hz, 1.2 segundos
    except Exception as e:
        print(f"⚠️ Error reproduciendo sonido: {e}")

def guardar_csv(datos, csv_path='../data/datos_luz.csv'):
    """Guarda datos en CSV"""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=datos.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(datos)

def main():
    print("🌱 Iniciando i Hate HoPiNg - Sistema de Optimización Energética")
    print("=" * 70)
    
    # Inicializar componentes
    serial = SerialHandler()
    camara = CameraHandler()
    fusion = FusionEngine()
    
    # Conectar Arduino
    if not serial.connect():
        print("❌ No se pudo conectar al Arduino. Saliendo...")
        return
    
    # Conectar cámara
    if not camara.open_camera():
        print("⚠️ No se pudo conectar la cámara, pero continuando solo con LDR...")
    
    print("\n🎯 Sistema listo.")
    print("🔕 Solo sonará alerta cuando haya DESPERDICIO (brillo < 80)")
    print("Presiona Ctrl+C para detener.\n")
    
    try:
        while True:
            # Leer LDR
            ldr_valor = serial.read_ldr_state()
            
            # Leer cámara
            brillo = camara.get_brightness()
            
            if ldr_valor is None:
                print("⏳ Esperando datos del LDR...")
                time.sleep(0.5)
                continue
            
            # Decidir estado
            resultado = fusion.decidir_estado(ldr_valor, brillo)
            
            # Mostrar resultado
            estado = resultado['estado']
            emoji = "✅" if estado == "USO_CORRECTO" else "⚠️" if estado == "OPTIMIZABLE" else "❌"
            
            print(f"{emoji} {estado}")
            print(f"   LDR: {ldr_valor} ({'LUZ' if ldr_valor == 0 else 'OSCURIDAD'})")
            print(f"   Brillo cámara: {brillo:.2f}/255" if brillo else "   Brillo cámara: N/A")
            print(f"   CO₂ estimado: {resultado['co2_estimado_kg']:.6f} kg")
            
            # SOLO hacer beep si es DESPERDICIO (valor muy bajo = problema)
            if estado == "DESPERDICIO":
                print("   🔊 ALERTA: Desperdicio energético detectado!")
                reproducir_alerta_solo_desperdicio()
            else:
                print("   🔕 Sin alerta (rango normal)")
            
            print("-" * 70)
            
            # Guardar en CSV
            guardar_csv(resultado)
            
            # Esperar
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n\n👋 Deteniendo sistema...")
    finally:
        serial.close()
        camara.release()
        print("✅ Sistema cerrado correctamente.")

if __name__ == "__main__":
    main()