#!/usr/bin/env python3


import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Odometry
from cetautomatix.magic_points import elements
from nav2_msgs.action._navigate_to_pose import NavigateToPose_Goal
from strategix_msgs.srv import ChangeActionStatus, GetAvailableActions


class Robot(Node):
    def __init__(self):
        super().__init__(node_name='robot')
        robot = self.get_namespace()
        self._current_action = "ARUCO42"
        self._get_available_client = self.create_client(GetAvailableActions, '/strategix/available')
        self._change_action_status_client = self.create_client(ChangeActionStatus, '/strategix/action')
        self._get_available_request = GetAvailableActions.Request()
        self._change_action_status_request = ChangeActionStatus.Request()
        self._get_available_request.sender = robot
        self._change_action_status_request.sender = robot
        self._odom_sub = self.create_subscription(Odometry, '/odom', self._odom_callback, 1)

    def fetch_available_actions(self):
        """Fetch available actions for BT."""
        response = self._get_available_client.call(self._get_available_request)
        return response.available

    def preempt_action(self, action):
        """Preempt an action for the BT."""
        self._change_action_status_request.action = action
        self._change_action_status_request.request = "PREEMPT"
        response = self._change_action_status_request.call(self._change_action_status_request)
        self._current_action = action if response.success else None
        return response

    def drop_current_action(self):
        """Drop an action for the BT."""
        if self._current_action is None:
            return False
        self._change_action_status_request.action = self._current_action
        self._change_action_status_request.request = "DROP"
        response = self._change_action_status_request.call(self._change_action_status_request)
        self._current_action = None
        return response

    def confirm_current_action(self):
        """Confirm an action for the BT."""
        if self._current_action is None:
            return False
        self._change_action_status_request.action = self._current_action
        self._change_action_status_request.request = "CONFIRM"
        response = self._change_action_status_request.call(self._change_action_status_request)
        self._current_action = None
        return response

    def _odom_callback(self, msg):
        self.position = (msg.pose.pose.position.x, msg.pose.pose.position.y)

    def euler_to_quaternion(self, yaw, pitch, roll):
        """Conversion between euler angles and quaternions."""
        qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
        qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2)
        qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2)
        qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(yaw / 2)
        return [qx, qy, qz, qw]

    def compute_best_action(self, list):
        action_coeff_list = []
        # start = timeEndOfGame.time - 100.0
        for action in list:
            for key, value in elements.items():
                if key == action:
                    distance = np.sqrt(
                        (value[0] - self.position[0])**2 + (value[1] - self.position[1])**2)
                    coeff_distance = distance * 100 / 3.6
                    action_coeff_list.append((key, coeff_distance))
                    break
        max = 0
        best_action = None
        for action in action_coeff_list:
            if action[1] > max:
                max = action[1]
                best_action = action[0]
        self._current_action = best_action

    def get_goal_pose(self):
        """Get goal pose for action."""
        msg = NavigateToPose_Goal()
        value = elements[self._current_action]
        msg.pose.pose.position.z = 0.0
        msg.pose.pose.position.x = value[0]
        msg.pose.pose.position.y = value[1]
        q = self.euler_to_quaternion(value[2] if value[2] is not None else 0, 0, 0)
        msg.pose.pose.orientation.x = q[0]
        msg.pose.pose.orientation.y = q[1]
        msg.pose.pose.orientation.z = q[2]
        msg.pose.pose.orientation.w = q[3]
        return msg
