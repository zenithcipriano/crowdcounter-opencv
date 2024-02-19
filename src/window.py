import cv2
import math

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QImage, QIntValidator, QPixmap
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from src.counter import PersonGridCounter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._setupUi()
        self._capture = cv2.VideoCapture(0)
        self._personGridCounter = PersonGridCounter()

    def _setupUi(self):
        self.setWindowTitle("")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        centralWidget.setMaximumHeight(
            math.floor(QDesktopWidget().screenGeometry().height() * 0.8)
        )

        self._image = QLabel(self)
        self._image.setAlignment(Qt.AlignCenter)

        rowCountLabel = QLabel("Number of rows: ")
        rowCountLabel.setFont(QFont("Arial", 12))

        rowCountInput = QLineEdit()
        rowCountInput.setValidator(QIntValidator())
        rowCountInput.textChanged.connect(self._setRowCount)

        columnCountLabel = QLabel("Number of columns: ")
        columnCountLabel.setFont(QFont("Arial", 12))

        columnCountInput = QLineEdit()
        columnCountInput.setValidator(QIntValidator())
        columnCountInput.textChanged.connect(self._setColumnCount)

        headerLayout = QHBoxLayout()
        headerLayout.addWidget(rowCountLabel)
        headerLayout.addWidget(rowCountInput)
        headerLayout.addWidget(columnCountLabel)
        headerLayout.addWidget(columnCountInput)

        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(32, 32, 32, 32)
        mainLayout.setSpacing(32)
        mainLayout.addLayout(headerLayout)
        mainLayout.addWidget(self._image)

    def _setRowCount(self, rowCount):
        if rowCount == "":
            rowCount = 1
        self._personGridCounter.setRowCount(int(rowCount))

    def _setColumnCount(self, columnCount):
        if columnCount == "":
            columnCount = 1
        self._personGridCounter.setColumnCount(int(columnCount))

    def startLoop(self):
        timer = QTimer(self)
        timer.timeout.connect(self._updateFrame)
        timer.start(17)

    def _updateFrame(self):
        ret, frame = self._capture.read()
        if ret == False:
            return

        self._personGridCounter.count(frame)
        self._display(frame)

    def _display(self, frame):
        frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qImage = QImage(
            frameRgb.data,
            frameRgb.shape[1],
            frameRgb.shape[0],
            QImage.Format_RGB888,
        )
        pixmap = QPixmap.fromImage(qImage)
        self._image.setPixmap(pixmap)
