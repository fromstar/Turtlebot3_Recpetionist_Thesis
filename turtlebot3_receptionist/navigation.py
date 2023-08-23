import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
import yaml
from yaml.loader import SafeLoader
from std_srvs.srv import Empty 
from turtlebot3_receptionist.tlg_bot import CONFIGURATION_DIR, pending_tasks, delete_task

def reinizialize_loc_callback(future):
    rclpy.shutdown()

def get_result_callback(future):
    res = future.result().status
    print(res)
    if res == 4:
        delete_task(pending_tasks[0][2],pending_tasks[0][3])
        rclpy.shutdown()
    else:
        srv_node = rclpy.create_node("reinizialize_loc_node")
        srv_client = srv_node.create_client(Empty, "reinitialize_global_localization")
        req = Empty.Request()
        srv_future = srv_client.call_async(req)
        srv_future.add_done_callback(reinizialize_loc_callback)
        rclpy.spin(srv_node)

def task_response_callback(future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        print("Goal rejected")
        return
    print("Goal accepted")
    get_result_future = goal_handle.get_result_async()
    get_result_future.add_done_callback(get_result_callback)

def navigation():
    msg = pending_tasks[0][0]
    update = pending_tasks[0][1]
    msg = msg.lower()
    found = False
    with open(CONFIGURATION_DIR) as f:
        data = yaml.load(f,Loader=SafeLoader)
    rooms_keys = list(data['rooms'].keys()) 
    for key in rooms_keys:
        if key in msg:
            found = True
            room = key
            break
        
    if found == False:
        update.message.reply_text("Room not found!")
        delete_task(pending_tasks[0][2],pending_tasks[0][3])
        print("Room not found!")

    else:
        rclpy.init()
        go_to_node = rclpy.create_node("go_to_node")
        action_client = ActionClient(go_to_node,NavigateToPose, 'navigate_to_pose')
        room_pos = data['rooms'][room]
        msg = PoseStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp.sec = 0
        msg.pose.position.x = float(room_pos['x'])
        msg.pose.position.y = float(room_pos['y'])
        msg.pose.position.z = float(room_pos['z'])
        msg.pose.orientation.z = float(room_pos['th'])
        while not action_client.wait_for_server(timeout_sec=1.0):
            print("Wait, action server not available")
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = msg
        goal_msg.behavior_tree = ''
        goal_future = action_client.send_goal_async(goal_msg)
        goal_future.add_done_callback(task_response_callback)
        rclpy.spin(go_to_node) 
        go_to_node.destroy_node()