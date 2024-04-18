from VideoProcess import VideoProcessing as vp
from Actions import SoundVolume as sv
from Gestures import len_between


while True:
    vp.process()
    # print(vp.HandLandmark)
    # print(vp.FaceLandmark)

    if vp.check_watch():
        # print('следим')
        vp.mouse_move()
        vp.mouse_left_click()
        if vp.check_stop_watch():
            continue
        elif vp.sound_process():
            #print('sound')
            dist = len_between(vp.HandLandmark[4], vp.HandLandmark[8])
            #print(vp.HandLandmark[4],vp.HandLandmark[8], dist)
            sv.change(dist)

        #elif vp.check_exit():
            #break
