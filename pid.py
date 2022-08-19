import numpy as np
import time
import math

def pidss(orta,orta2):
            Kp = 0.70
            Ki = 0
            Kd = 0.080
            integral = 0
            derivative = 0
            last_error = 0
            normal_error = 0

            Kp2 = 0.70
            Ki2 = 0
            Kd2 = 0.080
            integral2 = 0
            derivative2 = 0
            last_error2 = 0
            normal_error2 = 0
            setpoint =320

            error = int(orta - setpoint)
            normal_error = error/setpoint
            integral = float(integral + normal_error)
            derivative = normal_error - last_error
            last_error = normal_error
            pid = (Kp*normal_error+Ki*integral+Kd*derivative)

            setpoint2 =240
            error2 = int(orta2 - setpoint2)
            normal_error2 = error2/setpoint2
            integral2 = float(integral2 + normal_error2)
            derivative2 = normal_error2 - last_error2
            last_error2 = normal_error2

            pid2 = (Kp2*normal_error2+Ki2*integral2+Kd2*derivative2)
            pid2=round(pid2,4)
            pid=round(pid,4)
            return pid,pid2

            
	    


























