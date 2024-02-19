import cv2
from config import COLORS, CONF_THRESHOLD, NMS_THRESHOLD
from src.model import DetectionModel


class PersonGridCounter:
    def __init__(self):
        self._loadClasses()
        self._model = DetectionModel()
        self._rowCount = 1
        self._columnCount = 1

    def setRowCount(self, rowCount):
        self._rowCount = rowCount

    def setColumnCount(self, columnCount):
        self._columnCount = columnCount

    def _loadClasses(self):
        with open("classes.txt", "r") as classesFile:
            self._classNames = [
                className.strip() for className in classesFile.readlines()
            ]

    def count(self, frame):
        height, width, _ = frame.shape
        self._cellWidth = width // self._columnCount
        self._cellHeight = height // self._rowCount

        personCount = [
            [0 for j in range(self._columnCount)] for i in range(self._rowCount)
        ]

        self._drawGrid(frame)

        classes, scores, boxes = self._model.detect(
            frame, CONF_THRESHOLD, NMS_THRESHOLD
        )

        for classId, score, box in zip(classes, scores, boxes):
            className = self._classNames[classId]
            if className != "person":
                continue

            personRowIndex = 0
            personColumnIndex = 0
            personX = box[0] + box[2] // 2
            personY = box[1] + box[3] // 2

            for rowIndex in range(self._rowCount):
                rowBound = self._cellHeight * (rowIndex + 1)
                if personY < rowBound:
                    personRowIndex = rowIndex
                    break

            for columnIndex in range(self._columnCount):
                columnBound = self._cellWidth * (columnIndex + 1)
                if personX < columnBound:
                    personColumnIndex = columnIndex
                    break

            personCount[personRowIndex][personColumnIndex] += 1

            color = COLORS[int(classId) % len(COLORS)]
            cv2.circle(frame, (personX, personY), 4, color, 8)

        for rowIndex in range(self._rowCount):
            for columnIndex in range(self._columnCount):
                cv2.putText(
                    frame,
                    f"Persons: {personCount[rowIndex][columnIndex]}",
                    (
                        self._cellWidth * columnIndex + 8,
                        self._cellHeight * rowIndex + 32,
                    ),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.6,
                    (255, 0, 0),
                    2,
                )

    def _drawGrid(self, frame):
        for rowIndex in range(self._rowCount):
            for columnIndex in range(self._columnCount):
                cellStartPoint = (
                    self._cellWidth * columnIndex,
                    self._cellHeight * rowIndex,
                )
                cellEndPoint = (
                    self._cellWidth * (columnIndex + 1),
                    self._cellHeight * (rowIndex + 1),
                )
                cv2.rectangle(frame, cellStartPoint, cellEndPoint, (0, 0, 0), 1)
