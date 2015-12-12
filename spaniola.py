# Setarea importurilor
import pyaudio
import wave
import sys 
import sqlite3      
import time
import search
import bazadedate
from PyQt4.QtGui import*
from PyQt4.QtCore import*
from threading import Thread # multiprocess library


aplicatie=QApplication(sys.argv)

class Fereastra_Doua(QDialog):
	def __init__(self,eu):
		QDialog.__init__(self)
		
		# Dialog geometry and Title 

		self.setGeometry(740,100,300,280)
		self.setWindowTitle('Dictionar')

		#  Variabile

		self.EnglezaTxt=QLabel("<b>Engleza</b>",self)
		self.EnglezaTxt.setGeometry(25,20,60,30)
		self.SpaniolaTxt=QLabel("<b>Spaniola</b>",self)
		self.SpaniolaTxt.setGeometry(165,20,60,30)
		self.EnterEngleza=QTextEdit(self)
		self.EnterEngleza.setGeometry(20,60,90,50)
		self.EnterSpaniola=QTextEdit(self)
		self.EnterSpaniola.setGeometry(160,60,90,50)
		self.EnterEngleza.setStyleSheet("QTextEdit  {border:2px solid black;}")
		self.EnterSpaniola.setStyleSheet("QTextEdit {border:2px solid black;}")

		self.Regist=QPushButton("",self)
		self.Regist.setStyleSheet("QPushButton{border-top: 3px transparent;border-bottom: 3px transparent; border-right: 10px transparent; border-left: 10px transparent;}")
		self.Regist.setIcon(QIcon('pnguri/micoto.png'))
		self.Regist.setIconSize(QSize(80,40))
		self.Regist.setToolTip('Inregistreaza')
		self.Regist.setGeometry(110,120,50,40)
		self.Regist.pressed.connect(self.activate)
		#self.Regist.released.connect(self.releasing)

		self.test=QLabel("",self)
		self.test.setGeometry(210,120,60,40)	
		self.playbuton=QPushButton("",self)
		self.playbuton.setCheckable(True)
		self.playbuton.setGeometry(20,230,40,30)
		self.playbuton.setStyleSheet('QPushButton { border: 2px solid #8f8f91;border-radius:8px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 40px;}')
		self.playbuton.setIcon(QIcon('pnguri/play.png'))
		self.playbuton.setIconSize(QSize(60,20))
		self.playbuton.setToolTip('Reda')
		self.playbuton.setEnabled(False)
		self.playbuton.pressed.connect(self.playBUTTON)
		
		# Initializare Controale
		self.playtheaudio=False
		self.incercare=False
		self.ciclu=False
		self.inchide_dialog=False
		self.mentine_numaratoare=False		
		self.repeateaudio=False

		self.buttonBox=QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
		self.buttonBox.setGeometry(160,220,120,50)
		self.buttonBox.setStyleSheet('QPushButton { border: 2px solid #8f8f91;border-radius:10px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 40px;}')
		self.buttonBox.rejected.connect(self.cancel_press)
		self.buttonBox.accepted.connect(self.ok_button)

		self.progressing_bar = QProgressBar(self)
		self.progressing_bar.setGeometry(20,200,90,20)
		self.progressing_bar.setMaximum(9)
		self.progressing_bar.setStyleSheet("QProgressBar::chunk { background-color: #05B8CC; width: 10px; margin:0.5 px;}")


	def cancel_press(self):
		self.close()
		self.playtheaudio=False
		self.inchide_dialog = True
		self.playbuton.setEnabled(False)
		self.mentine_numaratoare=False
		self.EnterEngleza.setPlainText("")
		self.EnterSpaniola.setPlainText("")



	def set_text(self):

		if self.test.text() == "":
			self.incercare=True
			self.mentine_numaratoare=True
			for i in range(0,10):
				if self.mentine_numaratoare==True:
					a = 10-i
					self.test.setText(str(a)+"...")
					time.sleep(1)
				else:
					break
			self.playbuton.setEnabled(True)
			self.test.setText("")
			self.incercare=False

	def deset_text(self):
		
		if self.ciclu == False:
			self.ciclu=True
			
			CHUNK=1024

			p = pyaudio.PyAudio()

			stream=p.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=CHUNK)

		
			print ("recording.....")
		
			frames=[]
			while self.incercare == True and self.inchide_dialog==False:
				data=stream.read(CHUNK)
				frames.append(data)

			print ("finished recordin...")

			#stop Recording

			stream.stop_stream()
			stream.close()
			p.terminate()

			waveFile = wave.open(self.permanent_name, 'wb')
			waveFile.setnchannels(2)
			waveFile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
			waveFile.setframerate(44100)
			waveFile.writeframes(b''.join(frames))
			waveFile.close
			self.ciclu = False

	
	def play_the_wav(self):
		rp=1
		if self.repeateaudio == False:
			self.repeateaudio=True
			while self.playtheaudio == True and rp >=1:
				self.buttonBox.setEnabled(False)
				if self.permanent_name !="":
					wf = wave.open(self.permanent_name, 'rb')

					# instantiate PyAudio (1)
					p = pyaudio.PyAudio()

					# define callback (2)
					def callback(in_data, frame_count, time_info, status):
					    data = wf.readframes(frame_count)
					    return (data, pyaudio.paContinue)

					# open stream using callback (3)
					stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)

					# start the stream (4)
					stream.start_stream()

					# wait for stream to finish (5)
					while stream.is_active():
					    time.sleep(0.1)

					# stop stream (6)
					stream.stop_stream()
					stream.close()
					wf.close()

					# close PyAudio (7)
					p.terminate()
				rp -=1
			self.repeateaudio=False
		self.buttonBox.setEnabled(True)

	def playBUTTON(self):

		self.playtheaudio=True

		t1=Thread(target=self.play_the_wav)
		t1.start()

		for i in range(1,11):
			self.progressing_bar.setValue(i)
			time.sleep(1)
		time.sleep(0.2)	
		self.progressing_bar.setValue(0)	


	def activate(self):
		
		self.animatie=QPropertyAnimation(self.Regist,"geometry")
		self.animatie.setDuration(100)
		self.animatie.setStartValue(QRect(110,120,50,40))
		self.animatie.setEndValue(QRect(100,110,70,50))
		self.animatie.start()

		if (str(self.EnterEngleza.toPlainText())  and str(self.EnterSpaniola.toPlainText())) !="":
			t1=Thread(target=self.set_text)
			t2=Thread(target=self.deset_text)
			t1.start()
			t2.start()

			self.inchide_dialog = False
			
			name= "%s" % str(self.EnterEngleza.toPlainText())
			newname=""
			for i in name:
				if i.isalpha():
					if i.isupper():
						newname+=(i.lower())
					else:
						newname+=(i)

			self.permanent_name ="sunet/"+newname+".wav"
	
	def ok_button(self):

		bazadedate_connect = bazadedate
		if self.EnterEngleza.toPlainText !="" and self.EnterSpaniola.toPlainText !="" and self.permanent_name !="":
			bazadedate_connect.insert_text(self.EnterEngleza.toPlainText(),self.EnterSpaniola.toPlainText(),self.permanent_name)
			self.cancel_press()

