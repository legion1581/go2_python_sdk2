import time
import sys

from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from unitree_sdk2py.go2.audiohub.audiohub_client import AudioHubClient

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
    client.SetTimeout(3.0)
    client.Init()

    # uploading mp3
    robot.logger.info("Uploading Audio files")
    client.AudioPlayerUploadAudioFile("sound_1.mp3")

    # Get the list of Audio Files
    robot.logger.info("Getting list of Audio Files")
    code, audio_list = client.AudioPlayerGetAudioList()
    robot.logger.info(f"Audio list: {audio_list}")

    # Set the Play mode 
    robot.logger.info("Setting Play mode")
    code = client.AudioPlayerSetPlayMode('single_cycle')

    # Get the Play mode 
    robot.logger.info("Getting Play mode")
    code, play_mode = client.AudioPlayerGetPlayMode()
    robot.logger.info(f"PlayMode: {play_mode}")

    # Play the first audio in the list
    robot.logger.info("Playing the first audio in the list")
    uuid = audio_list['audio_list'][0]['UNIQUE_ID']
    client.AudioPlayerPlayByUUID(uuid)
    time.sleep(1)

    # Pause
    robot.logger.info("pause the audio..")
    client.AudioPlayerPause()
    time.sleep(1)

    # Resume
    robot.logger.info("continue the audio")
    client.AudioPlayerResume()
    time.sleep(2)

    # Rename the first audio in the list
    robot.logger.info("Renaming the first audio in the list")
    uuid = audio_list['audio_list'][0]['UNIQUE_ID']
    client.AudioPlayerRenameRecord(uuid, "audio_1234")

    # Get the list of Audio Files
    robot.logger.info("Getting list of Audio Files")
    code, audio_list = client.AudioPlayerGetAudioList()
    robot.logger.info(f"Audio list: {audio_list}")

    # Deleting first audio file
    robot.logger.info("Deleting first audio in the list")
    uuid = audio_list['audio_list'][0]['UNIQUE_ID']
    client.AudioPlayerdeleteRecord(uuid)



    
