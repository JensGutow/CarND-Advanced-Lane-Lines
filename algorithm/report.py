import algorithm.unit_conversion as conv
import algorithm.switch_perspective as persp
import numpy as np
import cv2


class report(object):

    def __init__(self, switch_persp):
        print("report constructor with switch_persp")
        self.sw_persp = switch_persp
        
    @staticmethod
    def report_radius_and_offs(img, radius, offs):
        radius_output =  "Curvature radius [m]: {0:.0f}".format(radius) 
        offs_output = "Midpoint offs [cm]:{0:.1f}".format(offs*100.0)
        font = cv2.FONT_HERSHEY_DUPLEX 
        org_radius = (20, 50) 
        org_offs   = (20, 120)
        fontScale = 2
        color = (0 ,0 ,255) # blue
        thickness = 1
        # Using cv2.putText() method 
        # output = img.copy() 
        output = img # no copy
        output = cv2.putText(output, radius_output, org_radius, font,
                            fontScale, color, thickness, cv2.LINE_AA) 
        output = cv2.putText(output, offs_output, org_offs, font,
                            fontScale, color, thickness, cv2.LINE_AA)
        return output 
            
    def decorate_lane_line(self, left_fit, right_fit, img, img_undist):
        ## Warp results back
        # Create an image to draw the lines on
        warp_zero = np.zeros_like(img).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
        
        # Generate x and y values for plotting
        ploty = np.linspace(0, img.shape[0]-1, img.shape[0] )
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
        pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

        # Warp the blank back to original image space using inverse perspective matrix (Minv)
        # newwarp = cv2.warpPerspective(color_warp, self.Minv, (img.shape[1], img.shape[0])) 
        newwarp = self.sw_persp.swtich_to_normal_perspective(color_warp)
        # Combine the result with the original image
        result = cv2.addWeighted(img_undist, 1, newwarp, 0.3, 0)

        return(result)    