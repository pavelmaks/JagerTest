import configparser
import os
import re
path = "settings.ini"

def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)

    config = configparser.ConfigParser()
    config.read(path)
    return config

def update_setting(path, section, data):
    """
    Update a setting
    """
    nums = re.findall(r'\d*\.\d+|\d+', data)

    nums = [float(i) for i in nums]
    config = get_config(path)
    startpos=str(nums[0])
    targetpos = str(nums[1])
    servopin = str(nums[2])
    frequencyservo = str(nums[3])
    servotime = str(nums[4])
    config.set(section, "startpos", startpos)
    config.set(section, "targetpos", targetpos)
    config.set(section, "servopin", servopin)
    config.set(section, "frequencyservo", frequencyservo)
    config.set(section, "servotime", servotime)
    with open(path, "w") as config_file:
        config.write(config_file)

update_setting(path,"Settings","2.5,10,22,50,11")