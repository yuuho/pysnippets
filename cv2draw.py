'''
OpenCVの描画関数についてまとめた

ここで登場するオブジェクト
- VBO2 (VertexBufferObject2) := ndarray (N,2_xy)
- IBO_ (IndexBufferObject1) := ndarray (M,)
- IBO2 (IndexBufferObject2) := ndarray (M,2_sg)
- IBO3 (IndexBufferObject3) := ndarray (M,3_smg)

( s:= start, m:= mid, g:= goal )

TODO) クリッピング処理
'''

H,W,C = (128,128,3)

vbo2 = np.array([[20,30],[40,70],[69,70],[100,100]])
ibo_ = np.array([0,1,2])
ibo2 = np.array([[0,1],[1,2],[2,0]])
ibo3 = np.array([[0,1,2],[2,1,3]])


# 点の描画 VBO2とIBO_を利用
points = [(vbo[idx,0],vbo[idx,1]) for vbo in [vbo2.astype(np.int32)] for idx in ibo_]
rendered = [ l.append( cv2.circle( l.pop(0), pt, radius=2,color=(255,255,255),
                        thickness=-1,lineType=cv2.LINE_8,shift=0)) if pt else l[0]
            for l in [[np.zeros((H,W,C),dtype=np.uint8)]] for pt in points+[None] ][-1]

# 線の描画 VBO2とIBO2を利用
lines = [np.stack([vbo[idxs[0]],vbo[idxs[1]]]) for vbo in [vbo2.astype(np.int32)] for idxs in ibo2]
rendered = cv2.polylines( np.zeros((H,W,C),dtype=np.uint8), lines, isClosed=False,
                color=(255,255,255),thickness=1,lineType=cv2.LINE_AA, shift=0)

# 面の描画 VBO2とIBO3を利用
polygons = [np.stack([vbo[idxs[0]],vbo[idxs[1]],vbo[idxs[2]]])
                for vbo in [vbo2.astype(np.int32)] for idxs in ibo]
rendered = cv2.fillPoly( np.zeros((H,W,C),dtype=np.uint8), polygons,
                color=(255,255,255),lineType=cv2.LINE_AA, shift=0)
