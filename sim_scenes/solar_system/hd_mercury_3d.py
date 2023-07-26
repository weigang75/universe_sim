# -*- coding:utf-8 -*-
# title           :高清水星3D效果
# description     :高清水星3D效果
# author          :Python超人
# date            :2023-02-11
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Mercury
from common.consts import SECONDS_PER_WEEK, SECONDS_PER_DAY
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    高清水星3D效果
    """
    bodies = [
        Mercury(texture="mercury_hd.jpg",
                init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                size_scale=1, show_name=False)
    ]
    mercury = bodies[0]

    # 3D摄像机初始化
    from simulators.ursina.entities.camera3d import Camera3d

    Camera3d.init()

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_DAY,
               position=(2.0 * mercury.radius, 0, -14000),
               cosmic_bg="",
               show_grid=False,
               show_camera_info=False,
               show_control_info=False,
               view_closely=0.001)
