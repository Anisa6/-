import math
from time import time

from defines import *

class Gestures:
    start_watch_time = 0
    start_watch_counter = 0

    stop_watch_time = 0
    stop_watch_counter = 0
    stop_watch_REYE = (0, 0)
    stop_watch_LEYE = (0, 0)

    exit_watch_time = 0
    exit_watch_counter = 0
    exit_start_pos = 0
    flag_right = 0
    flag_left = 0


    @staticmethod
    def FindDistance(p1, p2):
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def watch(p1, p2):
        result = False
        if int(Gestures.FindDistance(p1, p2)) < 30:
            # расположение ключевых точек подходит для жеста
            if Gestures.start_watch_time == 0:
                Gestures.start_watch_time = int(time() * 1000) # предполагаемое начало жеста
                Gestures.start_watch_counter = 1
                #print('предполагаемое начало жеста')
            elif int(time() * 1000) - Gestures.start_watch_time < 1000:
                # Если с момента предполагаемого начала жеста прошло менее секунды
                Gestures.start_watch_counter += 1
                #print('с момента предполагаемого начала жеста прошло менее секунды')
            elif 1000 < int(time() * 1000) - Gestures.start_watch_time < 2000:
                # если с начала жеста прошло от 1 до 2 секунд
                #print('с начала жеста прошло от 1 до 2 секунд')
                if Gestures.start_watch_counter > 1:
                    # Если за время с начала жеста ключевые точки были близки более 1 раза
                    Gestures.start_watch_time = 0
                    Gestures.start_watch_counter = 0
                    # print('включаем слежение')
                    result = True
            else:
                # Если прошло более 2 секунд, а жест еще не сработал
                Gestures.start_watch_time = 0
                Gestures.start_watch_counter = 0
                #print('прошло более 2 секунд, а жест еще не сработал')
            #print(int(Gestures.FindDistance(p1, p2)), Gestures.start_watch_counter)

        return result
    
    

    @staticmethod
    def stop_watch(fingers, face):
        result = False
        if len(face) > 0:
            Gestures.stop_watch_REYE = face[RIGHT_EYE]
            Gestures.stop_watch_LEYE = face[LEFT_EYE]
        else:
            f_points = [fingers[0]]
            f_points.extend(fingers[5:])
            xList = [p[0] for p in f_points]
            yList = [p[1] for p in f_points]
            x_min, x_max = min(xList), max(xList)
            y_min, y_max = min(yList), max(yList)
            #print(Gestures.stop_watch_REYE, Gestures.stop_watch_LEYE)
            #print(x_min, y_min, x_max, y_max)
            if x_min < Gestures.stop_watch_REYE[0] < x_max and y_min < Gestures.stop_watch_REYE[1] < y_max and \
                x_min < Gestures.stop_watch_LEYE[0] < x_max and y_min < Gestures.stop_watch_LEYE[1] < y_max:
                # print('???')
                if Gestures.stop_watch_time == 0:
                    print('предполагаемое начало жеста')
                    Gestures.stop_watch_time = int(time() * 1000)  # предполагаемое начало жеста
                    Gestures.stop_watch_counter = 1
                elif int(time() * 1000) - Gestures.stop_watch_time < 1000:
                    # Если с момента предполагаемого начала жеста прошло менее секунды
                    Gestures.stop_watch_counter += 1
                elif 1000 < int(time() * 1000) - Gestures.stop_watch_time < 2000:
                    # если с начала жеста прошло от 1 до 2 секунд
                    if Gestures.stop_watch_counter > 1:
                        # Если за время с начала жеста ключевые точки были близки более 1 раза
                        Gestures.stop_watch_time = 0
                        Gestures.stop_watch_counter = 0
                        # print('выключаем слежение')
                        result = True
                else:
                    # Если прошло более 2 секунд, а жест еще не сработал
                    Gestures.stop_watch_time = 0
                    Gestures.stop_watch_counter = 0
        return result

    @staticmethod
    def sound(f8, r_ear):
        result = False
        if len_between(f8, r_ear) < 20:
            result = True
        return result

    @staticmethod
    def do_exit(htm):
        result = False
        #if len_between(htm[16],htm[0]) < 90:
            #result = True
        return result





def len_between(p1, p2):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    return math.hypot(x2 - x1, y2 - y1)

