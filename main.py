import sys
import requests
from io import BytesIO

from PIL import Image, ImageQt
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel


class MapAPI(QMainWindow):
    map_l_list = ('map', 'sat', 'sat,skl')
    pt_configuration = 'pm2bll'

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        # self.setupUi(self)
        # self.retranslateUi(self)
        self.viewComboBox.addItems(['Карта', 'Спутник', 'Гибрид'])
        self.viewComboBox.currentIndexChanged.connect(self.get_image)

        self.map_ll = (37.530887, 55.703118)
        self.map_spn = (0.01, 0.01)
        # self.map_l = self.map_l_list[0]
        self.map_pt = []

        self.get_image()

    def get_image(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={','.join(map(str, self.map_ll))}&" \
                      f"spn={','.join(map(str, self.map_spn))}&l={self.map_l_list[self.viewComboBox.currentIndex()]}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.image = ImageQt.ImageQt(Image.open(BytesIO(response.content)))
        self.map_label.setPixmap(QPixmap.fromImage(self.image))

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
