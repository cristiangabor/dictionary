import pyaudio
import sys
import wave
import spaniola
from PyQt4.QtGui import*
from PyQt4.QtCore import*

def make_sound():
	CHUNK=1024

	p = pyaudio.PyAudio()

	stream=p.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=CHUNK)

	print ("recording.....")

	hercule=spaniola.Fereastra_Doua(self)
	hercule.playground()

	frames=[]

	for i in range(0,100):
		data=stream.read(CHUNK)
		frames.append(data)

	print ("finished recordin..")

	#stop Recording

	stream.stop_stream()
	stream.close()
	p.terminate()

	waveFile = wave.open("cristi.wav", 'wb')
	waveFile.setnchannels(2)
	waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
	waveFile.setframerate(44100)
	waveFile.writeframes(b''.join(frames))
	waveFile.close