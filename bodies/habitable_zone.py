# -*- coding:utf-8 -*-
# title           :小行星
# description     :小行星
# author          :Python超人
# date            :2023-07-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies.body import Body, AU
from bodies.torus_zone import TorusZone


class HabitableZone(TorusZone):
    """
    模拟太阳系宜居带:
    目前认为 太阳系 的宜居带范围是从距离太阳0.95个天文单位 (约1.42亿千米)到 2.4个天文单位（约3.59亿千米）的范围为宜居带，
    其宽度约为2.17亿千米， 按照这个标准，太阳系的宜居带中只有三个大型天体，分别是地球、 月球 以及火星（1.52天文单位）。
    """

    def __init__(self, name="宜居带", mass=1.9891e30,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="green_alpha_1.png",
                 inner_radius=0.95,
                 outer_radius=1.67,
                 subdivisions=64,
                 size_scale=1.0,
                 distance_scale=1.0,
                 rotation_speed=0,
                 parent=None):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "inner_radius": inner_radius,
            "outer_radius": outer_radius,
            "subdivisions": subdivisions,
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "rotation_speed": rotation_speed,
            "parent": parent
        }
        super().__init__(**params)
        # 环状宜居带（inner_radius, outer_radius, subdivisions）
        # inner_radius:内圆半径 outer_radius:外圆半径，subdivisions:细分数，控制圆环的细节和精度
        # self.torus_zone = 0.95, 1.67, 64
        # 使用 texture="red_green_blue.png",
        # self.torus_zone = 0.20, 6.00, 64

    def ignore_gravity_with(self, body):
        """
        是否忽略指定天体的引力
        @param body:
        @return:
        """
        # 小行星只对恒星有引力，忽略其他行星的引力
        # if body.is_fixed_star:
        return True

        # return True


if __name__ == '__main__':
    habitable_zone = HabitableZone()
    print(habitable_zone)
