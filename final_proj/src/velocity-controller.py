#! /usr/bin/env python3 
 
# Import the Python library for ROS 
import rospy, time 
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan 
from std_msgs.msg import Bool
 
def scan_callback(msg): 
    global range_front 
    global range_right 
    global range_left 
    global ranges 
    global min_front,i_front, min_right,i_right, min_left ,i_left 
     
    ranges = msg.ranges 
    # get the range of a few points 
    # in front of the robot (between 5 to -5 degrees) 
    range_front[:5] = msg.ranges[5:0:-1]   
    range_front[5:] = msg.ranges[-1:-5:-1] 
    # to the right (between 300 to 345 degrees) 
    range_right = msg.ranges[300:345] 
    # to the left (between 15 to 60 degrees) 
    range_left = msg.ranges[60:15:-1] 
    # get the minimum values of each range  
    # minimum value means the shortest obstacle from the robot 
    min_range,i_range = min( (ranges[i_range],i_range) for i_range in range(len(ranges)) ) 
    min_front,i_front = min( (range_front[i_front],i_front) for i_front in range(len(range_front)) ) 
    min_right,i_right = min( (range_right[i_right],i_right) for i_right in range(len(range_right)) ) 
    min_left ,i_left  = min( (range_left [i_left ],i_left ) for i_left  in range(len(range_left )) ) 
     
 
# Initialize all variables 
range_front = [] 
range_right = [] 
range_left  = [] 
min_front = 0 
i_front = 0 
min_right = 0 
i_right = 0 
min_left = 0 
i_left = 0 
 
 
 
# Create the node 
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1) # to move the robot 
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)   # to read the laser scanner 
rospy.init_node('velocity_controller') 
 
command = Twist() 
command.linear.x = 0.0 
command.angular.z = 0.0 
         
rate = rospy.Rate(10) 
time.sleep(1) # wait for node to initialize 


cmd_vel_pub.publish(command) 
time.sleep(2) 
 
DIST = 2
dist = DIST
        
while(not rospy.is_shutdown()):
    if(min_front > 2):
        temp = 0.2 if min_left > 1.5 else 0
        command.angular.z = command.angular.z + 0.2 if command.angular.z < temp else command.angular.z - 0.2
        command.linear.x = min(0.5, command.linear.x + 0.05) 
        dist = min(0.05 + dist, DIST) 
        print("C") 
    elif(min_left < dist):            
        command.angular.z = max(-0.2, command.angular.z - 0.02) 
        command.linear.x = max(0.1, command.linear.x - 0.05) 
        dist = max(dist - 0.05, DIST/5) 
        print("A") 
    elif(min_right < dist): 
        command.angular.z = min(0.5, command.angular.z + 0.05) 
        command.linear.x = max(0.1, command.linear.x - 0.05) 
        dist = max(dist - 0.05, DIST/5) 
        print("D")
    elif(min_front < 2 and  min_left < 0.5):
        command.angular.z = min(-0.2, command.angular.z - 0.02) 
        command.linear.x = max(0.1, command.linear.x - 0.05) 
        dist = max(dist - 0.05, DIST/5) 
        print("v")
    elif(min_front < 2 and  min_right < 0.5 ):
        command.angular.z = min(+0.2, command.angular.z + 0.02) 
        command.linear.x = max(0.1, command.linear.x - 0.05) 
        dist = max(dist - 0.05, DIST/5) 
        print("v")       

    cmd_vel_pub.publish(command)
    rate.sleep()


