import cv2


class DetectionModel:
    def __init__(self):
        net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

        self._model = cv2.dnn_DetectionModel(net)
        self._model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

    def detect(self, frame, conf_threshold, nms_threshold):
        return self._model.detect(frame, conf_threshold, nms_threshold)
