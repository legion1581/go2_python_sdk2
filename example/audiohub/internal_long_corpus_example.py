import time
import sys

from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from unitree_sdk2py.go2.audiohub.audiohub_client import AudioHubClient
from unitree_sdk2py.go2.audiohub.audiohub_api import *


from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.utils.logger import setup_logging
from unitree_sdk2py.sdk.sdk import create_standard_sdk

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        network_interface = sys.argv[1]
    else:
        network_interface = None
    
    # Set up a logger with verbose output enabled. This allows for detailed logging output which can be useful for debugging.
    setup_logging(verbose=True)

    # Initialize the SDK with a custom name, which is used to identify the SDK instance and its associated logs.
    sdk = create_standard_sdk('UnitreeGo2SDK')

    # Create a robot instance using the DDS protocol. 
    # `domainId=0` is used as it is currently the standard for all Go2 robots, although a script to change this on the robot is planned.
    # `interface="eth0"` specifies the network interface the DDS should use.
    # Each robot is uniquely identified by a serial number, allowing for multiple robots to be managed by the SDK.
    # Check if the network interface argument is provided

    communicator = DDSChannelFactoryInitialize(domainId=0, networkInterface=network_interface)
    robot = sdk.create_robot(communicator, serialNumber='B42D2000XXXXXXXX')

    client: AudioHubClient = robot.ensure_client(AudioHubClient.default_service_name)
    client.SetTimeout(120.0)
    client.Init()

    # Playing mp3 stored in /unitree/module/audio_hub/audio_player/internal_long_corpus
    robot.logger.info("Playing vui_cn_music_1.mp3")
    client.InternalLongCorpusPlay('vui_cn_music_1.mp3')

    # Waiting for the playback completion
    robot.logger.info("Waiting for playback to complete")
    code = client.InternalLongCorpusPlaybackCompleted()
    if code == 0:
        robot.logger.info("Playback Completed")
    else:
        robot.logger.info("Playback Completed Timed out")

    # Stop
    robot.logger.info("Stopping vui_cn_music_1.mp3")
    client.InternalLongCorpusStop()


