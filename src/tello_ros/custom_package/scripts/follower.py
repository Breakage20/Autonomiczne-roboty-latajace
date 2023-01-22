#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros2_aruco_interfaces.msg import ArucoMarkers
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import numpy as np
import time
from pid import PID

class Follower(Node):
    def __init__(self):
        super().__init__('follower')
        self.subscription = self.create_subscription(ArucoMarkers, '/aruco_markers', self.publisher_trajectory, 30)
        self.tag_id_sub=self.create_subscription(Int32,'/marker_id', self.get_id, 100)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Twist, '/drone1/cmd_vel', 20)
        self.velx = 0
        self.vely = 0
        self.velz = 0
        self.velw = 0
        self.max_speed=0.02
        self.timer = self.create_timer(0.05, self.check_for_new_message)
        self.move_cmd=Twist()
        self.last_received_message_time=0
        self.pid_lin = PID(P=0.5, I=0.0, D=0.0)
        self.pid_ang = PID(P=0.5, I=0.0, D=0.0)
        self.tag_id=0
    def get_id(self,msg):
        tag_id=msg.data
        tag_id=int(tag_id)
        self.tag_id=tag_id
    def check_for_new_message(self):
        # This function gets called every second (because we set the timer to 1.0 seconds)
        if time.time() - self.last_received_message_time > 0.05:
            self.move_cmd.linear.y = float(0)
            self.move_cmd.linear.x = float(0)
            self.move_cmd.linear.z = float(0)
            self.move_cmd.angular.z = float(0.2)
            self.publisher_.publish(self.move_cmd)
    def follow(self,msg,tag_id):
        if(time.time() - self.last_received_message_time < 0.05) and tag_id!=None:
            if (msg.poses[tag_id].position.x != 0):
                self.velx=self.pid_lin.update(msg.poses[tag_id].position.x)
            if (msg.poses[tag_id].position.y != 0):
                self.vely=self.pid_lin.update(msg.poses[tag_id].position.y)
            if (msg.poses[tag_id].position.z != 0.5):
                self.velz=self.pid_lin.update(-(msg.poses[tag_id].position.z - 0.5))
            if (msg.poses[tag_id].orientation.z != 0.0):
                self.velw=self.pid_ang.update(-(msg.poses[tag_id].orientation.z))

            if(0.48<msg.poses[tag_id].position.z<0.52):
                self.move_cmd.linear.x = float(0)
            else:
                self.move_cmd.linear.x = self.velz
           
            if(abs(msg.poses[tag_id].position.x)<0.02):
                self.move_cmd.linear.y = float(0)
            else:
                self.move_cmd.linear.y = self.velx

            if(abs(msg.poses[tag_id].position.y)<0.02):
                self.move_cmd.linear.z = float(0)
            else:
                self.move_cmd.linear.z = self.vely

            if(abs(msg.poses[tag_id].orientation.z)<0.02):
                self.move_cmd.angular.z = float(0)
            else:
                self.move_cmd.angular.z = self.velw

        if(time.time() - self.last_received_message_time < 0.05):
            self.publisher_.publish(self.move_cmd)
        else:
            pass
    def publisher_trajectory(self, msg):
        try:
            tag_ids = msg.marker_ids
            tag_index = tag_ids.index(self.tag_id)
            print("tag found")
        except ValueError:
            self.move_cmd.linear.y = float(0)
            self.move_cmd.linear.x = float(0)
            self.move_cmd.linear.z = float(0)
            self.move_cmd.angular.z = float(0.2)
            self.publisher_.publish(self.move_cmd)
            print(' not found in the list')
        else:
            self.follow(msg,tag_index)
            print("sledzi")
        self.last_received_message_time = time.time()

        #for idx, id in enumerate(msg.marker_ids):
        

    

    
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = Follower()

    rclpy.spin(minimal_publisher)


    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
