import csv
import statistics

# Leer el archivo
rows = []
with open('overhead.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append({
            'time': float(row['Time [s]']),
            'taskA': int(row['taskA']),
        })


pulse_widths = []

for i in range(1, len(rows)):
    prev = rows[i - 1]
    curr = rows[i]

    # Subida de TaskA (0->1)
    if prev['taskA'] == 0 and curr['taskA'] == 1:
        t_rise = curr['time']
        # Buscar la siguiente bajada
        for j in range(i + 1, len(rows)):
            if rows[j]['taskA'] == 0 and rows[j-1]['taskA'] == 1:
                t_fall = rows[j]['time']
                width = (t_fall - t_rise) * 1e9  # convertir a ns
                if 0 < width < 100000:  # filtrar valores inválidos
                    pulse_widths.append(width)
                break

print("=" * 50)
print("CALIBRACIÓN gpio_pin_set_dt() — Zephyr STM32L476RG")
print("=" * 50)
print(f"\nAncho de pulso (SET+RESET):")
print(f"  N muestras:          {len(pulse_widths)}")
print(f"  Promedio:            {statistics.mean(pulse_widths):.3f} ns")
print(f"  Desviación estándar: {statistics.stdev(pulse_widths):.3f} ns")
print(f"  Mínimo:              {min(pulse_widths):.3f} ns")
print(f"  Máximo:              {max(pulse_widths):.3f} ns")

overhead_per_call = statistics.mean(pulse_widths) / 2
print(f"\nOverhead de una llamada a gpio_pin_set_dt():")
print(f"  {overhead_per_call:.1f} ns")
