from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import speech_recognition as sr
from pydub import AudioSegment
import os
import rclpy
from geometry_msgs.msg import PoseStamped
import yaml
from yaml.loader import SafeLoader
import speech_recognition as sr
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

CHAT_ID = ""
TOKEN = ""    
CONFIGURATION = "src/turtlebot3/turtlebot3_navigation_povo/turtlebot3_navigation_povo/configuration.yaml"

def navigation(msg,update):
    rclpy.init()
    go_to_node = rclpy.create_node("go_to_node")
    action_client = ActionClient(go_to_node,NavigateToPose, 'navigate_to_pose')

    found == False
    with open(CONFIGURATION) as f:
        data = yaml.load(f,Loader=SafeLoader)
    rooms_keys = list(data['rooms'].keys()) 
    for key in rooms_keys:
        if key in msg:
            found = True
            room = key
            break
        
    if found == False:
        update.message.reply_text("Room not found!")
        print("Room not found!")
    else:
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
        
    go_to_node.destroy_node()
    rclpy.shutdown()
    
def start_command(update, context):
    name = update.message.chat.first_name
    update.message.reply_text("Hello " + name)
    update.message.reply_text("Please insert room number: ")

def convert_audio():
    orig_audio = "msg.ogg"
    wav_audio = "msg.wav"
    song = AudioSegment.from_ogg(orig_audio)
    song.export(wav_audio, format="wav")
    
def audio_handler(update, context):
    file_audio = context.bot.get_file(update.message.voice.file_id)
    file_audio.download(f'msg.ogg')
    convert_audio()
    file_audio = sr.AudioFile('msg.wav')
    rec = sr.Recognizer()
    with file_audio as source:
        audio = rec.record(source)
    try:
        res = rec.recognize_google(audio)
        print(res)
        if res == -1:
            print("Speech was unintelligible")
            update.message.reply_text("Speech was unintelligible")
        elif res == -2:
            update.message.reply_text("API was unavailable")
            print("API was unavailable")
        else:
            print(update.message.chat.first_name + " said: " + res)
            update.message.reply_text(update.message.chat.first_name + "said: " + res)
            navigation(res,update)
        os.remove("msg.ogg")
        os.remove("msg.wav")
        
    except sr.UnknownValueError:
        return -1
    except sr.RequestError:
        print("API unavailable")
        return -2

def text_handler(update,context):
    text = update.message.text
    print(update.message.chat.first_name+ " wrote: " + text)
    update.message.reply_text("You wrote: " + text)
    navigation(text,update)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.voice,audio_handler))
    dp.add_handler(MessageHandler(Filters.text,text_handler))
    
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__":
    main()
