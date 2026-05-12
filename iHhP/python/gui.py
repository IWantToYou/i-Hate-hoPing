# gui.py
import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
from serial_handler import SerialHandler
from camera_handler import CameraHandler
from fusion_engine import FusionEngine

class IHateHoPiNgGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 i Hate HoPiNg - Sistema de Optimización Energética")
        self.root.geometry("800x600")
        self.root.configure(bg='#1e1e1e')
        
        # Variables de control
        self.ejecutando = False
        self.hilo_ejecucion = None
        
        # Inicializar componentes
        self.serial = SerialHandler()
        self.camara = CameraHandler()
        self.fusion = FusionEngine()
        
        # Colores
        self.COLOR_FONDO = '#1e1e1e'
        self.COLOR_TEXTO = '#ffffff'
        self.COLOR_VERDE = '#4CAF50'
        self.COLOR_AMARILLO = '#FFC107'
        self.COLOR_ROJO = '#F44336'
        self.COLOR_GRIS = '#424242'
        
        self.crear_widgets()
        
    def crear_widgets(self):
        # Título
        lbl_titulo = tk.Label(
            self.root,
            text="🌱 i Hate HoPiNg",
            font=("Arial", 24, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO
        )
        lbl_titulo.pack(pady=20)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg=self.COLOR_FONDO)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Panel de Estado (grande y central)
        self.frame_estado = tk.Frame(frame_principal, bg=self.COLOR_GRIS, bd=3, relief=tk.RAISED)
        self.frame_estado.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        self.lbl_estado = tk.Label(
            self.frame_estado,
            text="SISTEMA DETENIDO",
            font=("Arial", 32, "bold"),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.lbl_estado.pack(pady=30)
        
        # Valores
        frame_valores = tk.Frame(self.frame_estado, bg=self.COLOR_GRIS)
        frame_valores.pack(pady=20)
        
        self.lbl_ldr = tk.Label(
            frame_valores,
            text="LDR: --",
            font=("Arial", 16),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.lbl_ldr.pack(pady=5)
        
        self.lbl_brillo = tk.Label(
            frame_valores,
            text="Brillo Cámara: -- / 255",
            font=("Arial", 16),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.lbl_brillo.pack(pady=5)
        
        self.lbl_co2 = tk.Label(
            frame_valores,
            text="CO₂ estimado: -- kg",
            font=("Arial", 14),
            bg=self.COLOR_GRIS,
            fg='#BDBDBD'
        )
        self.lbl_co2.pack(pady=5)
        
        # Barra de progreso de brillo
        self.lbl_brillo_barra = tk.Label(
            frame_valores,
            text="[" + " " * 50 + "]",
            font=("Courier", 12),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_VERDE
        )
        self.lbl_brillo_barra.pack(pady=10)
        
        # Botón de control
        self.btn_control = tk.Button(
            frame_principal,
            text="▶ INICIAR SISTEMA",
            font=("Arial", 16, "bold"),
            bg=self.COLOR_VERDE,
            fg="white",
            command=self.toggle_sistema,
            cursor="hand2",
            bd=0,
            padx=30,
            pady=15
        )
        self.btn_control.pack(pady=20)
        
        # Log de lecturas
        frame_log = tk.LabelFrame(
            frame_principal,
            text="📋 Registro de Lecturas",
            font=("Arial", 12, "bold"),
            bg=self.COLOR_FONDO,
            fg=self.COLOR_TEXTO
        )
        frame_log.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        self.txt_log = tk.Text(
            frame_log,
            height=8,
            bg='#2d2d2d',
            fg=self.COLOR_TEXTO,
            font=("Courier", 10),
            bd=0,
            wrap=tk.WORD
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar para el log
        scrollbar = ttk.Scrollbar(self.txt_log, command=self.txt_log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.config(yscrollcommand=scrollbar.set)
        
        # Footer
        lbl_footer = tk.Label(
            self.root,
            text="Python Pro Avanzado · Mayo 2026",
            font=("Arial", 8),
            bg=self.COLOR_FONDO,
            fg='#757575'
        )
        lbl_footer.pack(pady=10)
        
    def toggle_sistema(self):
        if not self.ejecutando:
            self.iniciar_sistema()
        else:
            self.detener_sistema()
            
    def iniciar_sistema(self):
        self.ejecutando = True
        self.btn_control.config(text="⏹ DETENER SISTEMA", bg=self.COLOR_ROJO)
        self.agregar_log("🚀 Sistema iniciado...\n")
        
        # Conectar hardware
        if not self.serial.connect():
            self.agregar_log("❌ Error: No se pudo conectar al Arduino\n")
            self.detener_sistema()
            return
            
        if not self.camara.open_camera():
            self.agregar_log("⚠️ Advertencia: Cámara no disponible\n")
        
        # Iniciar hilo de ejecución
        self.hilo_ejecucion = threading.Thread(target=self.ejecutar_loop, daemon=True)
        self.hilo_ejecucion.start()
        
    def detener_sistema(self):
        self.ejecutando = False
        self.btn_control.config(text="▶ INICIAR SISTEMA", bg=self.COLOR_VERDE)
        self.lbl_estado.config(text="SISTEMA DETENIDO", bg=self.COLOR_GRIS)
        self.agregar_log(" Sistema detenido\n")
        
        if self.serial:
            self.serial.close()
        if self.camara:
            self.camara.release()
            
    def ejecutar_loop(self):
        while self.ejecutando:
            try:
                # Leer LDR
                ldr_valor = self.serial.read_ldr_state()
                
                # Leer cámara
                brillo = self.camara.get_brightness()
                
                if ldr_valor is None:
                    time.sleep(0.5)
                    continue
                
                # Decidir estado
                resultado = self.fusion.decidir_estado(ldr_valor, brillo)
                
                # Actualizar GUI (thread-safe)
                self.root.after(0, self.actualizar_gui, resultado)
                
                time.sleep(1)
                
            except Exception as e:
                self.root.after(0, self.agregar_log, f"❌ Error: {str(e)}\n")
                time.sleep(1)
                
    def actualizar_gui(self, resultado):
        estado = resultado['estado']
        brillo = resultado['camara_brillo']
        ldr = resultado['ldr_raw']
        co2 = resultado['co2_estimado_kg']
        
        # Actualizar estado y colores
        if estado == "USO_CORRECTO":
            color = self.COLOR_VERDE
            emoji = "✅"
        elif estado == "OPTIMIZABLE":
            color = self.COLOR_AMARILLO
            emoji = "⚠️"
        else:  # DESPERDICIO
            color = self.COLOR_ROJO
            emoji = "❌"
        
        self.lbl_estado.config(text=f"{emoji} {estado}", bg=color)
        
        # Actualizar valores
        self.lbl_ldr.config(text=f"LDR: {ldr} ({'LUZ' if ldr == 0 else 'OSCURIDAD'})")
        
        if brillo is not None:
            self.lbl_brillo.config(text=f"Brillo Cámara: {brillo:.2f} / 255")
            self.lbl_co2.config(text=f"CO₂ estimado: {co2:.6f} kg")
            
            # Actualizar barra de progreso
            barra_len = int((brillo / 255) * 50)
            barra = "[" + "█" * barra_len + " " * (50 - barra_len) + "]"
            self.lbl_brillo_barra.config(text=barra, fg=color)
        else:
            self.lbl_brillo.config(text="Brillo Cámara: N/A")
            
        # Agregar al log (solo cada 5 segundos para no saturar)
        if hasattr(self, '_ultimo_log') and (time.time() - self._ultimo_log) > 5:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.agregar_log(f"[{timestamp}] {estado} | LDR:{ldr} | Brillo:{brillo:.1f}\n")
            self._ultimo_log = time.time()
        elif not hasattr(self, '_ultimo_log'):
            self._ultimo_log = time.time()
            
    def agregar_log(self, texto):
        self.txt_log.insert(tk.END, texto)
        self.txt_log.see(tk.END)  # Auto-scroll al final
        
    def on_closing(self):
        if self.ejecutando:
            self.detener_sistema()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = IHateHoPiNgGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()