# -*- coding:utf-8 -*-
# title           :地球
# description     :地球
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class Diamond(Obj):
    """
    钻石
    """

    def __init__(self, name="钻石", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="earth1.jpg", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False,
                 trail_color=None, show_name=False,
                 parent=None):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": 5507.85,
            "color": (7, 0, 162),
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name,
            "parent": parent
        }
        super().__init__(**params)


if __name__ == '__main__':
    diamond = Diamond()
    print(diamond)
