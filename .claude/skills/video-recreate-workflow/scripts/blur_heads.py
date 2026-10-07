import sys, cv2, numpy as np, mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision as V
import os
M=os.environ.get('MP_MODELS','models')+'/'  # face.tflite = blaze_face_short_range, pose.task = pose_landmarker_full
src,dst=sys.argv[1],sys.argv[2]
pose=V.PoseLandmarker.create_from_options(V.PoseLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=M+'pose.task'),running_mode=V.RunningMode.VIDEO,num_poses=3,min_pose_detection_confidence=0.3,min_tracking_confidence=0.3))
face=V.FaceDetector.create_from_options(V.FaceDetectorOptions(base_options=mpt.BaseOptions(model_asset_path=M+'face.tflite'),min_detection_confidence=0.3))
c=cv2.VideoCapture(src); fps=c.get(5); W,H=int(c.get(3)),int(c.get(4)); S=2
out=cv2.VideoWriter(dst+'.tmp.mp4',cv2.VideoWriter_fourcc(*'mp4v'),fps,(W*S,H*S))
i=0; prev=[]; stats=[]; frames=[]; allb=[]
while True:
    ok,f=c.read()
    if not ok: break
    rgb=cv2.cvtColor(f,cv2.COLOR_BGR2RGB); img=mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb)
    boxes=[]
    r=pose.detect_for_video(img,int(i*1000/fps))
    for lm in r.pose_landmarks:
        pts=np.array([[p.x*W,p.y*H] for p in lm[:11]])
        sh=np.array([[lm[11].x*W,lm[11].y*H],[lm[12].x*W,lm[12].y*H]])
        cx,cy=pts.mean(0); w=max(np.ptp(pts[:,0])*1.6, np.linalg.norm(sh[0]-sh[1])*0.75, 40)
        boxes.append((cx-w*0.7,cy-w*0.95,cx+w*0.7,cy+w*0.75))
    for d in face.detect(img).detections:
        b=d.bounding_box; boxes.append((b.origin_x-b.width*0.4,b.origin_y-b.height*0.7,b.origin_x+b.width*1.4,b.origin_y+b.height*1.3))
    frames.append(f); allb.append(boxes); stats.append(len(boxes)); i+=1
for i,f in enumerate(frames):
    use=[b for j in range(max(0,i-10),min(len(frames),i+11)) for b in allb[j]]
    mask=np.zeros((H,W),np.uint8)
    for x0,y0,x1,y1 in use:
        cv2.ellipse(mask,(int((x0+x1)/2),int((y0+y1)/2)),(int((x1-x0)/2),int((y1-y0)/2)),0,0,360,255,-1)
    cv2.rectangle(mask,(int(W*0.78),0),(W,int(H*0.06)),255,-1)  # watermark
    mask=cv2.GaussianBlur(mask,(21,21),0)/255.0
    small=cv2.resize(f,(W//24,H//24)); pix=cv2.GaussianBlur(cv2.resize(small,(W,H),interpolation=cv2.INTER_LINEAR),(31,31),0)
    g=(f*(1-mask[...,None])+pix*mask[...,None]).astype(np.uint8)
    out.write(cv2.resize(g,(W*S,H*S),interpolation=cv2.INTER_LANCZOS4))
out.release(); print('frames',i,'detections/frame min,mean',min(stats),np.mean(stats))
