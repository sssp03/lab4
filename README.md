# Laboratorio 4
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
  