class MainWindow(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.conecteaza_fereastra_doi=Fereastra_Doua(self)
		
		self.conecteaza_la_search=search

		self.setWindowTitle("Dictionar")
		self.setGeometry(100,100,600,400)
		self.engleza=QLabel('<b>Engleza</b>',self)
		self.engleza.setGeometry(50,15,60,20)
		self.spaniola=QLabel('<b>Spaniola</b>',self)
		self.spaniola.setGeometry(350,15,60,20)
		self.lista=QListWidget(self)
		self.lista.setStyleSheet("QListWidget{border:2px solid black;}")

		self.setStyleSheet("QListWidget::item {border-style: solid;border-width:1px;border-color:black;background-color: green;}")
		self.lista.setGeometry(50,50,200,200)
		self.lista.setSortingEnabled(True)
		self.lista.currentItemChanged.connect(self.info)
		self.lista2=QLabel(self)
		self.lista2.setGeometry(350,50,200,100)
		self.lista2.setStyleSheet("QLabel{border:2px solid black;}")
	
		self.butonAccept=QPushButton("Tradu",self)
		self.setStyleSheet('QPushButton { border: 2px solid #8f8f91;border-radius:8px;background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f6f7fa, stop: 1 #dadbde);min-width: 40px;}')
		self.butonAccept.clicked.connect(self.tradu_Textul)

		self.butonAccept.setGeometry(270,70,60,30)
		self.buttonAsculta=QPushButton("",self)
		self.buttonAsculta.setIcon(QIcon('pnguri/listen.png'))
		self.buttonAsculta.setIconSize(QSize(40,30))
		self.buttonAsculta.setToolTip('Asculta in Spaniola')
		self.buttonAsculta.setGeometry(500,160,20,30)
		self.buttonAsculta.setEnabled(False)
		self.buttonAsculta.clicked.connect(self.pune_piesa)
		self.butonAduga=QPushButton('Adauga',self)
		self.butonAduga.setGeometry(490,350,70,30)
		self.butonAduga.clicked.connect(self.fereastra_doi)


		for i in self.conecteaza_la_search.retrease_data():
			self.lista.addItem(i)

	
	def tradu_Textul(self):

		cautarea_efectuata=self.conecteaza_la_search.make_a_search(self.lista.currentItem().text())
		lista_de_tradus=[]

		for i in cautarea_efectuata:
			lista_de_tradus.append(i)

		for y,j in lista_de_tradus:
			text="<b>%s</b>" %y
			self.lista2.setText(text)
			self.de_ascultat=j
		
		if self.de_ascultat !="":
			self.buttonAsculta.setEnabled(True)
		else:
			self.buttonAsculta.setEnabled(False)

	def fereastra_doi(self):
		self.conecteaza_fereastra_doi.exec_()

	def pune_piesa(self):

		wf = wave.open(self.de_ascultat, 'rb')

		# instantiate PyAudio (1)
		p = pyaudio.PyAudio()

		# define callback (2)
		def callback(in_data, frame_count, time_info, status):
			data = wf.readframes(frame_count)
			return (data, pyaudio.paContinue)

		# open stream using callback (3)
		stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True,stream_callback=callback)

		# start the stream (4)
		stream.start_stream()

		# wait for stream to finish (5)
		while stream.is_active():
			time.sleep(0.1)

		# stop stream (6)
		stream.stop_stream()
		stream.close()
		wf.close()

		# close PyAudio (7)
		p.terminate()

	def info(self):

			 
		print (self.lista.currentItem().text())
	
	def run(self):
		self.show()
		aplicatie.exec_()

app=MainWindow()
app.run()








