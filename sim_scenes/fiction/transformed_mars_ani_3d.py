# -*- coding:utf-8 -*-
# title           :改造后火星的3D效果
# description     :改造后火星的3D效果
# author          :Python超人
# date            :2023-07-21
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
import os
import sys

from bodies import Earth
from common.consts import SECONDS_PER_HOUR
from objs import Satellite2
from sim_scenes.func import ursina_run
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import create_directional_light
from simulators.ursina.ursina_event import UrsinaEvent


def create_satellites():
    # 卫星位置和初始速度信息
    satellite_infos = [
        # {"position": [0, 0, 10002], "velocity": [6.3, 0, 0]},
        # {"position": [0, 0, -12000], "velocity": [5.75, 0, 0]},
        # {"position": [0, 8000, 0], "velocity": [7.05, 0, 0]},
        # {"position": [0, -12002, 0], "velocity": [5.75, 0, 0]},
        {"position": [0, 0, 14000], "velocity": [0, 5, 0]},
        # {"position": [0, 0, -10000], "velocity": [0, 6.3, 0]},
    ]
    satellites = []
    for i, info in enumerate(satellite_infos):
        # Satellite Satellite2
        satellite = Satellite2(name=f'卫星{i + 1}', mass=4.4e10,
                               size_scale=2e2, color=(255, 200, 0),
                               init_position=info["position"],
                               init_velocity=info["velocity"])
        # info["satellite"] = satellite
        satellites.append(satellite)
    return satellites


def transformed_mars_ani(transformed_texture=None, texture=None, camera3d=False):
    trans_texture = transformed_texture.replace(".jpg", "_trans.png")
    # texture = transformed_texture
    # texture = os.path.join("transformed", texture)
    if len(sys.argv) > 1:
        camera3d = True
    print("sys.argv", sys.argv)
    # 创建带有云层的地球
    mars = Earth(
        texture=texture,
        rotate_angle=0,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=1)

    transformed_mars = Earth(
        texture=os.path.join("transformed", transformed_texture),
        rotate_angle=0,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=0.9996).set_ignore_gravity(True)

    trans_mars = Earth(
        texture=os.path.join("transformed", trans_texture),
        rotate_angle=0,
        init_position=[0, 0, 0],
        init_velocity=[0, 0, 0],
        size_scale=0.9990).set_ignore_gravity(True)

    bodies = [mars, transformed_mars, trans_mars]

    # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
    clouds = Earth(name="云层", texture="transparent_clouds.png",
                   rotate_angle=0,
                   size_scale=1.02, parent=mars)

    satellites = create_satellites()
    bodies = bodies + satellites
    bodies.append(clouds)

    if camera3d:
        # TODO: 开启3D摄像机
        from simulators.ursina.entities.camera3d import Camera3d
        # 3D摄像机初始化(两眼到鼻梁的距离为1000公里效果)
        Camera3d.init(eye_distance=1000)

    def on_ready():
        # 为了较好的立体效果，可以增加太阳光线，光线指向火星（target=mars）
        create_directional_light(position=(300, 0, -300), light_num=3, target=mars)
        for satellite in satellites:
            satellite.planet.enabled = False

    def on_timer_changed(time_data: TimeData):
        # mars.planet.opacity = 0.01
        opacity = round((time_data.total_hours - 1) / 10, 2)
        clouds_opacity = round(opacity - 0.5, 2)
        show_satellites = False
        if opacity > 1.0:
            opacity = 1.0
        elif opacity < 0.0:
            opacity = 0.0
        # clouds.planet.enabled = False
        if opacity >= 1.0:
            mars.planet.enabled = False  # 原火星完全消失

        if clouds_opacity > 1.0:
            clouds_opacity = 1.0
            show_satellites = True
        elif clouds_opacity < 0.0:
            clouds_opacity = 0.0

        clouds.planet.alpha = clouds_opacity  # 火星云层渐渐显示
        mars.planet.alpha = 1 - opacity  # 原火星渐渐消失
        # show_satellites = True
        if show_satellites:
            for satellite in satellites:
                satellite.planet.enabled = True
                # satellite.planet.look_at(mars.planet)

        # if time_data.total_hours > 10:
        #     trans_mars.planet.enabled = True
        # else:
        #     trans_mars.planet.enabled = False
        # if mars.planet.enabled == False:
        #     opacity = round((time_data.total_hours*5 - 11) / 10, 2)
        #     if opacity > 1.0:
        #         opacity = 1.0
        #     elif opacity < 0.0:
        #         opacity = 0.0
        #     transformed_mars.planet.alpha = 0.9
        #     trans_mars.planet.enabled = False

    # 订阅事件后，上面2个函数功能才会起作用
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)
    # 运行前会触发 on_ready
    UrsinaEvent.on_ready_subscription(on_ready)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(1.80 * mars.radius, 0, -38000),
               show_grid=False,
               show_camera_info=False,
               show_control_info=False,
               # cosmic_bg="none",
               timer_enabled=True,
               show_timer=True,
               view_closely=0.001)  # 近距离观看 view_closely=True或0.001


if __name__ == '__main__':
    transformed_mars_ani(
        transformed_texture="mars.jpg",
        texture="mars.png",
        camera3d=True
    )
