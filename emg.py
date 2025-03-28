import numpy as np
import matplotlib.pyplot as plt

# Nombre del archivo
archivo_txt = "emg.txt"  # Asegúrate de que la ruta es correcta

# Cargar datos desde el archivo, saltando la primera fila (cabecera)
datos = np.loadtxt(archivo_txt, skiprows=1)

# Extraer columnas
tiempo = datos[:, 0]  # Primera columna: tiempo
voltaje = datos[:, 1]  # Segunda columna: voltaje

# Graficar la señal EMG
plt.figure(figsize=(10, 5))
plt.plot(tiempo, voltaje, label="Señal EMG", color="b")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (mV)")
plt.title("Señal de EMG")
plt.legend()
plt.grid(True)
plt.show()
