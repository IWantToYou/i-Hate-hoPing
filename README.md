# i Hate HoPiNg

## 📌 Descripción del Proyecto

**i Hate HoPiNg** es un sistema inteligente de optimización energética doméstica que combina hardware (Arduino), sensores ambientales y análisis de datos en Python para detectar y reducir el desperdicio de energía eléctrica.

El sistema monitorea la iluminación del entorno y la presencia de personas para determinar si existe un uso eficiente de la energía, generando alertas, cálculos de consumo y estimaciones de emisiones de CO₂.

---

## 🎯 Objetivo

Reducir el consumo innecesario de energía eléctrica y fomentar hábitos sostenibles mediante un sistema automatizado capaz de analizar y actuar en tiempo real.

---

## ⚙️ Funcionamiento

El sistema opera en cuatro etapas principales:

1. **Captura de datos**

   * Sensor LDR mide la luz ambiental
   * Cámara detecta presencia humana (OpenCV)

2. **Comunicación**

   * Arduino envía datos al sistema mediante comunicación serial

3. **Procesamiento**

   * Python analiza los datos
   * Determina si hay:

     * Uso correcto
     * Desperdicio energético
     * Estado optimizable

4. **Respuesta**

   * Muestra resultados al usuario
   * Calcula consumo (kWh) y emisiones de CO₂
   * (Opcional) Activa relé o LEDs

---

## 🧩 Componentes

### 🔌 Hardware

* Arduino UNO
* Sensor LDR
* Resistencias (10kΩ y 220Ω)
* LEDs
* Módulo Relé
* Protoboard
* Jumpers

### 🧠 Software

* Python
* OpenCV
* PySerial
* Pandas
* NumPy
* Matplotlib

---

## 📊 Estructura del Proyecto

```
/project
 ├── main.py
 ├── analyzer.py
 ├── serial_handler.py
 ├── data.csv
 └── README.md
```

---

## 📈 Datos y Análisis

El sistema registra información en un archivo CSV con la siguiente estructura:

* Hora
* Nivel de luz
* Presencia
* Estado del sistema
* Consumo energético (kWh)
* Emisiones de CO₂ (g)

Estos datos permiten:

* Analizar patrones de uso
* Generar estadísticas
* Optimizar el comportamiento energético

---

## 🧪 Pruebas

El proyecto incluye una lista de control de pruebas que valida:

* Lectura correcta del sensor LDR
* Detección de presencia
* Clasificación de estados
* Cálculo de consumo y CO₂
* Funcionamiento del hardware

---

## 🌍 Impacto Ambiental

El sistema contribuye a la reducción de emisiones de CO₂ al disminuir el consumo innecesario de energía eléctrica, promoviendo el uso eficiente de recursos.

---

## 🚀 Estado del Proyecto

🔧 En desarrollo
Actualmente se encuentra en fase de integración entre hardware y software.

---

## 💡 Futuras Mejoras

* Implementación de inteligencia artificial (predicción de consumo)
* Dashboard web en tiempo real
* Automatización completa del sistema
* Integración con múltiples sensores

---

## 🧑‍💻 Autor

## MotorCaI 🦜

---

## 📜 Licencia

Este proyecto está orientado al uso educativo y puede ser adaptado libremente como parte de iniciativas open-source.
