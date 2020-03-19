#!/usr/bin/env python3


import time
import py_trees


class Time(py_trees.behaviour.Behaviour):
    def __init__(self, name, duration):
        super().__init__(name=name)
        self.duration = duration

    def update(self):
        self.time = time.time() + self.duration
        return py_trees.common.Status.SUCCESS


class NewAction(py_trees.behaviour.Behaviour):
    def __init__(self, name, robot):
        super().__init__(name=name)
        self.robot = robot

    def update(self):
        if self.robot._current_action is None:
            available = self.robot.fetch_available_actions()
            best_action = self.robot.compute_best_action(available)
            return py_trees.common.Status.SUCCESS if self.robot.preempt_action(best_action) else py_trees.common.Status.FAILURE
        else:
            return py_trees.common.Status.SUCCESS


class ConfirmAction(py_trees.behaviour.Behaviour):
    def __init__(self, name, robot):
        super().__init__(name=name)
        self.robot = robot

    def update(self):
        return py_trees.common.Status.SUCCESS if self.robot.confirm_current_action() else py_trees.common.Status.FAILURE
