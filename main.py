import sys
from io import BytesIO

import requests

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from useful_functions.geocoder3 import get_coordinates, geocode


class MapAPI(QMainWindow):
    map_l_list = ('map', 'sat', 'sat,skl')
    pt_type = 'pm2bll'
    image_width, image_height = 600, 450

    def __init__(self):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        self.map_l.addItems(['Карта', 'Спутник', 'Гибрид'])
        self.map_l.currentIndexChanged.connect(self.set_image)
        self.search_btn.clicked.connect(self.search)
        self.refresh_btn.clicked.connect(self.refresh)
        self.index_btn.toggled.connect(self.set_index)

        self.cur_address = []

        self.map_ll = [37.530887, 55.703118]
        self.ll_delta = 0.001
        self.map_spn = 0.01
        self.spn_delta = 0.0001
        self.map_pt = tuple()

        self.set_image()
        self.setFocusPolicy(Qt.StrongFocus)  # necessary for keyboard events
        self.image.setFocus()

    def set_image(self):
        params = {
            'll': ','.join(map(str, self.map_ll)),
            'spn': f'{self.map_spn},{self.map_spn}',
            'l': self.map_l_list[self.map_l.currentIndex()],
            'pt': ','.join(map(str, self.map_pt)) + ',' + self.pt_type if self.map_pt else self.map_pt
        }
        map_request = 'http://static-maps.yandex.ru/1.x/'
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.img = ImageQt(Image.open(BytesIO(response.content)))
        self.image.setPixmap(QPixmap.fromImage(self.img))

    def keyPressEvent(self, event):
        self.statusbar.showMessage('')
        if event.key() == Qt.Key_PageUp and self.map_spn + self.spn_delta <= 90:
            self.map_spn = (self.map_spn + self.spn_delta) % 90
        elif event.key() == Qt.Key_PageDown and self.map_spn - self.spn_delta >= -90:
            self.map_spn = (self.map_spn - self.spn_delta) % 90
        elif event.key() == Qt.Key_Up:
            self.map_ll[1] = (self.map_ll[1] + self.ll_delta) % (90 if self.map_ll[1] > 0 else -90)
        elif event.key() == Qt.Key_Down and self.map_ll[1] - self.ll_delta >= -90:
            self.map_ll[1] = (self.map_ll[1] - self.ll_delta) % (90 if self.map_ll[1] > 0 else -90)
        elif event.key() == Qt.Key_Left and self.map_ll[0] - self.ll_delta >= -180:
            self.map_ll[0] = (self.map_ll[0] - self.ll_delta) % (180 if self.map_ll[1] > 0 else -180)
        elif event.key() == Qt.Key_Right and self.map_ll[0] + self.ll_delta <= 180:
            self.map_ll[0] = (self.map_ll[0] + self.ll_delta) % (180 if self.map_ll[1] > 0 else -180)
        self.set_image()

    def get_click_ll(self, x, y):
        focused_widget = QApplication.focusWidget()
        focused_widget.clearFocus()  # to get absolute image position
        lon = float()
        lat = float()
        self.map_pt = (lon, lat)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.get_click_ll(event.x(), event.y())
            self.set_image()
        elif event.button() == Qt.RightButton:
            pass

    def search(self):
        self.statusbar.showMessage('')
        try:
            self.map_ll = list(get_coordinates(self.search_bar.text()))
            self.map_pt = get_coordinates(self.search_bar.text())
            self.cur_address = [geocode(self.search_bar.text())['metaDataProperty']['GeocoderMetaData']['text']]
            if 'postal_code' in geocode(self.search_bar.text())['metaDataProperty']['GeocoderMetaData']['Address']:
                self.cur_address.append(geocode(self.search_bar.text())['metaDataProperty']['GeocoderMetaData']
                                        ['Address']['postal_code'])
            self.address_label.setText(self.cur_address[0])
            self.set_index(self.index_btn.isChecked())
            self.set_image()
        except RuntimeError as error:
            self.statusbar.showMessage(str(error))

    def refresh(self):
        self.statusbar.showMessage('')
        self.map_pt = tuple()
        self.cur_address = []
        self.search_bar.setText('')
        self.address_label.setText('')
        self.set_image()

    def set_index(self, selected):
        if selected and self.cur_address:
            self.address_label.setText(', '.join(self.cur_address))
        elif self.cur_address:
            self.address_label.setText(self.cur_address[0])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MapAPI()
    ex.show()
    sys.exit(app.exec())
