import algorithm.undistortion as undist
import algorithm.switch_perspective as persp
import algorithm.img_transformation as det
import algorithm.measure as measure
import algorithm.report as report
import algorithm.find_lane_lines as lines

class video_pipeline(object):
    # static member
   
    
    def __init__(self, undistortionPickleDest, perspectivePickleDest):
        print("video_pipeline constructor detla1")
        self.undist =  undist.undistortion()
        self.undist.setParameterFromPickle(undistortionPickleDest)
        
        self.persp = persp.switch_perspective()
        self.persp.setParameterFromPickle(perspectivePickleDest)
        
        self.det = det.img_transformation()
        
        self.measure = measure.measure()
        
        self.lines = lines.find_lane_lines()
        
        self.rep = report.report(self.persp)
        
        
    def process_video_pipeline(self, orgImg):
        #imgs = []
        #imgs.append(orgImg)
        undistortedImg = orgImg.copy()
        # undistortedImg = undistortion_used_saved_params(undistortedImg)
        undistortedImg = self.undist.undistortion(undistortedImg)
        
        #imgs.append(undistortedImg)
        ## trafoImg = get_birdsEyeTrafoAndGaussianBlur(undistortedImg)
        trafoImg = self.persp.get_birds_eye_with_blur(undistortedImg)
        
        #imgs.append(trafoImg)
        grayLines = self.det.transformation(trafoImg)
        
        #imgs.append(grayLines)
        l_cr,r_cr, l_persp, r_persp = self.lines.fit_polynomial(grayLines)
        curveRad_l = self.measure.calc_curve_rad(l_cr, grayLines)
        curveRad_r = self.measure.calc_curve_rad(r_cr, grayLines)
        offs = self.measure.calc_midpoint_offset(l_persp, r_persp, grayLines)
        result = self.rep.decorate_lane_line(l_persp, r_persp,grayLines, orgImg)
        result  = self.rep.report_radius_and_offs(result, (curveRad_l + curveRad_r)/2, offs)
        return  result