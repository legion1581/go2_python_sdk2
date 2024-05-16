import time
import sys
from unitree_sdk2py.core.dds.channel import DDSChannelSubscriber, DDSChannelFactoryInitialize

from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.utils.logger import setup_logging
from unitree_sdk2py.sdk.sdk import create_standard_sdk


idl_data_class = IDLDataClass()

WirelessController_ = idl_data_class.get_data_class('WirelessController_')

key_state = [
    ["R1", 0],
    ["L1", 0],
    ["start", 0],
    ["select", 0],
    ["R2", 0],
    ["L2", 0],
    ["F1", 0],
    ["F2", 0],
    ["A", 0],
    ["B", 0],
    ["X", 0],
    ["Y", 0],
    ["up", 0],
    ["right", 0],
    ["down", 0],
    ["left", 0],
]


def WirelessControllerHandler(msg: WirelessController_):
    global key_state
    robot.logger.info(f"lx: {msg.lx}")
    robot.logger.info(f"lx: {msg.ly}")
    robot.logger.info(f"lx: {msg.rx}")
    robot.logger.info(f"lx: {msg.ry}")
    robot.logger.info(f"keys: {msg.keys}")

    #Update key state
    for i in range(16):
        key_state[i][1] = (msg.keys & (1 << i)) >> i

    robot.logger.info(key_state)



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
        
    sub = DDSChannelSubscriber("rt/wirelesscontroller", WirelessController_)
    sub.Init(WirelessControllerHandler, 10)
    
    while True:
        time.sleep(10.0)
