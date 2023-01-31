import sys
import requests

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


class MapAPI(QMainWindow):
    map_l_list = ('map', 'sat', 'sat,skl')

    def __init__(self):
        super().__init__()
        uic.loadUi('', self)
        # self.setupUi(self)
        # self.retranslateUi(self)

        self.map_ll = (30.0, 30.0)
        self.mpa_spn = (0.01, 0.01)
        self.map_l = self.map_l_list[0]

    # def mouseMoveEvent(self, event):
    #     self.coords.setText(f"Координаты: {event.x()}, {event.y()}")

    def keyPressEvent(self, event):
        if event.key == Qt.Key_PageUp:
            pass
        elif event.key == Qt.Key_PageDown:
            pass
        elif event.key == Qt.Key_Up:
            pass
        elif event.key == Qt.Key_Down:
            pass
        elif event.key == Qt.Key_Left:
            pass
        elif event.key == Qt.Key_Right:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapAPI()
    ex.show()
    sys.exit(app.exec())
