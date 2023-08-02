# -*- coding:utf-8 -*-
# title           :地月场景模拟
# description     :地月场景模拟（月球始终一面朝向地球、月球对地球的扰动）
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================


from bodies import Sun, Earth, Moon
from objs import CoreValagaClas, SciFiBomber, WaterDrop
from common.consts import AU, SECONDS_PER_DAY, SECONDS_PER_WEEK, SECONDS_PER_MONTH
from sim_scenes.func import ursina_run, camera_look_at
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent

if __name__ == '__main__':
    """
    月球始终一面朝向地球
    月球对地球的扰动
    """
    OFFSETTING = 0
    # TODO: 可以抵消月球带动地球的力，保持地球在原地
    # OFFSETTING = 0.01265
    # sun = Sun(name="太阳", size_scale=6e1, init_position=[0, 0, -AU]).set_ignore_gravity(True)
    earth = Earth(init_position=[0, -200000, -50000],
                  texture="earth_hd.jpg",
                  rotate_angle=-23.44,
                  init_velocity=[OFFSETTING, 0, 0], size_scale=2.5e1)  # 地球放大 5 倍，距离保持不变
    water_drop = WaterDrop(init_position=[0, 0, AU / 40],
                           init_velocity=[-1, 0, 0],
                           size_scale=5e4)
    # moon = Moon(init_position=[0, 0, 363104],  # 距地距离约: 363104 至 405696 km
    #             init_velocity=[-1.03, 0, 0], size_scale=2e1)  # 月球放大 10 倍，距离保持不变
    # moon.set_light_disable(True)
    d = 100000
    x_offset = - 2 * d
    ship_list = []
    for x in range(5):
        for z in range(5):
            core_valaga_clas = CoreValagaClas(size_scale=15,
                                              init_position=[x_offset + x * d, -30000, z * d - 20000]).set_ignore_gravity(True)
            ship_list.append(core_valaga_clas)

    for x in range(5):
        for z in range(5):
            sci_fi_bomber = SciFiBomber(size_scale=3.5,
                                        init_position=[x_offset + x * d, 30000, z * d - 20000]).set_ignore_gravity(True)
            ship_list.append(sci_fi_bomber)

    earth.rotation_speed /= 6  # 地球的转速降低50倍

    bodies = [earth, water_drop] + ship_list


    def on_timer_changed(time_data: TimeData):
        if time_data.total_days > 27.5:
            exit(0)


    def on_ready():
        for body in bodies:
            if isinstance(body, CoreValagaClas):
                body.planet.rotation_x = 0 # -10
            elif isinstance(body, SciFiBomber):
                 body.planet.rotation_x = -90

        water_drop.planet.rotation_z = 90


    # 订阅事件后，上面2个函数功能才会起作用
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies,
               SECONDS_PER_DAY / 24,
               # SECONDS_PER_WEEK * 4,
               position=(0, 0, -220000),
               show_grid=False,
               # cosmic_bg="",
               # save_cube_map=True,
               timer_enabled=True,
               show_camera_info=False,
               show_control_info=False,
               view_closely=True
               # show_trail=True
               )
