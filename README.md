# delta-modulation
This project is dedicated to the Digital Communication course.
This code can record your own voice in real-time and perform delta modulation on it.

In this, you can choose the duration of your voice recording and choose the step size for the modulation.
After this, it will plot the original & modulated version of the message signal (which is your recorded voice in this). You can zoom into the modulated signal to see how delta modulation is taking place. It also plots the quantization error signal to understand at which instances the error is maximum.
It prints the Signal-to-Noise Ratio as well for understanding.

It also saves the modulated signal in .wav format and saves the encoded binary sequence in a .txt file.
You can choose the other python file if you want to perform modulation on an already existing .wav file. 

And if you want to reconstruct the original message signal back from the encoded binary sequence then run the demodulation2.py file and select the .txt file.
Note: Make sure to use the same step size for demoudulation & always type 44100 for sample rate for best results. It will generate a reconstructed .wav file.

Python libraries required for this:
1. tkinter: Provides graphical user interface (GUI) features for opening file dialogs.
2. numpy (For numerical computing in Python)
3. matplotlib (For plotting the signals)
4. scipy (For scientific computing and technical computing)
5. sounddevice (For recording and playing audio)

Made by Siddharth Kumar with the help of AI
