import time
import sys

from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from unitree_sdk2py.go2.vui.vui_client import VuiClient

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

    client: VuiClient = robot.ensure_client(VuiClient.default_service_name)
    client.SetTimeout(3.0)
    client.Init()

    for i in range(1, 11):
        robot.logger.info("#################GetBrightness####################")
        code, level = client.GetBrightness()

        if code != 0:
            robot.logger.error(f"get brightness error. code: {code}")
        else:
            robot.logger.info(f"get brightness success. level: {level}")

        time.sleep(1)

        robot.logger.info("#################SetBrightness####################")

        code = client.SetBrightness(i)

        if code != 0:
            robot.logger.error(f"set brightness error. code: {code}")
        else:
            robot.logger.info(f"set brightness success. level: {i}")

        time.sleep(1)

    robot.logger.info("#################SetBrightness 0####################")

    code  = client.SetBrightness(0)

    if code != 0:
        robot.logger.error(f"set brightness error. code: {code}")
    else:
        robot.logger.info("set brightness 0 success.")

    for i in range(1, 11):
        robot.logger.info("#################GetVolume####################")
        code, level = client.GetVolume()

        if code != 0:
            robot.logger.error(f"get volume error. code: {code}")
        else:
            robot.logger.info(f"get volume success. level: {level}")

        time.sleep(1)

        robot.logger.info("#################SetVolume####################")

        code = client.SetVolume(i)

        if code != 0:
            robot.logger.error(f"set volume error. code: {code}")
        else:
            robot.logger.info(f"set volume success. level: {level}")

        time.sleep(1)

    robot.logger.info("#################SetVolume 0####################")

    code  = client.SetVolume(0)

    if code != 0:
        robot.logger.error(f"set volume error. code: {code}")
    else:
        robot.logger.info("set volume 0 success.")
