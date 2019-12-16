#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
from turtlesim.msg import Color
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute

x = 0
y = 0
z = 0
yaw = 0

def background_color(r, g, b):
	rospy.wait_for_service('clear')
	clear_b = rospy.ServiceProxy('clear', Empty)
	rospy.set_param('/background_b',b)
	rospy.set_param('/background_r',r)
	rospy.set_param('/background_g',g)
	clear_b()

def transportation(x,y,angle):
	rospy.wait_for_service('turtle1/teleport_absolute')
	turtle1_teleport = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
	lineColor(255, 255, 255, 1)
	turtle1_teleport(x, y, angle)
	lineColor(204, 153, 255, 0)

def nextNum():
    lineColor(255,156,0, 1)
    rotate(78.69006753, False)
    move(3, 1.022, 1)
    rotate(78.69006753, True)
    lineColor(16, 71, 169, 0)

def lineColor(r, g, b, off):
    rospy.wait_for_service('turtle1/set_pen')
    turtle1_set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
    turtle1_set_pen(r, g, b, 2, off)


def rotate(angle, clockwise):
    global yaw
    yaw0 = yaw
    PI = 3.1415926535897
    vel_msg = Twist()
    ang_speed = 90 * 2 * PI / 360
    rel_ang = angle * 2 * PI / 360
    if (clockwise):
        vel_msg.angular.z = -abs(ang_speed)
    else:
        vel_msg.angular.z = abs(ang_speed)

    angle_moved = 0
    #loop_rate = rospy.Rate(120)
    cmd_vel_topic = 'turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
    while True:
        velocity_publisher.publish(vel_msg)
        #loop_rate.sleep()
        angle_moved = abs(yaw - yaw0)
        if not (angle_moved < rel_ang):
            break
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    


def callPoseback(pose_message):
    global x
    global y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta


def move(speed, distance, is_forward):
    velocity_message = Twist()
    global x, y
    x0 = x
    y0 = y

    if (is_forward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    distance_moved = 0.0
    #loop_rate = rospy.Rate(0.1)
    cmd_vel_topic = 'turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:
        #rospy.loginfo('Turtle moves forward')
        velocity_publisher.publish(velocity_message)

        #loop_rate.sleep()

        distance_moved = abs(0.4 * math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2))) 
        # print distance_moved
        if not (distance_moved < distance):
            #  rospy.loginfo('reached')
            break
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)
    

    
def makeTwo():
    move(3, 0.5, 1)
    rotate(90, True)
    move(3, 0.5, 1)
    rotate(90, True)
    move(3, 0.5, 1)
    rotate(270, True)
    move(3, 0.5, 1)
    rotate(90, False)
    move(3, 0.5, 1)

def makeFour():
	rotate(90, True)
	move(3, 0.5, 1)
	rotate(90, False)
	move(3, 0.5, 1)
	rotate(90, False)
	move(3, 0.5, 1)
	move(3, 1, False)
	rotate(90, True)

def makeSeven():
	move(3, 0.5, 1)
	rotate(116.56505, True)
	move(3,1.118034,1)
	rotate(206.56505, False)
	lineColor(255,156,0, 1)
	move(3, 0.5, 1)
	rotate(90, True)
	lineColor(16, 71, 169, 0)
	move(3, 0.5, 1)
	rotate(90, True)
	lineColor(255,156,0, 1)
	move(3, 0.5, 1)
	rotate(90, False)

def makeZero():
	move(3, 0.5, 1)
	rotate(90, True)
	move(3, 1, 1)
	rotate(90, True)
	move(3, 0.5, 1)
	rotate(90, True)
	move(3, 1, 1)
	rotate(90, True)
	rotate(63.4349488, True)
	lineColor(16, 71, 169, 1)
	move(3, 1.118033989,1)
	rotate(63.4349488, False)
	
	
    


print(x,y,yaw)
rospy.init_node('Turtlesim_number', anonymous=False, disable_signals=True)
position_topic = 'turtle1/pose'
pose_subscriber = rospy.Subscriber(position_topic, Pose, callPoseback)
time.sleep(1)  
background_color(255,156,0)
transportation(0.5, 5, 0)
lineColor(16, 71, 169, 0)
print(x, y, yaw)
rotate(60, True)
rotate(60, False)
makeTwo()
nextNum()
makeFour()
nextNum()
makeFour()
nextNum()
makeSeven()
nextNum()
makeTwo()
nextNum()
makeZero()
nextNum()
print(x,y,yaw)
#except rospy.ROSInterruptException:
#rospy.loginfo('node terminated')
