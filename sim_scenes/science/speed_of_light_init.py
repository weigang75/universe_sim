# -*- coding:utf-8 -*-
# title           :在太阳系中以光速运行
# description     :在太阳系中以光速运行
# author          :Python超人
# date            :2023-04-05
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from bodies import Sun, Asteroids, Body
from common.consts import AU, LIGHT_SPEED, SECONDS_PER_MINUTE, SECONDS_PER_HOUR
from sim_scenes.func import create_text_panel, smooth_speed_transition, check_calc_run_speed_maps
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.ui.control_ui import ControlUI
from simulators.ursina.ursina_config import UrsinaConfig
from simulators.ursina.ursina_event import UrsinaEvent
from ursina import camera
import datetime


class SpeedOfLightInit:
    def __init__(self, camera_follow_light):
        """
        @param camera_follow_light: 三种不同的摄像机视角
                None         # 摄像机固定，不会跟随光
                ForwardView  # 摄像机跟随光，方向是向前看
                SideView     # 摄像机跟随光，方向是侧面看
        """
        # 存放记录光体已到达天体列表
        self.arrived_bodies = []
        # 显示消息面板（记录光体已到达天体的时间）
        self.text_panel = None
        # 显示消息面板的信息（记录光体已到达天体的时间）
        self.arrived_info = ""

        self.__camera_follow_light = camera_follow_light
        self.__light_ship = None
        self.__bodies = None
        self.view_closely = False
        self.auto_control_speed = False
        self.body_arrived = None

        if self.__camera_follow_light in ["SideView"]:
            # 摄像机位置 = 前-后+、上+下-、左-右+、
            self.camera_position = (AU / 5, 0, 0)
            self.show_trail = True
            self.light_size_scale = 2e6
            self.light_init_position = [AU, AU / 20, 0]
            # self.auto_control_speed = True
        elif self.__camera_follow_light in ["SideViewActualSize"]:
            # 摄像机位置 = 前-后+、上+下-、左-右+、
            # self.camera_position = (0, AU, 0)
            self.show_trail = True
            self.light_size_scale = 2e6
            self.light_init_position = [AU, 0, 0]
            self.auto_control_speed = True
        elif self.__camera_follow_light == "ForwardView":
            # 摄像机位置 = 左-右+、前+后-、上-下+
            # self.camera_position = (0, AU / 10, -AU)
            self.camera_position = (0, -AU / 25, -AU / 50)
            self.show_trail = True
            self.light_size_scale = 2e6
            self.light_init_position = [AU / 8, AU / 10, 0]
            # self.auto_control_speed = True
        else:
            # 摄像机位置 = 左-右+、上+下-、前+后-
            self.camera_position = (0, AU, -6 * AU)
            self.show_trail = True
            self.light_size_scale = 1e7
            self.light_init_position = [AU / 3, 0, 0]
            self.auto_control_speed = True

    @property
    def light_ship(self):
        return self.__light_ship

    @light_ship.setter
    def light_ship(self, value):
        self.__light_ship = value

    @property
    def bodies(self):
        return self.__bodies

    @bodies.setter
    def bodies(self, value):
        self.__bodies = value
        if self.__camera_follow_light == "SideViewActualSize":
            # TODO: 将天体的大小不进行缩放
            for body in self.__bodies:
                if body is self.light_ship:
                    continue
                body.size_scale = 1
            self.camera_position = [-self.light_init_position[0] / 1.005, 0, 0]
            self.view_closely = True

    def on_reset(self):
        """
        当按键盘的 “O” 键重置后会触发
        @return:
        """
        if hasattr(self, "run_speed_maps"):
            delattr(self, "run_speed_maps")

        self.arrived_bodies.clear()  # 重置存放记录光体已到达天体列表
        self.arrived_info = "距离[太阳中心]：${distance}\n\n"
        if self.text_panel is not None:
            self.text_panel.text = self.arrived_info.replace("${distance}", "0 AU")

    def event_subscription(self):
        """
        订阅事件
        @return:
        """
        if self.light_ship is None:
            raise Exception("请指定 SpeedOfLightInit.light_body")

        if self.bodies is None:
            raise Exception("请指定 SpeedOfLightInit.bodies")

        # 订阅重新开始事件
        # 按键盘的 “O” 重置键会触发 on_reset
        UrsinaEvent.on_reset_subscription(self.on_reset)
        # 运行前会触发 on_ready
        UrsinaEvent.on_ready_subscription(self.on_ready)
        # 订阅计时器事件（记录已到达天体列表）
        # 运行中，每时每刻都会触发 on_timer_changed
        UrsinaEvent.on_timer_changed_subscription(self.on_timer_changed)

    def light_body_input(self, key):
        # TODO: 在这里控制光体的运动
        # if self.light_body.planet.hovered:
        if key == "w":
            # 上
            pass
        elif key == "s":
            # 上
            pass
        elif key == "a":
            # 左
            pass
        elif key == "d":
            # 右
            pass
            # self.light_body.velocity[1] = 1
            # self.light_body.planet.update()

    def on_ready(self):
        """
        模拟器开始运行前触发
        @return:
        """
        # self.__light_body.planet_scale = self.__light_body.planet.scale
        self.text_panel = create_text_panel()
        # self.text_panel.parent.enabled = False
        self.text_panel.text = self.arrived_info.replace("${distance}", "0 AU")

        self.light_ship.planet.rotation_x = 90

        if self.__camera_follow_light in ["SideView"]:
            camera.rotation_z = -90
            camera.rotation_y = -85
        elif self.__camera_follow_light in ["ForwardView"]:
            camera.rotation_x = -72
        elif self.__camera_follow_light in ["SideViewActualSize"]:
            self.light_ship.planet.rotation_x = 0
            # camera.rotation_z = -90
            camera.rotation_y = -85

        if self.__camera_follow_light in ["SideView", "SideViewActualSize"]:
            camera.parent = self.light_ship.planet

        elif self.__camera_follow_light == "ForwardView":
            # self.light_body.planet.enabled = False
            camera.parent = self.light_ship.planet
            self.light_ship.planet.input = self.light_body_input
            # camera.rotation_y = -15
            if hasattr(camera, "sky"):
                # 摄像机跟随地球后，需要对深空背景进行调整，否则看到的是黑色背景
                camera.sky.scale = 800
                camera.clip_plane_near = 0.1
                camera.clip_plane_far = 1000000

        # 取消订阅（防止 光体 的大小进行变化影响摄像机的视角）
        UrsinaEvent.on_body_size_changed_unsubscription(self.light_ship.planet.change_body_scale)

    # def on_body_size(self):
    #     self.light_body.planet.scale = self.light_body.planet_scale

    def auto_run_speed(self):
        """
        自动调整速度（对于空旷的位置，摄像机会进行加速）
        @return:
        """
        if not self.auto_control_speed:
            return
        # if self.__camera_follow_light != "SideViewActualSize":
        #     return

        if not hasattr(self, "run_speed_maps"):
            # 运行速度配置
            run_speed_maps = [
                {"au": 0., "secs": 1},
                {"au": 0.008, "secs": 1},
                {"au": "?", "secs": SECONDS_PER_MINUTE * 5},
                {"au": 0.386, "secs": 1},
                {"au": 0.3865, "secs": 1},  # [00:03:12] 到达 [水星] 0.384 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 5},
                {"au": 0.721, "secs": 1},
                {"au": 0.724, "secs": 1},  # [00:06:00] 到达 [金星] 0.721 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 5},
                {"au": 1.0, "secs": 1},
                {"au": 1.006, "secs": 1},  # [00:08:19] 到达 [地球、月球] 1.0 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 5},
                {"au": 1.52, "secs": 1},
                {"au": 1.522, "secs": 1},  # [00:12:39] 到达 [火星] 1.52 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 25},
                {"au": 5.19, "secs": 1},
                {"au": 5.20, "secs": 1},  # [00:43:10] 到达 [木星] 5.19 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 25},
                {"au": 9.5, "secs": 1},
                {"au": 9.51, "secs": 1},  # [01:19:01] 到达 [土星] 9.5 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 30},
                {"au": 19.2, "secs": 1},
                {"au": 19.21, "secs": 1},  # [02:39:41] 到达 [天王星] 19.2 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 30},
                {"au": 30.7, "secs": 1},
                {"au": 30.71, "secs": 1},  # [04:15:19] 到达 [海王星] 30.7 AU
                {"au": "?", "secs": SECONDS_PER_MINUTE * 30},
                {"au": 39.55, "secs": 1},
                {"au": 40, "secs": 1}  # [05:28:55] 到达 [冥王星] 39.55 AU
            ]
            run_speed_maps = check_calc_run_speed_maps(run_speed_maps)
            run_speed_maps = smooth_speed_transition(run_speed_maps)
            self.run_speed_maps = run_speed_maps

        light_distance = self.light_ship.position[2]
        current_idx = 0
        for i, m in enumerate(self.run_speed_maps):
            if i == 0:
                au_min = 0
            else:
                au_min = self.run_speed_maps[i - 1]["au"]

            au_max = m["au"]

            if light_distance < au_min * AU:
                # 如果光体的距离小于 au_min 则无需再循环
                break

            if au_max * AU > light_distance >= au_min * AU:
                if UrsinaConfig.seconds_per != m["secs"]:
                    seconds_per = m["secs"]  # int(round(m["secs"], 0))
                    UrsinaConfig.seconds_per = seconds_per
                    if seconds_per >= 10000:
                        msg = f"加速到 {int(seconds_per / 10000)} 万"
                    elif seconds_per >= 1000:
                        msg = f"加速到 {int(seconds_per / 1000)} 千"
                    elif seconds_per > 1:
                        msg = f"加速到 {int(seconds_per)} "
                    else:
                        msg = f"当前为 {int(seconds_per)} "

                    msg = f"{msg}倍光速"

                    ControlUI.current_ui.show_message(msg, close_time=-1)
                    current_idx = i
                    break

        if current_idx > 0:
            self.run_speed_maps = self.run_speed_maps[current_idx:]

    def on_timer_changed(self, time_data: TimeData):
        """
        计时器触发
        @param time_data: 计时器时间数据
        @return:
        """
        self.auto_run_speed()

        for body in self.bodies:
            if body is self.light_ship or isinstance(body, Sun) \
                    or body in self.arrived_bodies or isinstance(body, Asteroids):
                # 对于光速天体、太阳、小行星群、“已到达天体列表”中的天体无需计算
                continue
            # 计算判断，如果光速天体距离到达了某个天体，就记录到“已到达天体列表”中
            if self.light_ship.position[2] >= body.position[2] * body.distance_scale:
                if callable(self.body_arrived):
                    self.body_arrived(body)
                    self.arrived_bodies.append(body)
                if self.text_panel is not None:
                    self.arrived_info += f"[{time_data.time_text}]\t到达\t[{body.name}]\n\n"
                    # distance = round(self.light_body.position[2] / AU, 4)
                    # # print("浮点数保留两位小数，宽5位，不足补0：%05.5f " % 2.222)
                    # self.text_panel.text = self.arrived_info.replace("${distance}", "%.4f AU" % distance)
                    print(f"[{time_data.time_text}] 到达 [{body.name}] {round(self.light_ship.position[2] / AU, 4)} AU")
                    return

        if not hasattr(self, "last_time"):
            self.last_time = datetime.datetime.now()
        else:
            if datetime.datetime.now() - datetime.timedelta(milliseconds=1000) > self.last_time:
                # distance = round(self.light_body.position[2] / AU, 4)
                # self.text_panel.text = self.arrived_info.replace("${distance}", "%.4f AU" % distance)
                self.last_time = datetime.datetime.now()

        distance = round(self.light_ship.position[2] / AU, 4)
        self.text_panel.text = self.arrived_info.replace("${distance}", "%.4f AU" % distance)
