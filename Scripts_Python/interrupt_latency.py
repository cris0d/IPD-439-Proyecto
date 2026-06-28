import csv
import statistics
import bisect

# Leer el archivo
rows = []
with open('it.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            'time': float(row['Time [s]']),
            'taskA': int(row['TaskA']),
            'boton_it': int(row['Boton_IT'])
        })

# --- Paso 1: extraer flancos de bajada del botón con DEBOUNCE ---
# IMPORTANTE: el CSV es un export de "solo transiciones" (Saleae edge export),
# así que el timestamp de cada fila YA ES el instante exacto del flanco.
# No promediar con la fila anterior.
DEBOUNCE_WINDOW_S = 0.005  # 5 ms

button_falls = []
for i in range(1, len(rows)):
    prev = rows[i - 1]
    curr = rows[i]
    if prev['boton_it'] == 1 and curr['boton_it'] == 0:
        t_fall = curr['time']
        if not button_falls or (t_fall - button_falls[-1]) > DEBOUNCE_WINDOW_S:
            button_falls.append(t_fall)

# --- Paso 2: extraer flancos de subida de TaskA (ISR) ---
taskA_rises = []
for i in range(1, len(rows)):
    prev = rows[i - 1]
    curr = rows[i]
    if prev['taskA'] == 0 and curr['taskA'] == 1:
        taskA_rises.append(curr['time'])

# --- Paso 3: para cada caída de botón, buscar la SIGUIENTE subida de TaskA ---
MAX_WINDOW_S = 0.00002  # 20 µs en vez de 1 ms

il_values = []

for t_fall in button_falls:
    idx = bisect.bisect_right(taskA_rises, t_fall)
    if idx >= len(taskA_rises):
        continue

    t_rise = taskA_rises[idx]
    delta = t_rise - t_fall

    if 0 < delta < MAX_WINDOW_S:
        il_values.append(delta * 1e6)  # convertir a µs

OVERHEAD_GPIO_US = 0.265213

print("=" * 50)
print("INTERRUPT LATENCY — Zephyr STM32L476RG")
print("=" * 50)
print(f"\nFlancos de botón detectados (tras debounce): {len(button_falls)}")
print(f"Flancos de TaskA disponibles:                  {len(taskA_rises)}")

if not il_values:
    print("\n⚠️  No se encontraron muestras válidas de Interrupt Latency.")
else:
    print(f"\nInterrupt Latency (Botón cae → ISR ejecuta):")
    print(f"  N muestras:          {len(il_values)}")
    print(f"  Promedio medido:     {statistics.mean(il_values):.3f} µs")
    print(f"  Promedio real:       {statistics.mean(il_values) - OVERHEAD_GPIO_US:.3f} µs")
    if len(il_values) > 1:
        print(f"  Desviación estándar: {statistics.stdev(il_values):.3f} µs")
    print(f"  Mínimo:              {min(il_values):.3f} µs")
    print(f"  Máximo:              {max(il_values):.3f} µs")