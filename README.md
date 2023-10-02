# Turtlebot3 Recpetionist
Implementation of a receptionist robot using a Turtlebot3 with ROS2.

The purpose of the system is to accompany people or to deliver messages between offices in a building. The system can be used through the implementation of a telegram bot.

# Installation:
## Requirements:
* A turtlebot3 already configured with Ubuntu22 and ROS2 Humble ([see here](https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/#sbc-setup))
* A computer with Ubuntu22 and ROS2 Humble
## ROS2 Humble ([Official guide](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html))
```
$ sudo apt install software-properties-common
$ sudo add-apt-repository universe
$ sudo apt update && sudo apt install curl -y
$ sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install ros-humble-desktop
$ sudo apt install ros-humble-ros-base
$ sudo apt install ros-dev-tools
$ echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
```
## ROS2 Packages
```
$ sudo apt install ros-humble-gazebo-*
$ sudo apt install ros-humble-cartographer
$ sudo apt install ros-humble-cartographer-ros
$ sudo apt install ros-humble-navigation2
$ sudo apt install ros-humble-nav2-bringup
```
## Turtlebot3 Packages ([Official guide](https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup))
```
$ mkdir -p ~/turtlebot3_ws/src
$ cd ~/turtlebot3_ws/src/
$ git clone -b humble-devel https://github.com/ROBOTIS-GIT/DynamixelSDK.git
$ git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
$ git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3.git
$ cd ~/turtlebot3_ws
$ colcon build --symlink-install
$ echo 'source ~/turtlebot3_ws/install/setup.bash' >> ~/.bashrc
$ echo 'export ROS_DOMAIN_ID=30 #TURTLEBOT3' >> ~/.bashrc
$ echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
$ source ~/.bashrc
```
## Additional libraries
```
$ sudo apt install ffmpeg
$ pip install python-telegram-bot==13.13
$ pip install SpeechRecognition
$ pip install pydub
```
## Clone Repository
```
$ cd ~/turtlebot3_ws/src/turtlebot3
$ git clone https://github.com/fromstar/turtlebot3_receptionist.git
$ cd ~/turtlebot3_ws/
$ colcon build --packages-select turtlebot3_navigation_povo --symlink-install
$ echo '~./turtlebot3_ws/install/setup.bash' >> ~/.bashrc
```
# Run the project
* Using the telegram bot "BotFather" create your own telegram bot ([Tutorial to how create a telegram bot](https://core.telegram.org/bots/tutorial)).
* In the "receptionist.py" file, assign the values to CHAT_ID="" and TOKEN="" with your telegram id and the token of the bot you created.
* Capture a map of the area you are interested in ([How to SLAM](https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/))
* In the configuration file, populate the dictionary containing the stanzas with their associated locations using this syntax:
```
  rooms:
     name_office_1:
         x:
         y:
         z:
         th:
     name_office2:
         x:
         y:
         z:
         th:
```
To help you find the correct positions and populate the dictionary, run the navigation node and in a second terminal the set_initial_pose node. Set the name of the room from which the robot starts and then modify the parameters of the associated room to find the correct position. 
* In the configuration file, populate the list containing the IDs of Telegram users who are allowed to use the service and assign the name of the room from which the robot starts.
* Run the navigation node loading the captured map ([How to Navigate](https://emanual.robotis.com/docs/en/platform/turtlebot3/navigation/#navigation)).
* In a new terminal initialize the starting position by executing the set_initial_pose node:
```
ros2 run turtlebot3_receptionist set_initial_pose
```
* Run the receptionist node:
```
ros2 run turtlebot3_receptionist receptionist
```
