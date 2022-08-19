from __future__ import print_function
import time
from dronekit import connect, VehicleMode, mavutil, LocationGlobalRelative
import math
import pickle
import pid
from pymavlink import mavutil

sayi=0
sayi2=0
deger=0
vehicle = connect('127.0.0.1:14551', wait_ready=True,baud=57600)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    time.sleep(2)
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
def goto_position_target_local_ned(north, east, down):
    """	
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified 
    location in the North, East, Down frame.

    It is important to remember that in this frame, positive altitudes are entered as negative 
    "Down" values. So if down is "10", this will be 10 metres below the home altitude.

    Starting from AC3.3 the method respects the frame setting. Prior to that the frame was
    ignored. For more information see: 
    http://dev.ardupilot.com/wiki/copter-commands-in-guided-mode/#set_position_target_local_ned

    See the above link for information on the type_mask (0=enable, 1=ignore). 
    At time of writing, acceleration and yaw bits are ignored.

    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down, # x, y, z positions (or North, East, Down in the MAV_FRAME_BODY_NED frame
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink) 
    # send command to vehicle
    vehicle.send_mavlink(msg)


def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms (not used)
        0, 0,  # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED,  # frame
        0b0000111111000111,  # type_mask (only speeds enabled)
        0, 0, 0,  # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z,  # x, y, z velocity in m/s
        0, 0, 0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
def condition_yaw(heading, relative=False):
  
    if relative:
        is_relative = 1 #yaw relative to direction of travel
    else:
        is_relative = 0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)


def oku():
    try:
        with open("pay1.pkl", "rb") as f:
            xd = pickle.load(f)
            #time.sleep(3)
    except (EOFError):
        pass
        print("okuma hatasi")
    return xd 

say = 0
sayi2= 0
def sayma():
    global say
    say=say+1
    print(say)
    if say%4 == 0:
        
        global sayi2
        sayi2=sayi2+1
        if sayi2%2 == 0:
            goto_position_target_local_ned(0.3,0.3,0)
            time.sleep(4)
        else:
            goto_position_target_local_ned(0.3,-0.3,0)
            time.sleep(4)



def tara():
    
    for i in range (1,5):
        kosul=oku()
        if kosul[3] == True:
            
            condition_yaw(90,True)
            time.sleep(4)
            sayma()
            
            
          


        if kosul[3] == False:
            print("hedef buldu")
            pass
        
  
#vehicle = connect("127.0.0.1:14551", wait_ready=True)
#vehicle = connect('/dev/ttyAMA0', wait_ready=True)
a_e=320
a_n=240


time.sleep(2)
arm_and_takeoff(5)
time.sleep(2)

while True:
    try:
        with open("pay1.pkl", "rb") as f:
            xd = pickle.load(f)
            #time.sleep(3)
    except (EOFError):
        pass
        print("okuma hatasi")
    #tarama kısm
    tara()
    
   # deger = sayma()
   # print(deger)
    
                
                
    a_e = xd[0]
    a_n = xd[1]
    hiz = pid.pidss(a_e,a_n)
    veri0 = math.fabs(hiz[0])
    veri1 = math.fabs(hiz[1])
    #640 yatay genişlik, 360 dikey uzunuk değerleri
    print("veri0:",veri0)
    print("veri1:",veri1)
   
    if (a_e > 290 and a_e < 350 and a_n > 220 and a_n < 260):
        goto_position_target_local_ned(0,0,0)
        print("Position Hold")
        if xd[2] is True:
            
            time.sleep(1)
            
            
            print("Atış yapıldı.")
            time.sleep(1)
            vehicle.mode=VehicleMode("LAND")
    elif (a_e > 560 ):
        goto_position_target_local_ned(0,-0.5,0)
        print("get safe area-right")
    elif (a_n < 80):
        goto_position_target_local_ned(0,0.5,0)
        print("get safe area-left")
    elif (a_e > 320 and a_e <560 ):
        if (a_n>80 and a_n<240):
     
            goto_position_target_local_ned(veri1,-veri0,0)
            print (" kuzey dogu ")
       
        elif(a_n>240 and a_n<400):
          
            goto_position_target_local_ned(-veri1,-veri0,0)
            print (" guney dogu ")
         
    elif(a_e>80 and a_e < 320):
        
        if (a_n>80 and a_n<240):
           
            goto_position_target_local_ned(veri1,veri0,0)
            print (" kuzey bati ")
         
        elif (a_n>240 and a_n<400):
        
            goto_position_target_local_ned(-veri1,veri0,0)
            print (" guney bati ")
                
    else:
        goto_position_target_local_ned(0,0,0)
        print("stabil")
  
    if vehicle.mode.name!="GUIDED" :
        break
    a_e=320
    a_n=240
    
    time.sleep(3)
vehicle.mode=VehicleMode("LAND")
print ("land modu")
time.sleep(3)
vehicle.close()




