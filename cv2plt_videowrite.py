
'''
## メモ

動画作成の際、matplotlib.pyplot で大量の画像を作成するのはやらないほうが良い。
pyplot はメモリの管理がおかしいのでどこかで崩壊しがち。
毎回 ``.savefig()`` -> ``.close()`` -> ``.clf()`` -> ``.cla()`` をすると、
問題なくメモリ解放されて正しくレンダリングされることが多いが、
とても遅いので、素直に object-oriented API を使用したほうが良い。
plt は import 自体しないこと。
'''


import io
from pathlib import Path

import tqdm
import numpy as np
from matplotlib.figure import Figure
import cv2


# 動画書き出し関数
def write_video( imgs, path, fps=30.0 ):
    T,H,W,C = imgs.shape
    # VideoWriter 設定は (W,H) であることに注意 (合わないと再生できない動画ができる)
    [ [ writer.write(frame) for frame in tqdm.tqdm(imgs) ]
        for writer in [ cv2.VideoWriter( str(path),cv2.VideoWriter_fourcc(*'mp4v'),fps,(W,H) ) ] ]


# generator-based : 大量の画像をメモリに保持するのが難しいときは毎フレームレンダリングする
class VideoFrames:
    def __init__(self, data, H,W):
        self.data = data
        self.shape = (len(self),H,W,3)
    def __len__(self):
        return len(self.data)
    def __getitem__(self,idx):
        T,H,W,C = self.shape
        dpi = 180
        figsize_inch = np.array([W,H]) / dpi
        fig = Figure(figsize=figsize_inch, dpi=dpi)
        sbplt = fig.add_subplot(1,1,1)

        sample = 100
        x = np.linspace(0,10, sample)
        y = np.sin(x+self.data[idx])
        sbplt.plot(x,y)
        sbplt.set_ylim(-1.0, 1.0)

        with io.BytesIO() as buf:
            fig.savefig( buf, format="png", dpi=dpi )
            frame = cv2.imdecode( np.frombuffer( buf.getvalue(), dtype=np.uint8 ), 1)
        return frame



def main():
    T,H,W,C = 300,480,640,3
    fps = 30.0 # float

    rad_per_sec = 2*np.pi
    rad_per_frame = rad_per_sec/fps

    # 1: numpy で作成した画像シーケンスを書き出す。
    frames = np.empty((T,H,W,C),dtype=np.uint8)
    grid = np.mgrid[:H,:W].transpose(1,2,0)
    r = min(H,W)*0.4
    for t in range(T):
        pos = np.array([H/2,W/2])+np.array([r*np.sin(t*rad_per_frame),
                                            r*np.cos(t*rad_per_frame)])
        dist = ((grid-pos[None,None,:])**2).sum(axis=2)**0.5
        d = np.where(dist>=5,0,255)[:,:,None].astype(np.uint8)
        frames[t] = np.c_[d,d,d]
    write_video( frames, Path('/tmp/sample1.mp4'), fps=fps)

    # 2: matplotlib で作成した画像シーケンスを書き出す。
    data = np.arange(T)*rad_per_frame
    write_video( VideoFrames(data,H,W), Path('/tmp/sample2.mp4'), fps=fps)



if __name__ == '__main__': main()
