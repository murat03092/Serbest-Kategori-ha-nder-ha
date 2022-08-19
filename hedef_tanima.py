import cv2
import numpy as np
import time
import pickle

def update_pts(params, x, y):
    global x_init, y_init
    params["top_left_pt"] = (min(x_init, x), min(y_init, y))
    params["bottom_right_pt"] = (max(x_init, x), max(y_init, y))
    #img[y_init:y, x_init:x] = 255 - img[y_init:y, x_init:x]

def draw_rectangle(event, x, y, flags, params):
    global selected
    global x_init, y_init, drawing
    # First click initialize the init rectangle point
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_init, y_init = x, y
        # Meanwhile mouse button is pressed, update diagonal rectangle point
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        update_pts(params, x, y)
        # Once mouse botton is release
    elif event == cv2.EVENT_LBUTTONUP:
        selected=True
        drawing = False
        update_pts(params, x, y)

if __name__ == '__main__':
    drawing = False
    event_params = {"top_left_pt": (-1, -1), "bottom_right_pt": (-1, -1)}
    selected=False

    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture("cow.mp4")
    tracker=cv2.TrackerMOSSE_create()
    #csrt,kcf,mil,mosse
    initialized=False
    bbox1=[]

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cv2.namedWindow('Webcam')
    # Bind draw_rectangle function to every mouse event
    cv2.setMouseCallback('Webcam', draw_rectangle, event_params)

    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    orta_x=int(width/2)
    orta_y=int(height/2)
    

    bbox=()
    axy=[orta_x,orta_y]
    file_output='xdxd.avi'
    fourcc=cv2.VideoWriter_fourcc(*'FMP4')
    out=cv2.VideoWriter(file_output,fourcc,20.0,(int(width),int(height)))
    fp=open("pay1.pkl","wb")
    pickle.dump(axy,fp,protocol=2)
    fp.close()
    while True:
        ok, frame = cap.read()
        frame=cv2.flip(frame,1)
        img = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        img=frame
        (x0, y0), (x1, y1) = event_params["top_left_pt"], event_params["bottom_right_pt"]
        bbox1=[x0,y0,x1-x0,y1-y0]

        if selected:
            bbox = tuple(bbox1)
            tracked=tracker.init(img,bbox)
          
        if not ok:
            break
        ret,bbox=tracker.update(img)
        if ret:
            p1=(int(bbox[0]),int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(img,p1,p2,(255,0,0),2,1)
            a_x=int(2*bbox[0]+bbox[2])/2
            a_y=int(2*bbox[1]+bbox[3])/2
            axy=[a_x,a_y]
            cv2.line(img, (320, 240), (int(a_x),int(a_y)), (255, 0, 255), 2)
            cv2.circle(img, (int(a_x),int(a_y)), 2, (0,0,255), 2)
            cv2.putText(img, "Target", (int(a_x),int(a_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.55,(0, 20, 25), 2) 
            
            
        else:
            cv2.putText(img, "Track fail", (100, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65,(0, 0, 255), 2)
            axy=[orta_x,orta_y]
        
      
        print (axy)
        fp=open("pay1.pkl","wb")
        pickle.dump(axy,fp,protocol=2)
        fp.close()
        
        out.write(img)
        cv2.rectangle(img,(280,200),(360,280),(255,255,0),2)
        cv2.rectangle(img,(80,80),(560,400),(25,55,200),2)
        cv2.circle(img, (320, 240), 2, (0,0,255), 2)  
        cv2.putText(img, "Hold Area", (300,190), cv2.FONT_HERSHEY_SIMPLEX, 0.40,(0, 0, 255), 2)
        cv2.putText(img, "Safe Area", (75,75), cv2.FONT_HERSHEY_SIMPLEX, 0.40,(0, 0, 255), 2) 
        cv2.imshow('Webcam', img)
        
        c = cv2.waitKey(5)
        if c == 27:
            axy=[orta_x,orta_y]
            fp=open("pay1.pkl","wb")
            pickle.dump(axy,fp,protocol=2)
            fp.close()
            print(axy)
            time.sleep(0.5)
            break
       

    
    cap.release()
    out.release()
    cv2.destroyAllWindows()