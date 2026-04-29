# 🧪 i Hate HoPiNg — Test Report & Project Status

## 📌 Descripción

Este documento describe el estado actual del proyecto **i Hate HoPiNg**, incluyendo los avances realizados, pruebas completadas, componentes pendientes y errores identificados durante el desarrollo.

---

## ✅ Estado Actual del Proyecto

El proyecto se encuentra en una fase funcional a nivel de software, donde la lógica principal del sistema ya ha sido implementada y validada mediante simulaciones.

Actualmente, el sistema es capaz de analizar datos, clasificar situaciones energéticas y calcular impacto ambiental.

---

## 🟢 Pruebas Completadas

### 🔹 Funcionalidad

* Ejecución correcta del sistema en Python
* Simulación de datos de luz (LDR)
* Simulación de detección de presencia
* Clasificación correcta de estados:

  * DESPERDICIO
  * USO CORRECTO
  * OPTIMIZABLE

---

### 🔹 Software

* Procesamiento de datos sin errores
* Cálculo estimado de consumo energético (kWh)
* Cálculo de emisiones de CO₂
* Visualización de resultados en consola

---

### 🔹 Datos

* Definición de estructura de almacenamiento (`data.csv`)
* Registro de datos simulados

---

## 🟡 Pruebas en Desarrollo

### 🔹 Interfaz

* Visualización limitada a consola
* No se ha implementado interfaz gráfica o dashboard

---

### 🔹 Hardware (Parcial)

* Uso de datos simulados en lugar de sensores reales
* Pendiente conexión física del Arduino

---

## 🔴 Pruebas Pendientes

### 🔹 Hardware

* Lectura real del sensor LDR
* Montaje del circuito en protoboard
* Control físico de LEDs
* Activación del módulo relé

---

### 🔹 Integración

* Comunicación Arduino ↔ Python (PySerial)
* Sincronización entre hardware y software

---

### 🔹 Visión Artificial

* Implementación de detección de presencia con OpenCV

---

### 🔹 Validación Real

* Pruebas en entorno físico
* Evaluación con datos reales
* Ajuste de umbrales y condiciones

---

## 🐞 Bugs y Limitaciones

Actualmente no se han identificado errores críticos en el sistema, pero existen limitaciones importantes:

* Dependencia de datos simulados
* Falta de integración con hardware real
* Ausencia de validación en condiciones reales
* No se han probado escenarios complejos o prolongados

---

## 🔧 Plan de Mejora

Para completar el proyecto, se han definido las siguientes acciones:

1. Implementar conexión física del sensor LDR
2. Integrar Arduino con Python mediante comunicación serial
3. Añadir control de LEDs y relé
4. Implementar detección de presencia con OpenCV
5. Desarrollar una interfaz visual para el usuario
6. Realizar pruebas completas en entorno real

---

## 🧠 Conclusión

El proyecto ha alcanzado una base sólida en términos de lógica y análisis de datos.
La siguiente fase se centra en la integración de hardware y validación en condiciones reales para convertir el sistema en una solución completamente funcional.

---

## 📌 Estado General

🔧 En desarrollo — fase de integración hardware/software
