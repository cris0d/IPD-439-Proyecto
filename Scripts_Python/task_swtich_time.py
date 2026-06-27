import csv
import statistics

# Leer el archivo
rows = []
with open('digital.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            'time': float(row['Time [s]']),
            'taskA': int(row['TaskA']),
            'taskB': int(row['TaskB'])
        })

# Calcular TST A→B: tiempo entre bajada de TaskA y subida de TaskB
tst_ab = []
tst_ba = []

for i in range(1, len(rows) - 1):
    prev = rows[i - 1]
    curr = rows[i]
    
    # Bajada de TaskA (1→0)
    if prev['taskA'] == 1 and curr['taskA'] == 0:
        t_fall_a = curr['time']
        # Buscar siguiente subida de TaskB
        for j in range(i + 1, len(rows)):
            if rows[j]['taskB'] == 1 and rows[j-1]['taskB'] == 0:
                t_rise_b = rows[j]['time']
                tst = (t_rise_b - t_fall_a) * 1e9  # convertir a ns
                if 0 < tst < 100000:  # filtrar valores inválidos
                    tst_ab.append(tst)
                break

    # Bajada de TaskB (1→0)
    if prev['taskB'] == 1 and curr['taskB'] == 0:
        t_fall_b = curr['time']
        # Buscar siguiente subida de TaskA
        for j in range(i + 1, len(rows)):
            if rows[j]['taskA'] == 1 and rows[j-1]['taskA'] == 0:
                t_rise_a = rows[j]['time']
                tst = (t_rise_a - t_fall_b) * 1e9
                if 0 < tst < 100000:
                    tst_ba.append(tst)
                break

# Overhead GPIO calibrado (~277 ns por llamada)
OVERHEAD_GPIO_NS = 277

print("=" * 50)
print("TASK SWITCH TIME — FreeRTOS STM32L476RG")
print("=" * 50)

print(f"\nTST A→B (TaskA cede → TaskB ejecuta):")
print(f"  N muestras:          {len(tst_ab)}")
print(f"  Promedio medido:     {statistics.mean(tst_ab):.1f} ns")
print(f"  Promedio real:       {statistics.mean(tst_ab) - OVERHEAD_GPIO_NS:.1f} ns")
print(f"  Desviación estándar: {statistics.stdev(tst_ab):.1f} ns")
print(f"  Mínimo:              {min(tst_ab):.1f} ns")
print(f"  Máximo:              {max(tst_ab):.1f} ns")

print(f"\nTST B→A (TaskB cede → TaskA ejecuta):")
print(f"  N muestras:          {len(tst_ba)}")
print(f"  Promedio medido:     {statistics.mean(tst_ba):.1f} ns")
print(f"  Promedio real:       {statistics.mean(tst_ba) - OVERHEAD_GPIO_NS:.1f} ns")
print(f"  Desviación estándar: {statistics.stdev(tst_ba):.1f} ns")
print(f"  Mínimo:              {min(tst_ba):.1f} ns")
print(f"  Máximo:              {max(tst_ba):.1f} ns")

tst_all = tst_ab + tst_ba
print(f"\nTST PROMEDIO GLOBAL:")
print(f"  N muestras:          {len(tst_all)}")
print(f"  Promedio medido:     {statistics.mean(tst_all):.1f} ns")
print(f"  Promedio real:       {statistics.mean(tst_all) - OVERHEAD_GPIO_NS:.1f} ns")
print(f"  Desviación estándar: {statistics.stdev(tst_all):.1f} ns")
print(f"  Mínimo:              {min(tst_all):.1f} ns")
print(f"  Máximo:              {max(tst_all):.1f} ns")