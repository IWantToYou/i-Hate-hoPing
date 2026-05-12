from camera_handler import CameraHandler

print("🔍 Probando cámara...")
cam = CameraHandler()

if cam.open_camera():
    print("✅ Cámara conectada")
    brightness = cam.get_brightness()
    if brightness is not None:
        print(f"💡 Brillo detectado: {brightness:.2f}/255")
    else:
        print("⚠️ No se pudo leer el brillo")
    cam.release()
else:
    print("❌ No se pudo conectar la cámara")
    print("💡 Prueba cambiando 'index' en config.json a 1, 2, o 3")