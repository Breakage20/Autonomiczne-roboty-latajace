#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from ros2_aruco_interfaces.msg import ArucoMarkers
from geometry_msgs.msg import Twist
import numpy as np
import time
from pid import PID

class Follower(Node):
    def __init__(self):
        super().__init__('follower')
        self.subscription = self.create_subscription(ArucoMarkers, '/aruco_markers', self.publisher_trajectory, 30)
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
        self.pid = PID()
    def check_for_new_message(self):
        # This function gets called every second (because we set the timer to 1.0 seconds)
        if time.time() - self.last_received_message_time > 0.05:
            self.move_cmd.linear.y = float(0)
            self.move_cmd.linear.x = float(0)
            self.move_cmd.linear.z = float(0)
            self.move_cmd.angular.z = float(0)
            self.publisher_.publish(self.move_cmd)

    def publisher_trajectory(self, msg):

        self.last_received_message_time = time.time()

        for idx, id in enumerate(msg.marker_ids):
            if (msg.poses[idx].position.x != 0):
                self.velx=self.pid.update(msg.poses[idx].position.x)
            if (msg.poses[idx].position.y != 0):
                self.vely=self.pid.update(msg.poses[idx].position.y)
            if (msg.poses[idx].position.z != 0.5):
                self.velz=self.pid.update(-(msg.poses[idx].position.z - 0.5))

            if(0.48<msg.poses[idx].position.z<0.52):
                self.move_cmd.linear.x = float(0)
            else:
                self.move_cmd.linear.x = self.velz
                print("korekta odleglosci")
           
            if(abs(msg.poses[idx].position.x)<0.02):
                self.move_cmd.linear.y = float(0)
            else:
                self.move_cmd.linear.y = self.velx
                print("korekta LR")

            if(abs(msg.poses[idx].position.y)<0.02):
                self.move_cmd.linear.z = float(0)
            else:
                self.move_cmd.linear.z = self.vely
                print("korekta Wysokosci")


        if(time.time() - self.last_received_message_time < 0.05):
            self.publisher_.publish(self.move_cmd)
        else:
            pass

    

    
def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = Follower()

    rclpy.spin(minimal_publisher)


    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
