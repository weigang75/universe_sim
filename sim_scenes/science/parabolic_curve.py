# -*- coding:utf-8 -*-
# title           :抛物线模拟
# description     :抛物线模拟
# author          :Python超人
# date            :2023-04-09
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Moon, Earth, Body
from objs import Football
from common.consts import SECONDS_PER_HOUR, SECONDS_PER_MINUTE
from sim_scenes.func import ursina_run, get_vector2d_velocity, camera_look_at, two_bodies_colliding
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ursina_event import UrsinaEvent


def create_ejected_object(velocity, radius, trail_color, gravity_only_for, angle=10):
    """
    创建一个抛出物体
    @param velocity: 抛出去的速度
    @param radius: 地球中心的半径
    @param trail_color: 轨迹颜色
    @param gravity_only_for: 指定一个天体，被抛的物体的引力只对该天体有效
    @param angle: 抛出去的角度（地平线夹角，默认为10）
    @return:
    """
    # 根据速度、角度获取矢量速度（vx、vy） -> vx² + vy² = velocity²
    vx, vy = get_vector2d_velocity(velocity, angle=angle)
    football = Football(name=f'物体速度:{velocity}', mass=500, size_scale=1e3,
                        trail_color=trail_color, init_position=[0, radius + 500, 0],
                        init_velocity=[vx, vy, 0], gravity_only_for=[gravity_only_for])
    return football


if __name__ == '__main__':
    """
    抛物线模拟
    """
    # 地球在中心位置
    earth = Earth(init_position=[0, 0, 0], init_velocity=[0, 0, 0],
                  size_scale=1, rotation_speed=0, texture="earth_hd.jpg")
    radius = earth.radius
    # 创建4个不同的抛出速度的物体，速度分别为：7.5km/s、8.5km/s、10km/s、11.2km/s（第二宇宙速度）
    # velocity = 7.5，飞不出地球太远，就落地（仅适用于地球的重力，物体之间重力不要受到影响）
    obj0 = create_ejected_object(velocity=7.5, radius=radius, trail_color=(255, 0, 255),  # 粉色
                                 gravity_only_for=earth)  # 被抛物只对该地球引力有效
    # velocity = 8.5，飞不出地球太远，就落地
    obj1 = create_ejected_object(velocity=8.5, radius=radius, trail_color=(255, 0, 0),  # 红色
                                 gravity_only_for=earth)  # 被抛物只对该地球引力有效
    # velocity = 10，能飞出地球很远，但还是无法摆脱地球引力
    obj2 = create_ejected_object(velocity=10, radius=radius, trail_color=(0, 255, 0),  # 绿色
                                 gravity_only_for=earth)  # 被抛物只对该地球引力有效
    # velocity = 11.2，脱离地球引力直接飞出。速度11.2千米/秒为脱离地球引力的速度叫第二宇宙速度
    obj3 = create_ejected_object(velocity=11.2, radius=radius, trail_color=(0, 0, 255),  # 蓝色
                                 gravity_only_for=earth)  # 被抛物只对该地球引力有效

    bodies = [earth, obj0, obj1, obj2, obj3]


    def on_reset():
        """
        当按键盘的 “O” 键重置后，恢复所有抛出物的状态（引力有效），这样就可以反复观看
        @return:
        """
        for obj in [obj0, obj1, obj2, obj3]:
            obj.ignore_mass = False


    def on_timer_changed(time_data: TimeData):
        """
        在运行中，每时每刻都会触发，对抛出物与地球的碰撞进行判断，如果碰到地球，则停止运动
        @param time_data:
        @return:
        """
        for obj in [obj0, obj1, obj2, obj3]:
            # 循环判断每个抛出物与地球是否相碰撞
            if two_bodies_colliding(obj, earth):
                # 如果抛出物与地球相碰撞了，则静止不动（抛出物停止并忽略引力）
                obj.stop_and_ignore_gravity()


    # 订阅事件后，上面2个函数功能才会起作用
    # 按键盘的 “O” 重置键会触发 on_reset
    UrsinaEvent.on_reset_subscription(on_reset)
    # 运行中，每时每刻都会触发 on_timer_changed
    UrsinaEvent.on_timer_changed_subscription(on_timer_changed)

    # 使用 ursina 查看的运行效果
    # 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
    # position = 左-右+、上+下-、前+后-
    ursina_run(bodies, SECONDS_PER_HOUR / 2,  # 一秒相当于半个小时
               position=(0, 0, -45000),
               show_trail=True,
               show_timer=True,
               view_closely=0.001)
