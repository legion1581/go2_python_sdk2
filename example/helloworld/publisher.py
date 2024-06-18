import time
import sys

from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from user_data import *

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

    # Create a publisher to publish the data defined in UserData class
    pub = communicator.ChannelPublisher("topic", UserData)
    pub.Init()

    for i in range(30):
        # Create a Userdata message 
        msg = UserData(" ", 0)
        msg.string_data = "Hello world"
        msg.float_data = time.time()

        # Publish message
        if pub.Write(msg, 0.5):
            robot.logger.info(f"Publish success. msg: {msg}")
        else:
            robot.logger.info("Waitting for subscriber.")

        time.sleep(1)

    pub.Close()
