import rclpy
from rclpy.node import Node
from ros2_aruco_interfaces.msg import ArucoMarkers
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster



class ArucoMarker():
    def __init__(self, ID, pose, orient):
        self.ID = ID
        self.position = pose
        self.orientation = orient
        # print('ID: ', ID)


class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(ArucoMarkers, '/aruco_markers', self.listener_callback, 30)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(TransformStamped, '/tf', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

    def listener_callback(self, msg):
        # self.get_logger().info('I heard: "%f"' % msg.marker_ids[0])
        self.create_Aruco(msg)
        self.publisher_tf(msg)

    def publisher_tf(self, msg):
        t = TransformStamped()


        for idx, id in enumerate(msg.marker_ids):
            # Read message content and assign it to
            # corresponding tf variables
            t.header.stamp = self.get_clock().now().to_msg()
            t.header.frame_id = 'base_link_1'
            t.child_frame_id = 'marker' + str(id)

            # Turtle only exists in 2D, thus we get x and y translation
            # coordinates from the message and set the z coordinate to 0
            t.transform.translation.x = msg.poses[idx].position.z
            t.transform.translation.y = msg.poses[idx].position.y
            t.transform.translation.z = msg.poses[idx].position.x

            # For the same reason, turtle can only rotate around one axis
            # and this why we set rotation in x and y to 0 and obtain
            # rotation in z axis from the message
            # q = quaternion_from_euler(0, 0, msg.theta)
            t.transform.rotation.x = float(0)
            t.transform.rotation.y = float(0)
            t.transform.rotation.z = msg.poses[idx].orientation.x
            t.transform.rotation.w = msg.poses[idx].orientation.w

            # Send the transformation
            # self.tf_broadcaster.sendTransform(t)

            # msg1.transforms.transform = msg.poses[0]
            # msg1.transforms[0].transform.rotation = msg.poses[0].orientation
            # msg1.transforms[0].child_frame_id = str('marker' + msg.marker_ids[0])

            self.tf_broadcaster.sendTransform(t)
            # self.publisher_.publish(t)
            # self.get_logger().info('Publishing: "%s"' % msg.data)

    def create_Aruco(self, msg):
        ID = msg.marker_ids
        pose = msg.poses
        for idx, id in enumerate(ID):
            ArucoMarker(id, pose[idx].position, pose[idx].orientation)


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()