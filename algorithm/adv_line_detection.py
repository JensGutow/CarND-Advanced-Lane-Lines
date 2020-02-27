import cv2
import numpy as np

class adv_line_detection(object):
    # static member
    cl = 2
    
    def __init__(self, s_thresh_min = 130, s_thresh_max = 255, thresh_min = 45, thresh_max = 250):
        print("adv_line_detection constructor NEU2")
        self.s_thresh_min   =  s_thresh_min
        self.s_thresh_max   =  s_thresh_max
        self.thresh_min     = thresh_min
        self.thresh_max     =  thresh_max
    
    def line_detection(self, warpedImg, test=False):
        ## 1) warpedImg -> hls -> s_channel -> Threshold_s
        # Convert the warped image into HLS
        testOut = []
        if test:
            testOut.append(warpedImg)
        hls = cv2.cvtColor(warpedImg, cv2.COLOR_RGB2HLS)
        testOut.append(hls)
        # select the s-channel
        s_channel = hls[:,:,2]
        if test:
            testOut.append(s_channel)
        
        s_binary = np.zeros_like(s_channel)
        # s_binary: 1/0-image: 1 <-> s_thresh_min <= s_ch <= s_thres_max
        s_binary[(s_channel >= self.s_thresh_min) & (s_channel <= self.s_thresh_max)] = 1
        if test:
            testOut.append(s_binary)
        
        ## 2) warpedImg -> grayScaled -> Sobel_x -> Threshold_x
        # grasdacle conversion 
        gray = cv2.cvtColor(warpedImg, cv2.COLOR_RGB2GRAY)
        testOut.append(gray)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0) # Take the derivative in x
        abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
        scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
        if test:
            testOut.append(scaled_sobel)
        # Threshold x gradient
        sxbinary = np.zeros_like(scaled_sobel)
        # sxbinary: 1/0-image: 1 <-> thresh_min <= scaled_sobel <= thres_max
        sxbinary[(scaled_sobel >= self.thresh_min) & (scaled_sobel <= self.thresh_max)] = 1
        if test:
            testOut.append(sxbinary)
        
        ## 3) Combine the two binary thresholds
        combined_binary = np.zeros_like(sxbinary)
        combined_binary[(s_binary == 1) | (sxbinary == 1)] = 1
        if test:
            testOut.append(combined_binary)
            
        if test:    
            return combined_binary, testOut
        else:
            return combined_binary