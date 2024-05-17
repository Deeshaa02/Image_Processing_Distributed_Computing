import threading
import queue
import cv2
from mpi4py import MPI
import numpy as np

class WorkerThread(threading.Thread):

    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()



    def run(self):
        while True:
            try:
                task = self.task_queue.get(block=False)
                print(f"Slave{self.rank-1} task{task[2]}")
            except queue.Empty:
                task = None
            if task is None:
                print(f"worker {self.rank-1} exiting")
                break
            image, operation ,id = task
            result = self.process_image(image, operation,id)
            self.send_result(result)

    def process_image(self, image_path, operation,id):
        global result
        img = image_path

        if operation == 'Edge Detection':
            result = cv2.Canny(img, 100, 200)
        elif operation == 'Color Inversion':
            result = cv2.bitwise_not(img)
        elif operation == 'Blurring':
            result = cv2.medianBlur(img, 21)
        elif operation == 'Thresholding':
            result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif operation == 'Sharpening':
            sharp_kernel = np.array([[0, -1, 0],
                                     [-1, 5, -1],
                                     [0, -1, 0]])
            result = cv2.filter2D(src=img, ddepth=-1, kernel=sharp_kernel)
        elif operation == 'Opening':
            image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((3, 3), np.uint8)
            dilated = cv2.dilate(image_gray, kernel, iterations=2)
            eroded = cv2.erode(image_gray, kernel, iterations=2)
            result = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, kernel)
        elif operation == 'Image Enhancement':
            min_val = np.min(img)
            max_val = np.max(img)
            result = cv2.convertScaleAbs(img, alpha=255.0 / (max_val - min_val),
                                         beta=-255.0 * min_val / (max_val - min_val))
        else:
            print("Invalid operation:", operation)
            return None

        return result,id

    def send_result(self, result):
        self.comm.send(result, dest=0)


