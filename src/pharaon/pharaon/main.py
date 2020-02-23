#!/usr/bin python3


"""Service Node for Pharaon."""


from rclpy.node import Node
import rclpy
import bluetooth


bd_addr = "00:14:03:06:61:BA"
port = 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))


class PharaonService(Node):

    def __init__(self):
        super().__init__('pharaon_service')
        bd_addr = "00:14:03:06:61:BA"
        port = 1
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect(bd_addr, port)
        sock.bind(("", port))
        sock.listen(1)

    def activate_callback(self, request, response):
        self.get_logger().info(str(request))
        if False:
            sock.send("demandeStatus;")
            client_sock, address = sock.accept()
            print("Accepted connection from ", address)
            data = client_sock.recv(1024)
            return ("reçu: ", data)

        if (data == "deploy"):
            sock.send("deploy;")
            return ("deployed")

    def __del__(self):
        sock.close()


def main(args=None):
    rclpy.init(args=args)

    pharaon_service = PharaonService()  # on instancie

    rclpy.spin(pharaon_service)
    rclpy.shutdown()
