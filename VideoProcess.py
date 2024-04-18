import cv2
import mediapipe as mp
import pyautogui as pag
from defines import *

from Gestures import Gestures as gesture, len_between


class VideoProcessing:
    HandLandmark = list()
    FaceLandmark = list()
    wCam, hCam = 1280, 720

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    mp_draw = mp.solutions.drawing_utils

    mp_face = mp.solutions.face_detection
    face = mp_face.FaceDetection(min_detection_confidence=0.8)


    watch = False   # Флаг следить / не следить за жестами

    @staticmethod
    def take_hand_points(img, h, w):
        results_hand = VideoProcessing.hands.process(img)
        if results_hand.multi_hand_landmarks is not None:
            for handLms in results_hand.multi_hand_landmarks:
                VideoProcessing.HandLandmark = [(int(point.x * w), int(point.y * h)) for point in handLms.landmark]
                # x_mouse, y_mouse = VideoProcessing.HandLandmark[0]
                # pag.moveTo(x_mouse, y_mouse)
                #if VideoProcessing.HandLandmark[4][0] - VideoProcessing.HandLandmark[20][0] and VideoProcessing.HandLandmark[4][1] - VideoProcessing.HandLandmark[20][1] < 10:
                # print(len_between(VideoProcessing.HandLandmark[4], VideoProcessing.HandLandmark[12]))
                # if len_between(VideoProcessing.HandLandmark[4], VideoProcessing.HandLandmark[12]) < 20:
                #     pag.click()
                #     print('клик')

        else:
            VideoProcessing.HandLandmark = list()


    @staticmethod
    def take_face_points(img, h, w):
        results_face = VideoProcessing.face.process(img)
        if results_face.detections is not None:
            for face in results_face.detections:
                if face.score[0] > 0.80:
                    landmarks = face.location_data.relative_keypoints
                    VideoProcessing.FaceLandmark = [(int(landmark.x * w), int(landmark.y * h)) for landmark in
                                                    landmarks]


        else:
            VideoProcessing.FaceLandmark = list()


    @staticmethod
    def process():
        _, img = VideoProcessing.cap.read()
        img = cv2.flip(img, 1)

        imgBGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        h, w = img.shape[:2]

        VideoProcessing.take_hand_points(imgBGR, h, w)
        VideoProcessing.take_face_points(imgBGR, h, w)

        for point in VideoProcessing.HandLandmark:
            cx, cy = point
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        results_hand = VideoProcessing.hands.process(imgBGR)
        if results_hand.multi_hand_landmarks is not None:
            for handLms in results_hand.multi_hand_landmarks:
                VideoProcessing.mp_draw.draw_landmarks(img, handLms, VideoProcessing.mp_hands.HAND_CONNECTIONS)

        for point in VideoProcessing.FaceLandmark:
            img = cv2.circle(img, point, 10, (0, 255, 255), -1)


        # xmin, xmax = min(xLst), max(xLst)
        # ymin, ymax = min(yLst), max(yLst)
        # box = xmin, ymin, xmax, ymax
        #
        # cv2.rectangle(img, (box[0] - 20, box[1] - 20), (box[2] + 20, box[3] + 20), (0, 255, 0), 2)

        # Кодиить здесь!!!!
        cv2.imshow('video', img)
        if cv2.waitKey(1) == ord('q'):
            pass


    @staticmethod
    def check_watch():
        if not VideoProcessing.watch:
            #print(len(VideoProcessing.HandLandmark), len(VideoProcessing.FaceLandmark))
            if len(VideoProcessing.HandLandmark) > 0 and len(VideoProcessing.FaceLandmark) > 0:
                if gesture.watch(VideoProcessing.HandLandmark[8], VideoProcessing.FaceLandmark[RIGHT_EYE]):
                    VideoProcessing.watch = True

        return VideoProcessing.watch

    @staticmethod
    def check_stop_watch():
        # TODO реализовать распознавание жеста "НЕ Следить  за жестами"
        if len(VideoProcessing.HandLandmark) > 0:
            if gesture.stop_watch(VideoProcessing.HandLandmark, VideoProcessing.FaceLandmark):
                VideoProcessing.watch = False
        return not VideoProcessing.watch


    @staticmethod
    def check_exit():
        # TODO реализовать распознавание жеста "Выход из программы"
        if len(VideoProcessing.HandLandmark) > 0:
            if gesture.do_exit(VideoProcessing.HandLandmark) == True:
                return True
        return False
    

    @staticmethod
    def sound_process():
        result = False
        if len(VideoProcessing.HandLandmark) > 0 and len(VideoProcessing.FaceLandmark) > 0:
            if gesture.sound(VideoProcessing.HandLandmark[8],
                          VideoProcessing.FaceLandmark[RIGHT_EAR]):
                result = True
        return result


    @staticmethod
    def mouse_move():
        if len(VideoProcessing.HandLandmark) > 0:
            x_mouse, y_mouse = VideoProcessing.HandLandmark[0]
            pag.moveTo(x_mouse, y_mouse)

    @staticmethod
    def mouse_left_click():
        if len(VideoProcessing.HandLandmark) > 0:
            if len_between(VideoProcessing.HandLandmark[4], VideoProcessing.HandLandmark[12]) < 20:
                pag.click()
                print('клик')



def main():
    vp = VideoProcessing()

    vp.process()
    #print(vp.HandLandmark)
    #print(vp.FaceLandmark)




if __name__ == "__main__":
    main()

