class unit_conversion(object):
 # static member
    def __init__(self):
        print("unit_conversion constructor")
        
    # central definition of converting "ticks" (from pciture) to "meter" (from origin area)
    # return 
    #    - list of conversion factors
    #        [0] conversion factor for the x component
    #        [1] conversion factor for the < component
    @staticmethod
    def get_xy_m_per_tick():
        ym_per_pix = 30/720 # meters per pixel in y dimension
        xm_per_pix = 3.7/700 # meters per pixel in x dimension
        return xm_per_pix, ym_per_pix
