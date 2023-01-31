import sys
import requests

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication


class MapAPI(QMainWindow):
    map_l_list = ('map', 'sat', 'sat,skl')
    pt_configuration = 'pm2bll'

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.viewComboBox.addItems(['Карта', 'Спутник', 'Гибрид'])
        self.viewComboBox.currentIndexChanged.connect(self.get_image)

        self.map_ll = [37.530887, 55.703118]
        self.ll_delta = 0.001
        self.map_spn = [0.01, 0.01]
        self.spn_delta = 0.001
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

        map_file = "map.png"
        try:
            with open(map_file, "wb") as file:
                file.write(response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)

        a = ImageQt(map_file)
        pixmap = QPixmap.fromImage(a)
        self.map_label.setPixmap(pixmap)

        # self.image = ImageQt.ImageQt(Image.open(BytesIO(response.content)))
        # self.map_label.setPixmap(QPixmap.fromImage(self.image))

    # def mouseMoveEvent(self, event):
    #     self.coords.setText(f"Координаты: {event.x()}, {event.y()}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.map_spn[0] = (self.map_spn[0] + self.spn_delta) % 90
            self.map_spn[1] = (self.map_spn[1] + self.spn_delta) % 90
        elif event.key() == Qt.Key_PageDown:
            self.map_spn[0] = (self.map_spn[0] - self.spn_delta) % 90
            self.map_spn[1] = (self.map_spn[1] - self.spn_delta) % 90
        elif event.key() == Qt.Key_Up:
            self.map_ll[1] = (self.map_ll[1] + self.ll_delta) % (90 if self.map_ll[1] > 0 else -90)
        elif event.key() == Qt.Key_Down:
            self.map_ll[1] = (self.map_ll[1] - self.ll_delta) % (90 if self.map_ll[1] > 0 else -90)
        elif event.key() == Qt.Key_Left:
            self.map_ll[0] = (self.map_ll[0] + self.ll_delta) % (180 if self.map_ll[1] > 0 else -180)
        elif event.key() == Qt.Key_Right:
            self.map_ll[0] = (self.map_ll[0] - self.ll_delta) % (180 if self.map_ll[1] > 0 else -180)
        self.get_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MapAPI()
    ex.show()
    sys.exit(app.exec())
