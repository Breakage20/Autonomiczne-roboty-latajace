import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage


class TFSubPub(Node):
    def __init__(self):
        super().__init__('tf_publisher')
        self.subscription = self.create_subscription(TFMessage, '/tf', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(TFMessage, '/tf1', 10)
        timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.publisher_callback)

    def listener_callback(self, msg):
        print('dupa')

    
    def publisher_callback(self):
        msg = TFMessage
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1




def main(args=None):
    rclpy.init(args=args)

    tf_publisher = TFSubPub()

    rclpy.spin(tf_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    tf_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()