import time
import sys
from unitree_sdk2py.core.dds.channel import DDSChannelSubscriber, DDSChannelFactoryInitialize

from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.utils.logger import setup_logging
from unitree_sdk2py.sdk.sdk import create_standard_sdk


idl_data_class = IDLDataClass()
SportModeState_ = idl_data_class.get_data_class('SportModeState_')



def HighStateHandler(msg: SportModeState_):
    robot.logger.info("Position: ", msg.position)
    robot.logger.info("Velocity: ", msg.velocity)
    robot.logger.info("Yaw velocity: ", msg.yaw_speed)
    robot.logger.info("Foot position in body frame: ", msg.foot_position_body)
    robot.logger.info("Foot velocity in body frame: ", msg.foot_speed_body)


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

    sub = DDSChannelSubscriber("rt/sportmodestate", SportModeState_)
    sub.Init(HighStateHandler, 10)

    while True:
        time.sleep(10.0)
