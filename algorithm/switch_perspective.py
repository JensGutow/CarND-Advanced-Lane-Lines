import cv2
import pickle

class switch_perspective(object):
    # static member
    def __init__(self, M=[], Minv=[]):
        print("switch_perspective constructor")
        self.M = M
        self.Minv  = Minv
        
    # pickleFile: name of the pickle, will be read
    def setParameterFromPickle(self, pickleFile):
        # open a file, where you stored the pickled data
        file = open(pickleFile, 'rb')
        dist_pickle = pickle.load( file) 
        self.M = dist_pickle["M"]
        self.Minv = dist_pickle["Minv"]
        file.close
        
    def setParmeter(self, M, Minv):
        self.M = M
        self.Minv = Minv

    def get_birds_eye_with_blur(self, img):
        img_size = (img.shape[1], img.shape[0])
        warped = cv2.warpPerspective(img, self.M, img_size)
        # moving avarage
        gauss_kernel = 5
        img_blur = cv2.GaussianBlur(warped, (gauss_kernel, gauss_kernel), 0)
        return img_blur
        
    def swtich_to_normal_perspective(self, img):
        return cv2.warpPerspective(img, self.Minv, (img.shape[1], img.shape[0])) 