# -*- coding:utf-8 -*-
# title           :创建一个宇宙网格对象
# description     :创建一个宇宙网格对象
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import numpy as np
from ursina import Entity, camera, Vec3

from common.consts import AU
from sim_scenes.func import create_3d_card
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent


class OCamera:
    pass


class Camera3d(Entity):
    o = OCamera()
    is_ready = False

    def __init__(self, eye_distance=None, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

        if eye_distance is None:
            eye_distance = 1000

        camera.parent = self
        self.camera_pos = "right"
        self.eye_distance = eye_distance * UrsinaConfig.SCALE_FACTOR

    def switch_position(self):
        if self.camera_pos == "right":  # 摄像机右眼
            self.x -= 2 * self.eye_distance
            self.camera_pos = "left"
        elif self.camera_pos == "left":  # 摄像机左眼
            self.x += 2 * self.eye_distance
            self.camera_pos = "right"

    def update(self):
        pass

    @staticmethod
    def init(eye_distance=None, init_pos=None):
        Camera3d.is_ready = True

        def on_ready():
            Camera3d.init_on_ready(eye_distance, init_pos)

        UrsinaEvent.on_ready_subscription(on_ready)
        UrsinaEvent.on_before_evolving_subscription(Camera3d.exec_on_before_evolving)

    @staticmethod
    def init_on_ready(eye_distance, position):
        if hasattr(Camera3d.o, "init_position"):
            position = Camera3d.o.init_position
        elif position is None:
            position = camera.position
        else:
            position = np.array(position) * UrsinaConfig.SCALE_FACTOR

        Camera3d.o.camera3d = Camera3d(eye_distance)
        Camera3d.o.camera3d.position = position
        Camera3d.o._3d_card = create_3d_card()

    @staticmethod
    def exec_on_before_evolving(evolve_args):

        Camera3d.o._3d_card.switch_color()
        Camera3d.o.camera3d.switch_position()
        if Camera3d.o._3d_card.switch_flag == 1:
            evolve_args["evolve_dt"] = 0.0

        # if isinstance(camera.parent, Camera3d):
        #     camera.position = Vec3(0, 0, 0)
