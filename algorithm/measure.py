import algorithm.unit_conversion as conv
import numpy as np


class measure(object):
 # static member
    def __init__(self):
        print("measure constructor")
        c = conv.unit_conversion()
        self.xm_per_pix = c.get_xy_m_per_tick()[0]
        self.ym_per_pix = c.get_xy_m_per_tick()[1]
        
    # calc radius, given by the polynom second order poly2
    # the picture-ticks are interpreted/converted as/into orignial units (m)
    # args:
    #    - poly2: polygon 2 order, list, y(x) = poly2[0]*x*x + poly2[1]*x + poly2[2]
    #    - img: single picture, is used for calc the "y"-coordinates 
    #    - calc and return the radius in m
    # return:
    #    - raduis [m]
    # remark:
    #   - dimensions of the pciture: x and y coordinates
    #   - the polygon calcs the "x"-position of a given "y"-image coordinate in image space given by the extend of the image
    def calc_curve_rad(self, poly2, img):
        ploty = np.linspace(0, img.shape[0]-1, img.shape[0] )
        
        #ym_per_pix = get_xy_m_per_tick()[1]
        #xm_per_pix = get_xy_m_per_tick()[0]
        
         # Define y-value where we want radius of curvature
        # We'll choose the maximum y-value, corresponding to the bottom of the image
        y_eval = np.max(ploty) - 1
        
        # Calculation of R_curve (radius of curvature)
        curverad = ((1 + (2 * poly2[0] * y_eval * self.ym_per_pix + poly2[1]) ** 2) ** 1.5) / np.absolute(2 * poly2[0])

        return curverad
        
        
    # calculate the relative location of the car (of the camera) relative to the midpoint of the both lane lines l and r
    # l and r are lists of len of three and represent the left resepctive right lane line by a polygon second order
    # args:
    #    - l,r polygon 2 order, describe the left and right lane line (in picture coordinates ticks) 
    #        - y(x) = poly2[0]*x*x + poly2[1]*x + poly2[2]
    #    - img: single picture, is used for get the dimensiony in x and y direction
    #    - calc the the offset  l(0)-r(0)-(max_x/2) and convert to m
    # return:
    #    - relative car position (m, distance to the midpoint of the lane)
    # remark:
    #   - dimensions of the pciture: x and y coordinates
    #   - the polygons calc the "x"-position of a given "y"-image coordinate in image space given by the extend of the image
    def calc_midpoint_offset(self, l,r, img):
        # calculation the x-value of the both function l and r at the bottom 
        y = 0 #img.shape[0]-20
        # calc the x-position of l respective r lane at x
        xl=l[0] * y * y + l[1] * y + l[2]
        xr=r[0] * y * y + r[1] * y + r[2]
        # max dimension in x direction
        xmax = img.shape[1]
        xm = (xl + xr)/2
        offs = xm - (xmax/2)
        # convert "ticks" to m respective the x coordinate
        offs_m = offs * self.xm_per_pix
        return offs_m          