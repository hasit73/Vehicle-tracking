import numpy as np
from scipy.spatial.distance import cdist

class Tracker:
    MAX_DISAPPEAR_LIMIT = 5
    def __init__(self):
        self.next_unique_id = 0
        self.trackers = {}
        self.disappear_trackers = {}
        self.tracked_bboxes = {}
    
    
    def init_object(self,centroid,boxes):
        global next_unique_id
        self.trackers[self.next_unique_id] = centroid
        self.tracked_bboxes[self.next_unique_id] = boxes
        self.disappear_trackers[self.next_unique_id] = 0
        self.next_unique_id+=1

    def del_object(self,track_id):
        del self.trackers[track_id]
        del self.tracked_bboxes[track_id]
        del self.disappear_trackers[track_id]

    def update_object(self,bboxes):
        
        if(len(bboxes)==0):
            
            for oid in list(self.disappear_trackers.keys()):
                self.disappear_trackers[oid]+=1
                
                if self.disappear_trackers[oid] > Tracker.MAX_DISAPPEAR_LIMIT:
                    self.del_object(oid)
                
            return self.tracked_bboxes
        
        else:   
            input_centroids = np.zeros((len(bboxes),2)) 
            for i in range(len(bboxes)):
                x,y,w,h = bboxes[i][0],bboxes[i][1],bboxes[i][2],bboxes[i][3]
                cx,cy = x + w/2 , y + h/2
                input_centroids[i] = (cx,cy)

            
            if(len(self.trackers)==0):
                for i in range(len(input_centroids)):
                    self.init_object(input_centroids[i],bboxes[i])
            
            else:
                
                tracker_centroids = list(self.trackers.values())

                distance_matrix = cdist(np.array(tracker_centroids) , input_centroids)

                rows = distance_matrix.min(axis=1).argsort()
                cols = distance_matrix.argmin(axis=1)[rows]

                usedRows = set()
                usedCols = set()
                
                tracker_ids = list(self.trackers.keys()) 
                for row,col in zip(rows,cols):
                    if row in usedRows or col in usedCols:
                        continue
                    track_id = tracker_ids[row]
                    
                    self.trackers[track_id] = input_centroids[col]
                    self.tracked_bboxes[track_id] = bboxes[col]

                    self.disappear_trackers[track_id] = 0
                    usedRows.add(row)                                
                    usedCols.add(col)
                unusedRows = set(range(0,distance_matrix.shape[0])).difference(usedRows)
                unusedCols = set(range(0,distance_matrix.shape[1])).difference(usedCols)
                if(distance_matrix.shape[0]>=distance_matrix.shape[1]):
                    
                    for r in unusedRows: 
                        track_id = tracker_ids[r]
                        self.disappear_trackers[track_id]+=1
                        if(self.disappear_trackers[track_id] > Tracker.MAX_DISAPPEAR_LIMIT):
                            self.del_object(track_id)
                else:
                    for c in unusedCols:                    
                        self.init_object(input_centroids[c],bboxes[c])

        return self.tracked_bboxes
