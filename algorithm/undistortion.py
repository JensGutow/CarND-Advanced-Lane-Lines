import cv2
import pickle

class undistortion(object):
 # static member
    def __init__(self):
        print("undistortion constructor")
        self.mtx = []
        self.dist  = []
        
    # pickleFile: name of the pickle, will be read
    def setParameterFromPickle(self, pickleFile):
        # open a file, where you stored the pickled data
        # file = open('output_images\calibration\wide_dist_pickle.p', 'rb')
        file = open(pickleFile, 'rb')
        dist_pickle = pickle.load(file) 
        self.mtx = dist_pickle["mtx"]
        self.dist = dist_pickle["dist"]
        file.close
        
    def setParmeter(self, mtx, dist):
        self.mtx = mtx
        self.dist = dist
        
    def undistortion(self, img):
        # open a file, where you stored the pickled data
        return cv2.undistort(img, self.mtx, self.dist, None, self.mtx)