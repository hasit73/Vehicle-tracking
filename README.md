# Vehicle Tracking using Centroid tracker

### Algorithm used : Yolo algorithm for detection + centroid tracker to track vehicles
### Backend : opencv and python
### Library required:

- opencv = '4.5.4-dev'
- scipy = '1.4.1'


### IMPORTANT:

- I hadn't uploaded model weights and configuration files (which were used for object detection) here because those were already available in yolo_detection repo
- download yolo tiny weights , config file and coco.names file from here : [https://github.com/hasit73/yolo_detection]
- For detection i was using same code which was available in yolo_detection repo.

# Quick Overview about structure

#### 1) main.py

- Loading model and user configurations
- perform interfacing tasks


#### 2) yolo.py

- use opencv modules to detect objects from user given media(photo/video)
- detection take place inside this file


#### 3) config.json

- user configuration are mentioned inside this file
- for examples : input shapes and model parameters(weights file path , config file path etc) are added in config.json


#### 4) centroid_tracker.py

- implementation of centroid tracker

# How to use 

1) clone this directory

 
2) use following command to run detection and tracking on your custom video

  ```
  python main.py -c config.json -v <media_path>
  ```

  Example: 
  ```
  python main.py -c config.json -v car1.mp4
  ```
  
- Note : Before executing this command make sure that you have downloaded model weights and config file for yolo object detection.

### Results


- output:1

https://user-images.githubusercontent.com/69752829/141642879-a7d86862-6983-4881-a332-57a1e8ed970e.mp4


- output:2

https://user-images.githubusercontent.com/69752829/141642924-2bd306ca-7695-4d2b-9412-26a2bf1c767f.mp4



### Limitations:

There are two primary drawbacks of this object tracking algorithm.

1) The first is that it requires that object detection step to be run on every frame of the input video.

2) The second drawback is related to the underlying assumptions of the centroid tracking algorithm itself — centroids must lie close together between subsequent frames.

## If it's helful for you then please give star :)
