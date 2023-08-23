import rclpy
from time import sleep
from geometry_msgs.msg import PoseWithCovarianceStamped
import yaml
from yaml.loader import SafeLoader

CONFIGURATION_DIR = 'src/turtlebot3/turtlebot3_receptionist/turtlebot3_receptionist/configuration.yaml'

def main(args=None):
    rclpy.init(args=args)

    set_pose_node = rclpy.create_node("set_pose_node")
    set_pose_pub = set_pose_node.create_publisher(PoseWithCovarianceStamped, 'initialpose', 10)

    with open(CONFIGURATION_DIR) as f:
        data = yaml.load(f,Loader=SafeLoader)
    
    data = data['rooms'][data['starting_pose']]
    msg = PoseWithCovarianceStamped()
    msg.header.frame_id = 'map'
    msg.header.stamp.sec = 0
    msg.pose.pose.position.x = float(data['x'])
    msg.pose.pose.position.y = float(data['y'])
    msg.pose.pose.position.z = float(data['z'])
    msg.pose.pose.orientation.z = float(data['th'])

    for i in range(0,5):
        set_pose_pub.publish(msg)
        sleep(0.5)

    set_pose_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()