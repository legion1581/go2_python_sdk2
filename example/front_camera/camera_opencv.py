from unitree_sdk2py.core.dds.channel import DDSChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient
import cv2
import numpy as np
import sys

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


    client: VideoClient = robot.ensure_client(VideoClient.default_service_name)
    client.SetTimeout(3.0)
    client.Init()

    code, data = client.GetImageSample()

    # Request normal when code==0
    while code == 0:
        # Get Image data from Go2 robot
        code, data = client.GetImageSample()

        # Convert to numpy image
        image_data = np.frombuffer(bytes(data), dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        # Display image
        cv2.imshow("front_camera", image)
        # Press ESC to stop
        if cv2.waitKey(20) == 27:
            break

    if code != 0:
        robot.logger.error(f"Get image sample error. code: {code}")
    else:
        # Capture an image
        cv2.imwrite("front_image.jpg", image)

    cv2.destroyWindow("front_camera")
