import cv2,numpy as np,sys
c=cv2.VideoCapture(sys.argv[1]);F=[]
while True:
    ok,f=c.read()
    if not ok:break
    F.append(cv2.cvtColor(cv2.resize(f,(72,128)),cv2.COLOR_BGR2GRAY).astype(float))
for i in range(0,42,6):
    d=[np.abs(F[i]-F[j]).mean() for j in range(200,360)]
    j=int(np.argmin(d))+200;print(f"teaser {i/30:.2f}s best match {j/30:.2f}s diff={min(d):.1f}")
# scene cuts
for i in range(1,len(F)):
    d=np.abs(F[i]-F[i-1]).mean()
    if d>25:print(f"cut at {i/30:.2f}s d={d:.0f}")
