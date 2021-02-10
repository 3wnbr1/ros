#!/usr/bin/env python3


"""Teb_obstacles localisation node."""


import rclpy
import copy

from rclpy.node import Node
from costmap_converter_msgs.msg import ObstacleArrayMsg, ObstacleMsg
from visualization_msgs.msg import MarkerArray, Marker
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point32
from platform import machine
from transformix_msgs.srv import TransformixParametersTransformStamped

class Teb_obstacles(Node):

    def __init__(self):
        super().__init__("teb_dynamic_obstacles_node")
        self.simulation = True if machine() != "aarch64" else False

        self.allie = "obelix" if self.get_namespace().strip("/") == "asterix" else "asterix"

        self.get_allie_odom_transformation()

        self.allies_subscription_ = self.create_subscription(
            Odometry, f'/{self.allie}/odom', self.allies_subscription_callback, 10)
        self.ennemies_subscription_ = self.create_subscription(
            MarkerArray, '/ennemies_positions_markers', self.ennemies_subscription_callback, 10)
        self.allies_subscription_
        self.ennemies_subscription_

        self.obstacles_publisher_ = self.create_publisher(ObstacleArrayMsg, 'obstacles', 10)

        self.dictionary_index_id = {"0":0, "1":0, "2":0}

        self.last_time_allie_callback = self.get_clock().now().to_msg()

        self.initObstaclesArray()

        self.create_timer(0.5, self.send_obstacles)

        self.get_logger().info('teb_dynamic_obstacles node is ready')

    def get_allie_odom_transformation(self):
        if self.simulation:
            return

        get_tf_client = self.create_client(TransformixParametersTransformStamped, f'/{self.allie}/get_odom_map_tf')

        if not get_tf_client.wait_for_service(timeout_sec=15.0):
            self.get_logger().info(f'No service /{self.allie}/get_odom_map_tf availible, is there ony one robot?')
            return
        get_tf_request = TransformixParametersTransformStamped.Request()
        future = get_tf_client.call_async(get_tf_request)
        rclpy.spin_until_future_complete(self, future)
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().info(
                'Service call failed %r' % (e,))
        else:
            self.odom_map_tf = response.transform_stamped
    def initObstaclesArray(self):
        """ObstacleArray index 0: allie, index 1-2: ennemies"""
        self.obstacles = ObstacleArrayMsg()
        self.obstacles.header.frame_id = "map"
        self.obstacles.obstacles.append(ObstacleMsg())
        self.obstacles.obstacles.append(ObstacleMsg())
        self.obstacles.obstacles.append(ObstacleMsg())
        for i in range(3):
            self.obstacles.obstacles[i].header.frame_id = "map"
            self.obstacles.obstacles[i].polygon.points = [Point32()]
            self.obstacles.obstacles[i].polygon.points[0].x = -1.0
            self.obstacles.obstacles[i].polygon.points[0].y = -1.0
            self.obstacles.obstacles[i].radius = 0.15
        self.previous_obstacles = copy.deepcopy(self.obstacles)

    def get_diff_time(self, t1, t2):
        return float(t1.sec - t2.sec + (t1.nanosec - t2.nanosec)*1e-9)

    def set_obstacle(self, index, marker):
        self.previous_obstacles.obstacles[index] = copy.deepcopy(self.obstacles.obstacles[index])
        self.obstacles.obstacles[index].header = marker.header
        self.obstacles.obstacles[index].polygon.points[0].x = marker.pose.position.x
        self.obstacles.obstacles[index].polygon.points[0].y = marker.pose.position.y

        dt = float(self.get_diff_time(marker.header.stamp, self.previous_obstacles.obstacles[index].header.stamp))

        if dt != 0.0:
            self.obstacles.obstacles[index].velocities.twist.linear.x = (
                marker.pose.position.x - self.previous_obstacles.obstacles[index].polygon.points[0].x
            ) / dt

            self.obstacles.obstacles[index].velocities.twist.linear.y = (
                marker.pose.position.y - self.previous_obstacles.obstacles[index].polygon.points[0].y
            ) / dt


    def allies_subscription_callback(self, msg):
        """Determine the pose of base_link in map
           set the dynamic obstacle for teb_local_planner"""
        if self.get_diff_time(self.get_clock().now().to_msg(), self.last_time_allie_callback) > 0.3:
            pose = msg.pose.pose
            x = pose.position.x + self.odom_map_tf.transform.translation.x
            y = pose.position.y + self.odom_map_tf.transform.translation.y
            tmp_marker = Marker()
            tmp_marker.pose.position.x = x
            tmp_marker.pose.position.y = y
            self.set_obstacle(0, tmp_marker)
            self.last_time_allie_callback = self.get_clock().now().to_msg()

    def ennemies_subscription_callback(self, msg):
        """Identity the ennemie marker in assurancetourix marker_array detection
           set the dynamic obstacle for teb_local_planner"""
        for ennemie_marker in msg.markers:
            if ennemie_marker.id <= 10:
                in_dict = False
                for index in range(1,2):
                    if self.dictionary_index_id[f"{index}"] == ennemie_marker.id:
                        self.set_obstacle(index, ennemie_marker)
                        in_dict = True
                if not in_dict:
                    if self.dictionary_index_id["1"] == 0:
                        self.dictionary_index_id["1"] = ennemie_marker.id
                    elif self.dictionary_index_id["2"] == 0:
                        self.dictionary_index_id["2"] = ennemie_marker.id
                    else:
                        self.get_logger().info('obstacleArray index limit, is there 3 ennemies, or is it a bad marker detection')

    def send_obstacles(self):
        self.obstacles_publisher_.publish(self.obstacles)

def main(args=None):
    """Entrypoint."""
    rclpy.init(args=args)
    teb_obstacles = Teb_obstacles()
    try:
        rclpy.spin(teb_obstacles)
    except KeyboardInterrupt:
        pass
    teb_obstacles.destroy_node()
    rclpy.shutdown()
