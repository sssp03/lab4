## Laboratorio 4
En la práctica realizada, el objetivo fue capturar la señal electromiográfica del músculo en estado de fatiga. Para ello, se utilizaron los siguientes elementos: un módulo de ECG, jumpers,fuente de voltaje, cables con sus respectivos electrodos y un sistema de adquisición de datos NI-DAQmx este sistema se descargo por meio de un link que esta en el aula virtual.
Como primer paso, se colocaron tres electrodos: uno de referencia (tierra) en el codo y dos de registro en el antebrazo, parecido como se muestra en la imagen:

![image](https://github.com/user-attachments/assets/ee47aa9b-4352-4970-8734-ec1de5749ded)

Despues de esto se conecto todo y por medio de la DAQmx se pudo observar la grafica en el computador para guardar la señal nosotros utlizamos python con el siguiente codigo:

```python
import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import matplotlib.pyplot as plt
with nidaqmx.Task() as task:
   task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
   task.timing.cfg_samp_clk_timing(10000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=1000)
   data = task.read(READ_ALL_AVAILABLE)
   plt.plot(data)
   plt.ylabel('Amplitude')
   plt.title('Waveform')
   plt.show()

AIChannel(name=Dev1/ai0)
##[<matplotlib.lines.Line2D object at 0x00000141D7043970>]
Text(0, 0.5, 'Amplitude')
Text(0.5, 1.0, 'waveform')
```
Con el codigo anterior se logro graficar y guardar la señal, a continuacion se va explicar que hace cada linea del codigo anterior:

- Se importa nidaqmx para la adquisición de datos.
- Se traen constantes necesarias (AcquisitionType y READ_ALL_AVAILABLE).
- Se importa matplotlib.pyplot para graficar la señal.

```python
with nidaqmx.Task() as task:
```

- Se crea una tarea (task) usando un contexto with, lo que garantiza que la tarea se cierre correctamente después de ejecutarse.

```python
  task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
```

- Se añade un canal de voltaje analógico (ai0) del dispositivo Dev1.
- Este canal leerá señales de voltaje en el puerto Dev1/ai0.

```python
task.timing.cfg_samp_clk_timing(2000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=2600)
```
- Se configura la tasa de muestreo en 2000 muestras por segundo (Hz).
- El modo de adquisición es finito (FINITE), es decir, tomará una cantidad limitada de muestras 13s.
- Se especifica que tomará 26000 muestras por canal.
```python
data = task.read(READ_ALL_AVAILABLE)
```
- Se leen todas las muestras disponibles en el buffer.
```python
plt.plot(data)
plt.ylabel('Amplitude')
plt.title('Waveform')
plt.show()
```
- Se grafica la señal adquirida (data).
- Se etiquetan los ejes (Amplitud en el eje Y).
- Se muestra la gráfica.

Después de capturar la señal se le plicaron los siguientes filtros para limpiar la señal y quedara mas bonita:
# Filtrado pasa altas (High-pass, 20 Hz):
Esta parte del código elimina el ruido de baja frecuencia (artefactos de movimiento, línea base).
```python
high_cutoff = 20  # Frecuencia de corte en Hz
b_high, a_high = signal.butter(4, high_cutoff / (fs / 2), btype='high')
emg_highpass = signal.filtfilt(b_high, a_high, emg_signal)
```
- Diseña un filtro Butterworth de orden 4.
- Aplica el filtro a la señal usando filtfilt() (filtrado en ambas direcciones para evitar desfase).
# Filtrado pasa bajas (Low-pass, 450 Hz):
Esta parte elimina interferencias electromagnéticas y ruido de alta frecuencia.
```python
low_cutoff = 450  # Frecuencia de corte en Hz
b_low, a_low = signal.butter(4, low_cutoff / (fs / 2), btype='low')
emg_filtered = signal.filtfilt(b_low, a_low, emg_highpass)
```
- Diseña otro filtro Butterworth de orden 4.
- Filtra la señal después del pasa altas
![SEÑALORIGINAL Y FILTRADA](https://github.com/user-attachments/assets/0ea90c99-d4b8-42cb-b625-3a16d711fbd6)

Luego de realizar estos filtros, se dividio la señal registrada en ventanas de tiempo, usando una técnica de aventanamiento como la ventana de Hamming o Hanning. y realizar el análisis espectral de cada ventana utilizando la Transformada de Fourier (FFT) para obtener el espectro de frecuencias en intervalos específicos de la señal EMG.
# Ventaneo de la señal EMG
Esta parte divide la señal en ventanas de 0.5 segundos con 50% de solapamiento.
```python
win_size = int(0.5 * fs)  # Ventana de 0.5s (1000 muestras)
overlap = int(0.25 * fs)  # 50% de solapamiento (500 muestras)
step = win_size - overlap
num_windows = (len(emg_filtered) - win_size) // step
```
- Convierte 0.5 s en muestras → 0.5×2000=1000
- Calcula el solapamiento (mitad de la ventana).
- Determina cuántas ventanas caben en la señal.
# Aplicación de la Ventana de Hamming
Cada segmento de la señal se multiplica por una ventana de Hamming para suavizar los bordes.
```python
segment = emg_filtered[start:end] * np.hamming(win_size)
```
- Extrae un segmento de 1000 muestras.
- Multiplica por la ventana de Hamming (reduce efectos de bordes en la FFT).
# Transformada de Fourier (FFT) en cada ventana
Esto obtiene el espectro de frecuencias de cada segmento.
```python
fft_spectrum = np.fft.rfft(segment)  # FFT rápida para señales reales
freqs = np.fft.rfftfreq(win_size, d=1/fs)  # Calcula las frecuencias correspondientes
```
- np.fft.rfft() → Calcula la Transformada de Fourier de la señal en la ventana.
- np.fft.rfftfreq() → Genera el eje de frecuencias (hasta 500 Hz).
Frecuencia dominante:

# Frecuencia dominante:
```python
freq_dominante = freqs[np.argmax(fft_spectrum)]
```
-Toma la frecuencia donde la FFT tiene el pico máximo (mayor amplitud).

# Frecuencia media (Centroide espectral):
```python
freq_media = np.sum(freqs * fft_spectrum) / np.sum(fft_spectrum)
```
-Calcula la media ponderada de las frecuencias del espectro.
# Desviación estándar espectral:
```python
freq_std = np.sqrt(np.sum((freqs - freq_media)**2 * fft_spectrum) / np.sum(fft_spectrum))
```
- Mide la dispersión de la energía espectral respecto a la frecuencia media.
![ESPECTRO](https://github.com/user-attachments/assets/999854c3-d73a-4284-9647-97348099e20a)

El análisis espectral de la señal segmentada en diferentes ventanas temporales muestra que la mayor concentración de energía se encuentra en el rango de 0 a 100 Hz, lo cual es característico de la actividad muscular. A partir de los 100 Hz, la amplitud de la señal disminuye progresivamente, lo que indica una menor presencia de componentes de alta frecuencia, también Se puede  observar cierta variabilidad entre las ventanas, lo que podría significar cambios en la activación muscular a lo largo del tiempo. Además, en frecuencias superiores a 200 Hz, se presenta un nivel de ruido que podría estar asociado a interferencias externas o artefactos de movimiento. 

# Prueba de hipótesis 
Una prueba de hipótesis es un procedimiento estadístico utilizado para determinar si existe suficiente evidencia en una muestra de datos para aceptar o rechazar una suposición sobre una población. 

![image](https://github.com/user-attachments/assets/92aa7e43-7f2b-4112-bdfd-87c966b6f9f5)

# Se importaron las librerías:

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
```
# Se definieron los datos de muestras :
```python
n1 = 50858  # Número de muestras del primer grupo
n2 = 50858  # Número de muestras del segundo grupo
mu1 = 0.001200367   # Media del primer grupo
mu2 = 0.001452753   # Media del segundo grupo
sigma1 = 5.1903     # Desviación estándar del primer grupo
sigma2 = 5.1904     # Desviación estándar del segundo grupo
```
# El cálculo estadístico:
```python
t_stat = (mu1 - mu2) / np.sqrt((sigma1**2 / n1) + (sigma2**2 / n2))
```
# Cálculo de los grados de libertad 
```python
df = ((sigma1**2 / n1) + (sigma2**2 / n2))**2 / (
    ((sigma1**2 / n1)**2 / (n1 - 1)) + ((sigma2**2 / n2)**2 / (n2 - 1))
)
df = int(df)  # Se convierte a entero
```
# Valor crítico:
```python
alpha_01 = stats.t.ppf(1 - 0.025, df=df)
```
# Generación de la distribución
```python
x = np.linspace(-4, 4, 400)  # Se crea un rango de valores de t
y = stats.t.pdf(x, df=df)    # Se calcula la función de densidad de probabilidad
```
# Gráfica de distribución
```python
plt.figure(figsize=(8, 5))
plt.plot(x, y, label=f'Distribución t (df={df})', color='blue')
```

El gráfico representa la distribución t , utilizada para evaluar la significancia estadística en una prueba de hipótesis. La curva azul muestra la distribución t con 101,713 grados de libertad, lo que implica que se asemeja a una distribución normal estándar debido al gran tamaño de la muestra.
Las regiones sombreadas en rojo corresponden a las regiones de rechazo para un nivel de significancia de α = 0.05. Los valores críticos de t se encuentran en ±1.96, lo que significa que cualquier estadístico de prueba fuera de este rango indicaría una diferencia estadísticamente significativa entre las muestras.
El estadístico t calculado en esta prueba es t = -0.01 (línea verde punteada), el cual se encuentra dentro de la región de aceptación. Esto indica que no hay suficiente evidencia estadística para rechazar la hipótesis nula, es decir, no se detecta una diferencia significativa entre las medianas de las muestras comparadas.
Este resultado sugiere que los cambios observados en los datos pueden deberse a la variabilidad natural de la muestra y no a un efecto real significativo.

# Hipótesis para el análisis de fatiga muscular
- Hipótesis nula (H₀): No hay fatiga muscular, la mediana de la señal EMG no muestra un cambio significativo.
- Hipótesis alternativa (H₁): Hay fatiga muscular, la mediana de la señal EMG presenta un cambio significativo.
Según el gráfico de la distribución t , si el estadístico t cae dentro de la región blanca (zona de aceptación), no se rechaza la hipótesis nula (H₀), lo que sugiere que no hay evidencia suficiente para afirmar que existe fatiga muscular.
Por otro lado, si el estadístico t cae en la región sombreada (zona de rechazo), se rechaza la hipótesis nula (H₀) y se acepta la alternativa (H₁), lo que indica que sí hay un cambio significativo en la señal EMG, lo cual es evidencia de fatiga muscular.
Dado que en el gráfico el estadístico t obtenido es t = -0.01, y este valor cae dentro de la región blanca, no hay suficiente evidencia estadística para afirmar la presencia de fatiga muscular en este caso. 




