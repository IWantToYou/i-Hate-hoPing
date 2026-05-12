from serial_handler import SerialHandler

print("🔍 Probando conexión con Arduino...")
handler = SerialHandler()

if handler.connect():
    print("✅ ¡Conexión exitosa! Leyendo datos del LDR...")
    for i in range(5):
        valor = handler.read_ldr_state()
        if valor is not None:
            print(f"  Lectura {i+1}: LDR = {valor} ({'LUZ' if valor == 0 else 'OSCURIDAD'})")
        import time; time.sleep(0.5)
    handler.close()
else:
    print("❌ No se pudo conectar. Verifica COM3 y que el Serial Monitor esté cerrado.")