import sys
if sys.prefix == '/Users/eduardofelix/scout_bot_mac/.pixi/envs/default':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/Users/eduardofelix/scout_bot_mac/ros_ws/install/scout_bot'
