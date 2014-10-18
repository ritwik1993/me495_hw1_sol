#!/usr/bin/env python

import rospy
import numpy as np
import math
import sys
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute 

def trajectory_driver(T):
    twist=Twist()
    pub=rospy.Publisher('turtle1/cmd_vel',Twist, queue_size=10)
    rospy.init_node('turtlecmd_tracker',anonymous=True)
    r=rospy.Rate(60)
    while not rospy.is_shutdown():
        t=rospy.get_time()
        vx=(12*math.pi*math.cos(4*math.pi*t/T))/T
        vy=(6*math.pi*math.cos(2*math.pi*t/T))/T
        ax=-48*pow(math.pi,2)*math.sin(4*math.pi*t/T)/pow(T,2)
        ay=-12*pow(math.pi,2)*math.sin(2*math.pi*t/T)/pow(T,2)
        twist.linear.x=math.sqrt(pow(vx,2)+pow(vy,2))
        twist.angular.z=((vx*ay)-(vy*ax))/(pow(vx,2)+pow(vy,2))
        #twist.angular.z=(math.pi/T)*(((2*math.sin(4*math.pi*t/T)*math.cos(2*math.pi*t/T)/pow(math.cos(4*math.pi*t/T),2))-(math.sin(2*math.pi*t/T)/math.cos(4*math.pi*t/T)))/(1+((pow(math.cos(2*math.pi*t/T),2))/4*pow(math.cos(4*math.pi*t/T),2))))
        pub.publish(twist)
        r.sleep()
       

if __name__ == '__main__':
    try:
        rospy.wait_for_service('turtle1/teleport_absolute')
        turtle_initial=rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
        turtle_initial(5.5,5.5,math.pi/6)
        if len(sys.argv)>1:
            trajectory_driver(float(sys.argv[1]))
        else:
            trajectory_driver(8)
    except rospy.ROSInterruptException: pass
