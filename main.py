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
        
        elif vp.sound_process_active():
            if vp.HandLandmark:
                dist = len_between(vp.HandLandmark[4], vp.HandLandmark[8])
                sv.change(dist)
                
            if vp.sound_process_stop():
                continue
