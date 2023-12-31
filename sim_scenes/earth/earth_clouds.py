# -*- coding:utf-8 -*-
# title           :带有云层地球模拟
# description     :带有云层地球模拟
# author          :Python超人
# date            :2023-05-01
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Earth
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_DAY
from sim_scenes.func import ursina_run

if __name__ == '__main__':
    """
    带有云层地球模拟
    """
    earth = Earth(texture="earth_hd.jpg",
                  init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                  size_scale=1).set_ignore_gravity()  # 忽略引力

    # 创建带有云层的地球
    earth_with_clouds = Earth(texture="earth_hd.jpg",
                              init_position=[1.5 * earth.diameter, 0, 0],
                              init_velocity=[0, 0, 0],
                              size_scale=1)
    # 创建云层（texture纹理图使用了透明云层的图片，云层的 size_scale 要稍微比地球大一点）
    clouds = Earth(name="地球云层", texture="transparent_clouds.png",
                   size_scale=1.001, parent=earth_with_clouds)

    bodies = [earth, earth_with_clouds, clouds]

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,
               position=(1.5 * earth.radius, 0, -30000),
               show_grid=False,
               view_closely=0.001)   # 近距离观看 view_closely=True或0.001
