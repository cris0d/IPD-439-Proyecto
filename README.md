# Proyecto: Benchmarking de Sistemas Operativos en Tiempo Real (RTOS)
**Asignatura:** IPD439 - Seminario Avanzado de Computadores  
**Institución:** Universidad Técnica Federico Santa María  
**Alumno:** Cristián Ayancán  
**Plataforma:** STM32L476RG (Nucleo-64)

---

## Descripción del Proyecto

Este proyecto compara el desempeño de distintos sistemas operativos en tiempo real (RTOS) sobre la plataforma STM32L476RG, midiendo métricas críticas como Task Switch Time, Preemption Time e Interrupt Latency. Las mediciones se realizaron utilizando un analizador lógico Saleae a 100 MS/s.

---

## Estructura del Repositorio

### 📁 FreeRTOS/

#### 📁 FreeRTOS_Benchmark_2/
Proyecto STM32CubeIDE para la medición del **Task Switch Time**.

#### 📁 FreeRTOS_3/
Proyecto STM32CubeIDE para la medición del **Preemption Time**.

#### 📁 FreeRTOS_4/
Proyecto STM32CubeIDE para la medición del **Interrupt Latency**.

---

## Instrucciones para Replicar el Proyecto

### 🔹 Clonar repositorio
```bash
1. git clone https://github.com/cris0d/IPD-439-Proyecto.git
2. Abrir STM32CubeIDE y seleccionar un nuevo Workspace.
3. Ir a `File > Import... > General > Existing Projects into Workspace`.
4. Seleccionar la carpeta `FreeRTOS/FreeRTOS_Benchmark_2`, `FreeRTOS/FreeRTOS_3` o `FreeRTOS/FreeRTOS_4` según el proyecto a abrir.
```