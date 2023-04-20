# -*- coding:utf-8 -*-
# title           :带雪的岩石
# description     :带雪的岩石
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class RockSnow(Obj):
    """
    带雪的岩石
    """

    def __init__(self, name="雪岩", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="rock_snow.jpg", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=None, show_name=False,
                 model="rock_snow.obj", rotation=(0, 0, 0),
                 parent=None, gravity_only_for=[]):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": density,
            "color": color,
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name,
            "parent": parent,
            "rotation": rotation,
            "gravity_only_for": gravity_only_for,
            "model": model
        }
        super().__init__(**params)


if __name__ == '__main__':
    rock_snow = RockSnow()
    print(rock_snow)
