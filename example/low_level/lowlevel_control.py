import time
import sys

from unitree_sdk2py.core.dds.channel import DDSChannelPublisher, DDSChannelFactoryInitialize
from unitree_sdk2py.utils.crc import CRC
from unitree_sdk2py.utils.thread import Thread
import unitree_legged_const as go2

from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.utils.logger import setup_logging
from unitree_sdk2py.sdk.sdk import create_standard_sdk


idl_data_class = IDLDataClass()
LowCmd_ = idl_data_class.get_data_class('LowCmd_')

crc = CRC()

if __name__ == '__main__':

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
    pub = DDSChannelPublisher("rt/lowcmd", LowCmd_)
    pub.Init()
    
    cmd = idl_data_class.create_zeroed_dataclass(LowCmd_)
    cmd.head[0]=0xFE
    cmd.head[1]=0xEF
    cmd.level_flag = go2.LOWLEVEL
    cmd.gpio = 0
    for i in range(20):
        cmd.motor_cmd[i].mode = 0x01  # (PMSM) mode
        cmd.motor_cmd[i].q= go2.PosStopF
        cmd.motor_cmd[i].kp = 0
        cmd.motor_cmd[i].dq = go2.VelStopF
        cmd.motor_cmd[i].kd = 0
        cmd.motor_cmd[i].tau = 0

    while True:        
        # Toque controle, set RL_2 toque
        cmd.motor_cmd[go2.LegID["RL_2"]].q = 0.0 # Set to stop position(rad)
        cmd.motor_cmd[go2.LegID["RL_2"]].kp = 0.0
        cmd.motor_cmd[go2.LegID["RL_2"]].dq = 0.0 # Set to stop angular velocity(rad/s)
        cmd.motor_cmd[go2.LegID["RL_2"]].kd = 0.0
        cmd.motor_cmd[go2.LegID["RL_2"]].tau = 1.0 # target toque is set to 1N.m

        # Poinstion(rad) control, set RL_0 rad
        cmd.motor_cmd[go2.LegID["RL_0"]].q = 0.0  # Taregt angular(rad)
        cmd.motor_cmd[go2.LegID["RL_0"]].kp = 10.0 # Poinstion(rad) control kp gain
        cmd.motor_cmd[go2.LegID["RL_0"]].dq = 0.0  # Taregt angular velocity(rad/ss)
        cmd.motor_cmd[go2.LegID["RL_0"]].kd = 1.0  # Poinstion(rad) control kd gain
        cmd.motor_cmd[go2.LegID["RL_0"]].tau = 0.0 # Feedforward toque 1N.m
        
        cmd.crc = crc.Crc(cmd)

        #Publish message
        if pub.Write(cmd):
            robot.logger.info(f"Publish success. crc: {cmd.crc}")
        else:
            robot.logger.info("Waitting for subscriber.")

        time.sleep(0.002)