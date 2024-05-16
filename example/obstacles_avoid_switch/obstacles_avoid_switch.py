import time
import sys

from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from unitree_sdk2py.go2.obstacles_avoid.obstacles_avoid_client import ObstaclesAvoidClient

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

    client: ObstaclesAvoidClient = robot.ensure_client(ObstaclesAvoidClient.default_service_name)
    client.SetTimeout(3.0)
    client.Init()

    while True:
        robot.logger.info("##################GetServerApiVersion###################")
        code, serverAPiVersion = client.GetServerApiVersion()
        if code != 0:
            robot.logger.error(f"get server api error. code: {code}")
        else:
            robot.logger.info(f"get server api version: {serverAPiVersion}")

        if serverAPiVersion != client.GetApiVersion():
            robot.logger.error("api version not equal.")

        time.sleep(3)

        robot.logger.info("##################SwitchGet###################")
        code, enable = client.SwitchGet()
        if code != 0:
            robot.logger.error(f"switch get error. code: {code}")
        else:
            robot.logger.info(f"switch get success. enable: {enable}")
            
        time.sleep(3)
        
        robot.logger.info("##################SwitchSet (on)###################")
        code = client.SwitchSet(True)
        if code != 0:
            robot.logger.error(f"switch set error. code: {code}")
        else:
            robot.logger.info(f"switch set success.")
            
        time.sleep(3)

        robot.logger.info("##################SwitchGet###################")
        code, enable1 = client.SwitchGet()
        if code != 0:
            robot.logger.error(f"switch get error. code: {code}")
        else:
            robot.logger.info(f"switch get success. enable: {enable1}")
            
        time.sleep(3)

        robot.logger.info("##################SwitchSet (off)###################")
        code = client.SwitchSet(False)
        if code != 0:
            robot.logger.error(f"switch get error. code: {code}")
        else:
            robot.logger.info("switch set success.")
            
        time.sleep(3)

        robot.logger.info("##################SwitchGet###################")
        code, enable1 = client.SwitchGet()
        if code != 0:
            robot.logger.error(f"switch get error. code: {code}")
        else:
            robot.logger.info(f"switch get success. enable: {enable1}")
            
        time.sleep(3)


        robot.logger.info("##################SwitchSet (enable)###################")

        code = client.SwitchSet(enable)
        if code != 0:
            robot.logger.error(f"switch get error. code: {code}")
        else:
            robot.logger.info(f"switch set success. enable: {enable}")
            
        time.sleep(3)

        robot.logger.info("##################SwitchGet###################")
        code, enable = client.SwitchGet()
        if code != 0:
            robot.logger.error(f"switch get error. code: {code}")
        else:
            robot.logger.info(f"switch get success. enable: {enable}")
            
        time.sleep(3)
        