import csv
import statistics
import bisect

# Leer el archivo
rows = []
with open('pt.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            'time': float(row['Time [s]']),
            'taskLPT': int(row['TaskLPT']),
            'taskHPT': int(row['TaskHPT'])
        })

# IMPORTANTE: el CSV es un export de "solo transiciones" (Saleae edge export),
# así que el timestamp de cada fila YA ES el instante exacto del flanco.
# No promediar con la fila anterior (ver lección aprendida en Interrupt Latency).

# --- Paso 1: extraer flancos de SUBIDA de TaskLPT (T0: dispara osSemaphoreRelease / k_sem_give) ---
lpt_rises = []
for i in range(1, len(rows)):
    prev = rows[i - 1]
    curr = rows[i]
    if prev['taskLPT'] == 0 and curr['taskLPT'] == 1:
        lpt_rises.append(curr['time'])

# --- Paso 2: extraer flancos de SUBIDA de TaskHPT (T1: retoma el CPU tras la preemption) ---
hpt_rises = []
for i in range(1, len(rows)):
    prev = rows[i - 1]
    curr = rows[i]
    if prev['taskHPT'] == 0 and curr['taskHPT'] == 1:
        hpt_rises.append(curr['time'])

# --- Paso 3: para cada subida de LPT, buscar la SIGUIENTE subida de HPT ---
# PTmedido = (t_subida,HPT - t_subida,LPT)
MAX_WINDOW_S = 0.0005  # 500 µs: ventana generosa, ajusta si ves outliers

pt_values = []
for t_lpt in lpt_rises:
    idx = bisect.bisect_right(hpt_rises, t_lpt)
    if idx >= len(hpt_rises):
        continue

    t_hpt = hpt_rises[idx]
    delta = t_hpt - t_lpt

    if 0 < delta < MAX_WINDOW_S:
        pt_values.append(delta * 1e6)  # convertir a µs

# Overhead de UNA sola llamada a gpio_pin_set_dt() ya calibrado: 265.213 ns
OVERHEAD_GPIO_US = 0.265213

print("=" * 50)
print("PREEMPTION TIME — Zephyr STM32L476RG")
print("=" * 50)
print(f"\nFlancos de subida de TaskLPT detectados: {len(lpt_rises)}")
print(f"Flancos de subida de TaskHPT detectados: {len(hpt_rises)}")

if not pt_values:
    print("\n⚠️  No se encontraron muestras válidas de Preemption Time.")
else:
    print(f"\nPreemption Time (TaskLPT sube → TaskHPT retoma CPU):")
    print(f"  N muestras:          {len(pt_values)}")
    print(f"  Promedio medido:     {statistics.mean(pt_values):.3f} µs")
    print(f"  Promedio real:       {statistics.mean(pt_values) - OVERHEAD_GPIO_US:.3f} µs")
    if len(pt_values) > 1:
        print(f"  Desviación estándar: {statistics.stdev(pt_values):.3f} µs")
    print(f"  Mínimo:              {min(pt_values):.3f} µs")
    print(f"  Máximo:              {max(pt_values):.3f} µs")