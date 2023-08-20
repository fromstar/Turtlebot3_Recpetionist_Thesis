# Turtlebot3_Recpetionist_Thesis

## Installation Guide:
* Follow the Quick Start guide for the setup on the Pc remote and on the Turtlebot: https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/#pc-setup
  * IMPORTANT: Install the Turtlebot3 packages on the remote pc from source
* Make sure to have in the ~/.bashrc file these lines:
  * source /opt/ros/humble/setup.bash
  * source ~/turtlebot3_ws/install/setup.bash
  * export ROS_DOMAIN_ID=30 #TURTLEBOT3
  * export TURTLEBOT3_MODEL=burger    
* Go in the turtlebot3_ws/src/turtlebot3 folder
* Clone this repo with the correcto package name
* Install ffmpeg
  * sudo apt install ffmpeg 
* Install the necessary library
  * pip install python-telegram-bot==13.13
  * pip install SpeechRecognition
  * pip install pydub
* In the turtlebot3_ws:
  * colcon build --packages-select turtlebot3_navigation_povo --symlink-install
  * echo '~./turtlebot3_ws/install/setup.bash' >> ~/.bashrc
