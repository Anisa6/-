import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class SoundVolume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(0, None)
    vol_per = 0

    @staticmethod
    def change(length):
        SoundVolume.vol_per = np.interp(length, [50, 200], [0, 100])
        SoundVolume.vol_per = 5 * round(SoundVolume.vol_per / 5)
        SoundVolume.volume.SetMasterVolumeLevelScalar(SoundVolume.vol_per / 100, None)
