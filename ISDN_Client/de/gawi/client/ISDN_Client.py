import sys
import PyQt4
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSlot, QUrl
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebView

html = """
<html>
<body>
    <h1>Hello!</h1><br>
    <h2><a href="#" onclick="printer.text('Message from QWebView')">QObject Test</a></h2>
    <h2><a href="#" onclick="alert('Javascript works!')">JS test</a></h2>
</body>
</html>
"""

app = QApplication(sys.argv)
view = QWebView()

class PreviewWindow(PyQt4.QtGui.QWidget):
    def __init__(self, parent=None):
        super(PreviewWindow, self).__init__(parent)

        self.label = QtGui.QLabel("Nachricht!")

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setWindowTitle("Preview")

    def mousePressEvent(self, event):
        print "mouse"
        self.close()

class ConsolePrinter(QObject):
    def __init__(self, parent=None):
        super(ConsolePrinter, self).__init__(parent)

    @pyqtSlot(str)
    def text(self, message):
        print message
        flags = QtCore.Qt.ToolTip
        flags |= QtCore.Qt.WindowStaysOnTopHint
        previewWindow = PreviewWindow(view)
        previewWindow.setWindowFlags(flags)
        previewWindow.show()
        print "now"

printer = ConsolePrinter()

def loadJavaScriptObjects():
    frame.addToJavaScriptWindowObject('printer', printer)

if __name__ == '__main__':
    #app = QApplication(sys.argv)
    #view = QWebView()
    frame = view.page().mainFrame()
    #printer = ConsolePrinter()
    #view.setHtml(html)
    QtCore.QObject.connect(frame, QtCore.SIGNAL('javaScriptWindowObjectCleared()'), loadJavaScriptObjects)
    view.load(QUrl('http://localhost:8080/Vaadin_remote_executor/?debug'))
    #frame.addToJavaScriptWindowObject('printer', printer)
    frame.evaluateJavaScript("alert('Hello');")
    #frame.evaluateJavaScript("printer.text('Goooooooooo!');")
    view.show()
    app.exec_()