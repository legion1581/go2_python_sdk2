import math
import time
import sys
from unitree_sdk2py.core.dds.channel import DDSChannelSubscriber, DDSChannelFactoryInitialize

from unitree_sdk2py.go2.sport.sport_client import (
    SportClient,
    PathPoint,
    SPORT_PATH_POINT_SIZE,
)

from unitree_sdk2py.idl.idl_dataclass import IDLDataClass
from unitree_sdk2py.utils.logger import setup_logging
from unitree_sdk2py.sdk.sdk import create_standard_sdk


idl_data_class = IDLDataClass()

SportModeState_ = idl_data_class.get_data_class('SportModeState_')


class SportModeTest:
    def __init__(self, robot) -> None:
        # Time count
        self.t = 0
        self.dt = 0.01

        # Initial poition and yaw
        self.px0 = 0
        self.py0 = 0
        self.yaw0 = 0

        self.client: SportClient = robot.ensure_client(SportClient.default_service_name, enableLease=True)
        self.client.SetTimeout(2.0)
        self.client.Init()

    def GetInitState(self, robot_state: SportModeState_):
        self.px0 = robot_state.position[0]
        self.py0 = robot_state.position[1]
        self.yaw0 = robot_state.imu_state.rpy[2]

    def StandUpDown(self):
        self.client.StandDown()
        print("Stand down !!!")
        time.sleep(1)

        self.client.StandUp()
        print("Stand up !!!")
        time.sleep(1)

        self.client.StandDown()
        print("Stand down !!!")
        time.sleep(1)

        self.client.Damp()

    def VelocityMove(self):
        elapsed_time = 1
        for i in range(int(elapsed_time / self.dt)):
            self.client.Move(0.3, 0, 0.3)  # vx, vy vyaw
            time.sleep(self.dt)
        self.client.StopMove()

    def BalanceAttitude(self):
        self.client.Euler(0.1, 0.2, 0.3)  # roll, pitch, yaw
        self.client.BalanceStand()

    def TrajectoryFollow(self):
        time_seg = 0.2
        time_temp = self.t - time_seg
        path = []
        for i in range(SPORT_PATH_POINT_SIZE):
            time_temp += time_seg

            px_local = 0.5 * math.sin(0.5 * time_temp)
            py_local = 0
            yaw_local = 0
            vx_local = 0.25 * math.cos(0.5 * time_temp)
            vy_local = 0
            vyaw_local = 0

            path_point_tmp = PathPoint(0, 0, 0, 0, 0, 0, 0)

            path_point_tmp.timeFromStart = i * time_seg
            path_point_tmp.x = (
                px_local * math.cos(self.yaw0)
                - py_local * math.sin(self.yaw0)
                + self.px0
            )
            path_point_tmp.y = (
                px_local * math.sin(self.yaw0)
                + py_local * math.cos(self.yaw0)
                + self.py0
            )
            path_point_tmp.yaw = yaw_local + self.yaw0
            path_point_tmp.vx = vx_local * math.cos(self.yaw0) - vy_local * math.sin(
                self.yaw0
            )
            path_point_tmp.vy = vx_local * math.sin(self.yaw0) + vy_local * math.cos(
                self.yaw0
            )
            path_point_tmp.vyaw = vyaw_local

            path.append(path_point_tmp)

            self.client.TrajectoryFollow(path)
            
    def SpecialMotions(self):
        self.client.RecoveryStand()
        print("RecoveryStand !!!")
        time.sleep(1)
        
        self.client.Stretch()
        print("Sit !!!")
        time.sleep(1)  
        
        self.client.RecoveryStand()
        print("RecoveryStand !!!")
        time.sleep(1)


# Robot state
robot_state = idl_data_class.create_zeroed_dataclass(SportModeState_)
def HighStateHandler(msg: SportModeState_):
    global robot_state
    robot_state = msg


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
    time.sleep(1)

    test = SportModeTest(robot)
    test.GetInitState(robot_state)

    print("Start test !!!")
    while True:
        test.t += test.dt

        test.StandUpDown()
        test.VelocityMove()
        test.BalanceAttitude()
        test.TrajectoryFollow()
        test.SpecialMotions()

        time.sleep(test.dt)
