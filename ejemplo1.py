import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

# Cargar la señal desde el archivo .txt
data = np.loadtxt("emg_healthy_cleaned.txt", skiprows=1)  # Saltamos la primera fila (encabezado)
t = data[:, 0]  # Tiempo en segundos
emg_signal = data[:, 1]  # Señal EMG

# Definir la frecuencia de muestreo
fs = 2000  # Hz

# --- FILTRADO ---
# Pasa altas (elimina ruido de línea base y movimiento)
high_cutoff = 20  
b_high, a_high = signal.butter(4, high_cutoff / (fs / 2), btype='high')
emg_highpass = signal.filtfilt(b_high, a_high, emg_signal)

# Pasa bajas (elimina interferencias electromagnéticas)
low_cutoff = 450  
b_low, a_low = signal.butter(4, low_cutoff / (fs / 2), btype='low')
emg_filtered = signal.filtfilt(b_low, a_low, emg_highpass)

# --- VENTANEO ---
win_size = int(0.5 * fs)  # Ventanas de 0.5 segundos
overlap = int(0.25 * fs)  # 50% de solapamiento
step = win_size - overlap
num_windows = (len(emg_filtered) - win_size) // step

plt.figure(figsize=(12, 6))

for i in range(num_windows):
    start = i * step
    end = start + win_size
    segment = emg_filtered[start:end] * np.hamming(win_size)  # Aplicar ventana de Hamming
    
    # --- ANÁLISIS ESPECTRAL ---
    fft_spectrum = np.fft.rfft(segment)
    freqs = np.fft.rfftfreq(win_size, d=1/fs)
    
    plt.plot(freqs, np.abs(fft_spectrum), alpha=0.5, label=f"Ventana {i+1}" if i < 5 else None)

# Configuración de la gráfica de espectro
plt.title("Análisis Espectral de la Señal EMG por Ventanas")
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud")
plt.xlim([0, 500])
plt.grid()
plt.legend()
plt.show()

# Guardar la señal filtrada
np.savetxt("emg_healthy_filtered.txt", np.column_stack((t, emg_filtered)), header="Tiempo[s] SeñalEMG_Filtrada", comments='')

