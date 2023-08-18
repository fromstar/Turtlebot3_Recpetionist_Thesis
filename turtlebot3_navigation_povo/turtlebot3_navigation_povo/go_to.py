import rclpy
from time import sleep
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseWithCovarianceStamped
import yaml
from yaml.loader import SafeLoader
import os
import speech_recognition as sr
import time
from playsound import playsound
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus

def recognize_speech():  
    rec = sr.Recognizer()
    mic = sr.Microphone()
    print("Waiting room number: ")
    time.sleep(0)
    
    if not isinstance(rec, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(mic, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with mic as source:
        rec.adjust_for_ambient_noise(source)
        audio = rec.listen(source)
    try:
        res = rec.recognize_google(audio)
        return res
    
    except sr.UnknownValueError:
        return -1
    except sr.RequestError:
        print("API unavailable")
        return -2

def main(args=None):
    rclpy.init(args=args)

    # go_to_node = rclpy.create_node("go_to_node")
    # go_to_pub = go_to_node.create_publisher(PoseStamped, 'goal_pose', 10)
    
    go_to_node = rclpy.create_node("go_to_node")
    action_client = ActionClient(go_to_node,NavigateToPose, 'navigate_to_pose')
    
    with open('src/turtlebot3/turtlebot3_navigation_povo/turtlebot3_navigation_povo/configuration.yaml') as f:
        data = yaml.load(f,Loader=SafeLoader)
    
    room = -1
    found = False
    # while True:
    while room == -1 or room == -2 or found == False:
        room = recognize_speech()
        print(room)
        if room == -1:
            print("Speech was unintelligible")
        elif room == -2:
            print("API was unavailable")
        else:
            rooms_keys = list(data['rooms'].keys())        
            for key in rooms_keys:
                if key in room:
                    found = True
                    room = key
                    break
            if found == False:
                print("Room not found: " + room)
                   
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
    rclpy.spin_until_future_complete(go_to_node,goal_future)
    # goal_handle = goal_future.result()
    # result_future = goal_handle.get_result_async()
    # while True:       
        # print(result_future.result())
        # print(GoalStatus.STATUS_SUCCEEDED)
        # print()
        # sleep(1)
        
    # for i in range(0,10):
    #     go_to_pub.publish(msg)
    #     sleep(0.2)
    # playsound('src/turtlebot3/turtlebot3_navigation_povo/audio/follow_me.wav')



if __name__ == '__main__':
    main()