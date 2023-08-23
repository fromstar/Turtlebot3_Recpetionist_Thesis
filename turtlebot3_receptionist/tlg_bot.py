import speech_recognition as sr
from pydub import AudioSegment
import os
import yaml
from yaml.loader import SafeLoader

CONFIGURATION_DIR = "src/turtlebot3/turtlebot3_receptionist/turtlebot3_receptionist/configuration.yaml"
pending_tasks = []
current_users = {}

task_id = 1

def add_task(task,update):
    global task_id
    u_id = update.message.from_user['id']
    if not u_id in current_users:
        current_users[u_id] = {}
    current_users[u_id][task_id] = task
    pending_tasks.append([task,update,u_id,task_id])
    task_id += 1

def limit_access(update, context, command = False):
    id = update.message.from_user['id']
    with open(CONFIGURATION_DIR) as f:
        data = yaml.load(f,Loader=SafeLoader)
    allowed_ids = data["users"]
    if id in allowed_ids:
        if command:
            return True
        elif update.message.text == None:
            print(update.message.from_user['username'] + " send a vocal command")
            audio_handler(update, context)
        else:
            print(update.message.from_user['username'] + " send a text command")
            text_handler(update, context)
    else:
        update.message.reply_text("Sorry, your ID is not allowed to use this service.")
        return False

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
        if res == -1:
            print("Speech was unintelligible")
            update.message.reply_text("Speech was unintelligible")
        elif res == -2:
            update.message.reply_text("API was unavailable")
            print("API was unavailable")
        else:
            print("I heard from " + update.message.from_user['username'] + ": " + res)
            update.message.reply_text("I heard: " + res)
            update.message.reply_text("There are  " + str(len(pending_tasks)) + " pending tasks before yours")
            add_task(res,update)
            
        os.remove("msg.ogg")
        os.remove("msg.wav")
        
    except sr.UnknownValueError:
        return -1
    except sr.RequestError:
        print("API unavailable")
        return -2

def text_handler(update,context):
    text = update.message.text
    print(update.message.from_user['username'] + " wrote: " + text)
    update.message.reply_text("You wrote: " + text)
    update.message.reply_text("There are  " + str(len(pending_tasks)) + " pending tasks before yours")
    add_task(text,update)

def delete_task(u_id, t_id):
    current_users[u_id].pop(t_id)
    for i in range(0,len(pending_tasks)):
        if pending_tasks[i][3] == t_id:
            delete_task = pending_tasks.pop(i)
            break

def delete_command(update, context):
    if limit_access(update,context,True):
        if len(context.args) != 0:
            t_id = int(context.args[0])
            u_id = update.message.from_user['id']
            if t_id in current_users[u_id]:
                delete_task(u_id,t_id)
                update.message.reply_text("Task " + str(delete_task[2]) + " cancelled")
            else:
                update.message.reply_text("You don't have a task with the given ID")
        else:
            update.message.reply_text("Please insert the task id you want to delete")

def user_recap_command(update, context):
    if limit_access(update,context,True):
        recap = "Task id: Task\n"
        u_id = update.message.from_user['id']
        if u_id in current_users and len(current_users[u_id]) != 0:
            t_keys = current_users[u_id]
            for tk in t_keys:
                recap = recap + str(tk) + ": \t" + current_users[u_id][tk] + "\n"
            update.message.reply_text(recap)
        else:
            update.message.reply_text("You don't have pending tasks.")

def list_command(update, context):
    if limit_access(update,context,True):
        with open(CONFIGURATION_DIR) as f:
            data = yaml.load(f,Loader=SafeLoader)
        rooms_keys = list(data['rooms'].keys()) 
        lst = "Available offices: \n\n"
        lst += '\n'.join(map(str, rooms_keys))
        update.message.reply_text(lst)
        print(lst)

def help_command(update, context):
    if limit_access(update,context,True):
        lst = "/start: Start the bot\n"
        lst += "/list: List of available offices\n"
        lst += "/queue: See how many pending tasks there are\n"
        lst += "/delete \"task_id\": Delete a task with the given ID\n"
        lst += "/recap: List of your pending tasks\n"
        lst += "/help: List of the available commands\n"
        lst += "Send a vocal or a text message to tell me where I have to go\n\n"
        update.message.reply_text(lst)

def start_command(update, context):
    if limit_access(update,context,True):
        name = update.message.chat.first_name
        update.message.reply_text("Hello " + name)
        msg = "Use /help to see the list of the available commands\n\n"
        msg += "Please send a text or a vocal message with the office where I have to go"
        update.message.reply_text(msg)

def queue_command(update, context):
    if limit_access(update,context,True):
        update.message.reply_text("There are " + str(len(pending_tasks)) + " pending tasks")