from pathlib import Path

import numpy as np
import cv2

print(cv2.__version__) # 3.4.2

### simple use case ############################################################

def read_video(path):
    cap = cv2.VideoCapture(str(path))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = [ cap.read()[1] for _ in ' '*num_frames ]
    return np.stack(frames)


### ignore errors which randomly happened ######################################

def read_video2(path):
    cap = cv2.VideoCapture(str(path))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    for _ in range(num_frames):
        ret,frame = cap.read()
        if not ret:
            if len(frames)!=0:
                return ( False, np.stack(frames) )
            else:
                return ( False, None )
        frames += [frame]
    return ( True, np.stack(frames) )


### slice-base sampling ########################################################

# 音声と映像の両方入っているフレームしか読み込めないっぽい
# 音声が映像より短いと，FRAME_COUNT の値まで読み込めず，途中で False になる

def read_video3(path, slice_obj):
    cap = cv2.VideoCapture(str(path))
    assert cap.isOpened()

    # you can get parameters as follows
    # - https://docs.opencv.org/4.0.1/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_rate = float(cap.get(cv2.CAP_PROP_FPS))

    start,stop,step = slice_obj.start, slice_obj.stop, slice_obj.step
    indice = [idx for idx in range(start if start else 0,
                                    stop if stop else num_frames+1, step)]
    frames = []
    for i in range(num_frames):
        print(i,'/',num_frames,', ',cap.get(cv2.CAP_PROP_POS_FRAMES))
        ret,frame = cap.read()
        if not ret:
            if len(frames)!=0:
                print(ret)
                return ( False, np.stack(frames) )
            else:
                return ( False, None )
        if i in indice:
            frames += [frame]
    return ( True, np.stack(frames) )


def main():
    status, seq = read_video3(Path('/home/horiuchi/Documents/sample_movie/output.mp4'),slice(None,None,30))
    print(status)
    print(seq.shape)


if __name__=='__main__': main()
