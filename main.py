from yolo import YoloDetection
import cv2
import argparse
from centroid_tracker import Tracker
# import imageio

CONFIG_FILE = None
model = None

def load_config(config_path):
    global CONFIG_FILE
    CONFIG_FILE = eval(open(config_path).read())


def load_model():
    global model
    model = YoloDetection(CONFIG_FILE["model-parameters"]["model-weights"],
                    CONFIG_FILE["model-parameters"]["model-config"],
                    CONFIG_FILE["model-parameters"]["model-names"],
                    CONFIG_FILE["shape"][0],
                    CONFIG_FILE["shape"][1])


def start_detection(media_path):

    tracker = Tracker()

    cv2.namedWindow("Video",cv2.WINDOW_NORMAL)
    cap = cv2.VideoCapture(media_path)
    # writer = imageio.get_writer("demo1.mp4")
    ret = True
    while ret:
        ret , frame = cap.read()

        detections = model.process_frame(frame)
        tracker_res = tracker.update_object([ x[1:5] for x in detections ])
        
        for id,boxes in tracker_res.items():
            x,y = (int(boxes[0]), int(boxes[1]))
            w,h = (int(boxes[2]), int(boxes[3]))
            cv2.rectangle(frame,(x,y),(x+w,y+h),thickness=2,color=(255,0,0))
            cv2.putText(frame,str(id),(x,y-20),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        
        cv2.imshow("Video",frame)
        ## write video using imageio
        # writer.append_data(frame[:,:,::-1])
        key = cv2.waitKey(30)
        if(key==27):
            break
    # writer.close()
    cv2.destroyAllWindows()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Provide arguements")
    parser.add_argument("--config","-c")
    parser.add_argument("--debug","-d")
    parser.add_argument("--video","-v")
    args = parser.parse_args()
    config_path = args.config
    load_config(config_path)
    load_model()
    start_detection(args.video)