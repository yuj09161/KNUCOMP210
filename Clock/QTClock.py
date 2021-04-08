USE_QT6 = False

if USE_QT6:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import (
        QMainWindow, QApplication, QSizePolicy,
        QWidget, QGridLayout, QHBoxLayout,
        QLabel, QPushButton, QLCDNumber, QSpacerItem
    )
else:
    from PySide2.QtCore import QTimer
    from PySide2.QtWidgets import (
        QMainWindow, QApplication, QSizePolicy,
        QWidget, QGridLayout, QHBoxLayout,
        QLabel, QPushButton, QLCDNumber, QSpacerItem
    )

TITLE = f'Simple Digital Clock (with PySide{USE_QT6 * 4 + 2})'

import datetime  # noqa: E402


sizePolicy_EE = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
sizePolicy_EE.setHorizontalStretch(0)
sizePolicy_EE.setVerticalStretch(0)

sizePolicy_ME = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
sizePolicy_ME.setHorizontalStretch(0)
sizePolicy_ME.setVerticalStretch(0)

sizePolicy_PF = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
sizePolicy_PF.setHorizontalStretch(0)
sizePolicy_PF.setVerticalStretch(0)


class ClockUi:
    def setupUi(self, Clock):
        # pylint: disable = attribute-defined-outside-init
        # pylint: disable = redefined-outer-name

        Clock.setWindowTitle(TITLE)
        Clock.resize(600, 200)

        self.centralWidget = QWidget(Clock)
        self.glCent = QGridLayout(self.centralWidget)

        self.lcd = QLCDNumber(self.centralWidget)
        self.lcd.setDigitCount(8)
        sizePolicy_EE.setHeightForWidth(
            self.lcd.sizePolicy().hasHeightForWidth()
        )
        self.lcd.setSizePolicy(sizePolicy_EE)
        self.glCent.addWidget(self.lcd, 0, 0, 2, 1)

        self.lbTitleAM = QLabel(self.centralWidget)
        sizePolicy_ME.setHeightForWidth(
            self.lbTitleAM.sizePolicy().hasHeightForWidth()
        )
        self.lbTitleAM.setSizePolicy(sizePolicy_ME)
        self.glCent.addWidget(self.lbTitleAM, 0, 1)

        self.lbAM = QLabel(self.centralWidget)
        sizePolicy_ME.setHeightForWidth(
            self.lbAM.sizePolicy().hasHeightForWidth()
        )
        self.lbAM.setSizePolicy(sizePolicy_ME)
        self.glCent.addWidget(self.lbAM, 0, 2)

        self.lbTitlePM = QLabel(self.centralWidget)
        sizePolicy_ME.setHeightForWidth(
            self.lbTitlePM.sizePolicy().hasHeightForWidth()
        )
        self.lbTitlePM.setSizePolicy(sizePolicy_ME)
        self.glCent.addWidget(self.lbTitlePM, 1, 1)

        self.lbPM = QLabel(self.centralWidget)
        sizePolicy_ME.setHeightForWidth(
            self.lbPM.sizePolicy().hasHeightForWidth()
        )
        self.lbPM.setSizePolicy(sizePolicy_ME)
        self.glCent.addWidget(self.lbPM, 1, 2)

        self.widAMPM = (self.lbTitleAM, self.lbTitlePM, self.lbAM, self.lbPM)

        self.widBot = QWidget(self.centralWidget)
        sizePolicy_PF.setHeightForWidth(
            self.widBot.sizePolicy().hasHeightForWidth()
        )
        self.widBot.setSizePolicy(sizePolicy_PF)
        self.hlBot = QHBoxLayout(self.widBot)
        self.hlBot.setContentsMargins(0, 0, 0, 0)

        self.hlBot.addItem(
            QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )

        self.btnChange = QPushButton(self.widBot)
        self.hlBot.addWidget(self.btnChange)

        Clock.setCentralWidget(self.centralWidget)

        self.retranslateUi()

    def retranslateUi(self):
        self.lbTitleAM.setText('AM')
        self.lbTitlePM.setText('PM')

        self.btnChange.setText('12/24시간제 변경')

        self.lbTitleAM.setStyleSheet('font-size: 20px')
        self.lbTitlePM.setStyleSheet('font-size: 20px')
        self.lbAM.setStyleSheet('font-size: 35px')
        self.lbPM.setStyleSheet('font-size: 35px')


class Clock(QMainWindow, ClockUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__is_24 = False

        self.__refresh_12 = QTimer(self)
        self.__refresh_12.setInterval(250)
        self.__refresh_12.timeout.connect(self.__refresh_time_12)

        self.__refresh_24 = QTimer(self)
        self.__refresh_24.setInterval(250)
        self.__refresh_24.timeout.connect(self.__refresh_time_24)
        self.__refresh_24.start()

        self.btnChange.clicked.connect(self.__toggle_12_24)

        self.__toggle_12_24()

    def __toggle_12_24(self):
        if self.__is_24:
            for wid in self.widAMPM:
                wid.hide()

            self.__refresh_24.stop()
            self.__refresh_12.start()

            self.glCent.removeWidget(self.widBot)
            self.glCent.addWidget(self.widBot, 2, 0, 1, 1)

            self.__refresh_time_12()
            self.__is_24 = False
        else:
            for wid in self.widAMPM:
                wid.show()

            self.__refresh_12.stop()
            self.__refresh_24.start()

            self.glCent.removeWidget(self.widBot)
            self.glCent.addWidget(self.widBot, 2, 0, 1, 3)

            self.__refresh_time_24()
            self.__is_24 = True

    def __refresh_time_24(self):
        lcd_str, am_pm =\
            datetime.datetime.now().strftime('%I:%M:%S %p').split(' ')
        self.lcd.display(lcd_str)
        if am_pm == 'AM':
            self.lbAM.setText('●')
            self.lbPM.setText('○')
        else:
            self.lbAM.setText('○')
            self.lbPM.setText('●')

    def __refresh_time_12(self):
        self.lcd.display(datetime.datetime.now().strftime('%H:%M:%S'))


if __name__ == '__main__':
    app = QApplication()

    clock = Clock()
    clock.show()

    app.exec_()
