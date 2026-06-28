# Proyecto: Benchmarking de Sistemas Operativos en Tiempo Real (RTOS)
**Asignatura:** IPD439 - Seminario Avanzado de Computadores  
**Institución:** Universidad Técnica Federico Santa María  
**Alumno:** Cristián Ayancán  
**Plataforma:** STM32L476RG (Nucleo-64)

---

## Descripción del Proyecto

Este proyecto compara el desempeño de dos sistemas operativos en tiempo real (RTOS) —**FreeRTOS** y **Zephyr**— sobre la plataforma STM32L476RG, midiendo métricas críticas como **Task Switch Time**, **Preemption Time** e **Interrupt Latency**. Las mediciones se realizaron utilizando un analizador lógico Saleae a 100 MS/s, y los resultados fueron procesados mediante scripts de Python para obtener estadísticas representativas (media, desviación estándar, mínimo y máximo) de cada métrica.

---

## Estructura del Repositorio

### 📁 FreeRTOS/

#### 📁 FreeRTOS_Benchmark_2/
Proyecto STM32CubeIDE para la medición del **Task Switch Time**.

#### 📁 FreeRTOS_3/
Proyecto STM32CubeIDE para la medición del **Preemption Time**.

#### 📁 FreeRTOS_4/
Proyecto STM32CubeIDE para la medición del **Interrupt Latency**.

### 📁 Zephyr/

#### 📁 zephyr_task_switch_time/
Proyecto Zephyr (west workspace app) para la medición del **Task Switch Time**.

#### 📁 zephyr_preemption_time/
Proyecto Zephyr (west workspace app) para la medición del **Preemption Time**.

#### 📁 zephyr_interrupt_latency/
Proyecto Zephyr (west workspace app) para la medición del **Interrupt Latency**.

---

## Instrucciones para Replicar el Proyecto

### 🔹 Clonar repositorio

```bash
git clone https://github.com/cris0d/IPD-439-Proyecto.git
```

### 🔹 FreeRTOS (STM32CubeIDE)

```bash
1. Abrir STM32CubeIDE y seleccionar un nuevo Workspace.
2. Ir a `File > Import... > General > Existing Projects into Workspace`.
3. Seleccionar la carpeta `FreeRTOS/FreeRTOS_Benchmark_2`, `FreeRTOS/FreeRTOS_3` o `FreeRTOS/FreeRTOS_4` según el proyecto a abrir.
4. Compilar (`Project > Build`) y flashear (`Run > Debug` o `Run > Run`) directamente desde el IDE vía ST-Link.
```

### 🔹 Zephyr (west + Linux)

```bash
1. Instalar dependencias del sistema (Python 3, CMake, Ninja, GCC ARM) y la herramienta `west`.
2. Inicializar el workspace de Zephyr (`west init` / `west update`) e instalar el Zephyr SDK
   (incluye el toolchain arm-none-eabi-gcc y OpenOCD).
3. Entrar a la carpeta del benchmark a compilar, por ejemplo:
   cd Zephyr/zephyr_task_switch_time
4. Compilar para la Nucleo-L476RG:
   west build -b nucleo_l476rg
5. Flashear la placa:
   west flash --runner openocd
```

> Repetir los pasos 3-5 para `zephyr_preemption_time` y `zephyr_interrupt_latency`.

### 🔹 Captura y análisis de mediciones

1. Conectar el analizador lógico Saleae a los pines GPIO configurados en cada proyecto (ver `main.c` / overlay de cada carpeta).
2. Capturar las transiciones con **Logic 2** y exportar a CSV (modo "edges only").
3. Procesar el CSV con los scripts de Python incluidos en el repositorio para obtener las estadísticas de cada métrica (N, promedio, desviación estándar, mínimo, máximo).
