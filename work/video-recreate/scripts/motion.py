import cv2,numpy as np,sys
c=cv2.VideoCapture(sys.argv[1]);prev=None;i=0;out=[]
while True:
    ok,f=c.read()
    if not ok:break
    g=cv2.cvtColor(cv2.resize(f,(144,256)),cv2.COLOR_BGR2GRAY)
    if prev is not None:
        d=np.abs(g.astype(float)-prev).mean()
        try:
            w=np.eye(2,3,dtype=np.float32);_,w=cv2.findTransformECC(prev.astype(np.float32),g.astype(np.float32),w,cv2.MOTION_AFFINE,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,30,1e-4),None,5)
            z=(abs(w[0,0])+abs(w[1,1]))/2
        except: z=float('nan')
        out.append((i,d,z))
    prev=g.astype(np.float32);i+=1
for s in range(0,len(out),15):
    ch=out[s:s+15];print(f"{s/30:5.1f}s motion={np.mean([x[1] for x in ch]):5.2f} zoom={np.nanmean([x[2] for x in ch]):.4f}")
