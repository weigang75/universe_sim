# -*- coding:utf-8 -*-
# title           :在太阳系中以光速运行（裸眼3D）
# description     :在太阳系中以光速运行（裸眼3D）
# author          :Python超人
# date            :2023-07-02
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from common.consts import AU
from sim_scenes.func import ursina_run, create_solar_system_bodies, create_light_ship
from common.consts import LIGHT_SPEED
from sim_scenes.science.speed_of_light_init import SpeedOfLightInit

# TODO: 三种不同的摄像机视角
from simulators.ursina.entities.body_timer import TimeData
from simulators.ursina.entities.entity_utils import get_value_direction_vectors
from simulators.ursina.ursina_event import UrsinaEvent

camera_follow_light = None  # 摄像机固定，不会跟随光
camera_follow_light = 'ForwardView'  # 摄像机跟随光，方向是向前看

# 实例化一个初始化对象（订阅事件，记录到达每个行星所需要的时间）
init = SpeedOfLightInit(camera_follow_light)

# TODO: 注意：这里的算法是基于牛顿的万有引力（质量为0不受引力的影响在天体物理学中是不严谨）
# 创建太阳系天体（忽略质量，引力无效，初速度全部为0）
bodies = create_solar_system_bodies(ignore_mass=True, init_velocity=[0, 0, 0])

# camera_pos = "left"
camera_pos = "right"
camera_l2r = 0.01 * AU

if camera_pos == "right":  # 摄像机右眼
    init.light_init_position[0] += camera_l2r
elif camera_pos == "left":  # 摄像机左眼
    init.light_init_position[0] -= camera_l2r

init.light_init_position[0] = 4000000
init.light_init_position[1] = 1000000
# init.auto_control_speed = True

# 从 init 对象中获取 光体的大小（light_size_scale），光体的位置（light_init_position）
# 创建一个以光速前进的天体（模拟一个光子） speed=1光速=299792.458千米/秒，注意：质量为0才能达到光速，虽然如此，但也可以试试超光速
light_ship = create_light_ship(init.light_size_scale, init.light_init_position, speed=LIGHT_SPEED * 1)
# 增加光速天体到天体集合
bodies.append(light_ship)

# 运行前指定bodies、light_body并订阅事件
init.light_ship = light_ship
init.bodies = bodies
init.event_subscription()

UrsinaEvent.on_reset_unsubscription(init.on_reset)


def on_reset():
    init.on_reset
    init.arrived_info = "距离[太阳中心]：${distance}\n\n"
    init.arrived_info = "距离[太阳中心]：${distance}\n\n光速飞船速度：${speed}\n\n"


def on_timer_changed(time_data: TimeData):
    velocity, _ = get_value_direction_vectors(light_ship.velocity)
    distance = round(init.light_ship.position[2] / AU, 4)
    text = init.arrived_info.replace("${distance}", "%.4f AU" % distance)
    init.text_panel.text = text.replace("${speed}", str(round(velocity / LIGHT_SPEED, 1)) + "倍光速")


# 订阅重新开始事件
# 按键盘的 “O” 重置键会触发 on_reset
UrsinaEvent.on_reset_subscription(on_reset)
# 订阅计时器事件（记录已到达天体列表）
# 运行中，每时每刻都会触发 on_timer_changed
UrsinaEvent.on_timer_changed_subscription(on_timer_changed)


def body_arrived(body):
    # 到达每个行星都会触发，对光速飞船进行加速，超光速前进（使用未来曲率引擎技术）
    if body.name == "火星":  # 到达火星，加速前进，并进行攀升
        light_ship.acceleration = [0, 35, 300]
    elif body.name == "木星":  # 到达木星，加速前进，并进行下降
        light_ship.acceleration = [0, -100, 200]
    elif body.name == "土星":  # 到达土星，加速前进，并进行攀升
        light_ship.acceleration = [0, 55, 200]
    elif body.name == "天王星":  # 到达天王星，加速前进，并进行下降
        light_ship.acceleration = [0, -50, 200]
    elif body.name == "海王星":  # 到达海王星，加速前进，并进行攀升
        light_ship.acceleration = [-3, 48, 300]
    # print(body)

# def body_arrived(body):
#     # 到达每个行星都会触发，对光速飞船进行加速，超光速前进（使用未来曲率引擎技术）
#     if body.name == "火星":  # 到达火星，加速前进，并进行攀升
#         light_ship.acceleration = [0, 35000, 300000]
#     elif body.name == "木星":  # 到达木星，加速前进，并进行下降
#         light_ship.acceleration = [0, -100000, 200000]
#     elif body.name == "土星":  # 到达土星，加速前进，并进行攀升
#         light_ship.acceleration = [0, 55000, 200000]
#     elif body.name == "天王星":  # 到达天王星，加速前进，并进行下降
#         light_ship.acceleration = [0, -50000, 200000]
#     elif body.name == "海王星":  # 到达海王星，加速前进，并进行攀升
#         light_ship.acceleration = [-3, 48000, 300000]


init.body_arrived = body_arrived

# 使用 ursina 查看的运行效果
# 常用快捷键： P：运行和暂停  O：重新开始  I：显示天体轨迹
# position = 左-右+、上+下-、前+后-
ursina_run(bodies, 60,
           position=init.camera_position,
           show_trail=init.show_trail,
           show_timer=True,
           view_closely=init.view_closely,
           bg_music="sounds/interstellar.mp3")