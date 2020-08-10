import pafy
import sys
import datetime
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ui import *
from hurry.filesize import size
class GUI(Ui_MainWindow):
	def __init__(self,window):
		self.setupUi(window)
		self.window = window
		self.VerifyBtn.clicked.connect(self.verify)
		self.FolderBtn.clicked.connect(self.selectDest)
		self.DownloadBtn.clicked.connect(self.download)
		self.NormalRadio.toggled.connect(self.NormalToggle)
		self.VideoRadio.toggled.connect(self.VideoToggle)
		self.AudioRadio.toggled.connect(self.AudioToggle)
	def verify(self):
		try:
			self.NormalList.clear()
			self.VideoList.clear()
			self.AudioList.clear()
			self.url = self.UrlInput.text()
			self.video = pafy.new(self.url)
			self.Title .setText('Video Title :  '+self.video.title)
			self.Duration.setText('Video Length :  '+str(datetime.timedelta(seconds=self.video.length)))
			self.NormalLoad()
			self.VideoLoad()
			self.AudioLoad()
			self.Title.setEnabled(True)
			self.Duration.setEnabled(True)
			self.DestInput.setEnabled(True)
			self.FolderBtn.setEnabled(True)
			self.ProgressLabel.setEnabled(True)
			self.ProgressBar.setEnabled(True)
			self.AudioRadio.setEnabled(True)
			self.VideoRadio.setEnabled(True)
		except Exception as error:
			QMessageBox.warning(self.window,'Error',error.__str__())
	def NormalLoad(self):
		self.NormalList.setEnabled(True)
		self.NormalRadio.setEnabled(True)
		for i in self.video.streams:
			self.NormalList.addItem(i.resolution+' ('+size(i.get_filesize())+') '+i.extension)
	def VideoLoad(self):
		self.VideoList.setEnabled(True)
		for i in self.video.videostreams:
			self.VideoList.addItem(i.resolution+' ('+size(i.get_filesize())+') '+i.extension)
	def AudioLoad(self):
		self.AudioList.setEnabled(True)
		for i in self.video.audiostreams:
			self.AudioList.addItem(i.bitrate+' ('+size(i.get_filesize())+') '+i.extension)
	def NormalToggle(self):
		if self.NormalRadio.isChecked():
			self.NormalLoad()
			self.VideoList.setEnabled(False)
			self.AudioList.setEnabled(False)
	def VideoToggle(self):
		if self.VideoRadio.isChecked():
			self.VideoLoad()
			self.NormalList.setEnabled(False)
			self.AudioList.setEnabled(False)
	def AudioToggle(self):
		if self.AudioRadio.isChecked():
			self.AudioLoad()
			self.NormalList.setEnabled(False)
			self.VideoList.setEnabled(False)		

	def selectDest(self):
		try:
			self.Dest = QFileDialog.getExistingDirectory(self.window,'Select destination','')
			self.DestInput.setText(self.Dest)
			self.DownloadBtn.setEnabled(True)
		except Exception as error:
			QMessageBox.warning(self.window,'Error',error.__str__())
	def download(self):
		if(self.Dest==''):
			self.selectDest()
		else:
			if self.NormalRadio.isChecked():
				self.NormalDownload()
			elif self.VideoRadio.isChecked():
				self.VideoDownload()
			elif self.AudioRadio.isChecked():
				self.AudioDownload()
	def reset(self):
		self.ProgressBar.setProperty('value',0)
	def NormalDownload(self):
		try:
			stream = self.video.streams[self.NormalList.currentIndex()]
			stream.download(filepath=self.Dest,callback=self.progress)
			QMessageBox.information(self.window,'Success','Video downloaded successfully')
			self.reset()
		except Exception as error:
			QMessageBox.warning(self.window,'Error',error.__str__())
	def VideoDownload(self):
		try:
			stream = self.video.videostreams[self.VideoList.currentIndex()]
			stream.download(filepath=self.Dest,callback=self.progress)
			QMessageBox.information(self.window,'Success','Video downloaded successfully')
			self.reset()
		except Exception as error:
			QMessageBox.warning(self.window,'Error',error.__str__())
	def AudioDownload(self):
		try:
			stream = self.video.audiostreams[self.AudioList.currentIndex()]
			stream.download(filepath=self.Dest,callback=self.progress)
			QMessageBox.information(self.window,'Success','Audio downloaded successfully')
			self.reset()
		except Exception as error:
			QMessageBox.warning(self.window,'Error',error.__str__())
	def progress(a,value,c,d,e,f):
		self.ProgressBar.value+=value
	def progress(self,a,b,c,d,e):
		x = c*100
		self.ProgressBar.setProperty("value",x)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
