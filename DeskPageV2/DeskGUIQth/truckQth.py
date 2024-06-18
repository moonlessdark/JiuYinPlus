# coding: utf-8
import threading
import time

from PySide6.QtCore import QThread, Signal, QWaitCondition, QMutex

from DeskPageV2.DeskFindPic.findCars import TeamFunc, FindTaskNPCFunc, ReceiveTruckTask, TransportTaskFunc, \
    FightMonster, UserGoods
from DeskPageV2.DeskTools.GhostSoft.get_driver_v3 import SetGhostBoards, SetGhostMouse
from DeskPageV2.DeskTools.WindowsSoft.MonitorDisplay import coordinate_change_from_windows
from DeskPageV2.DeskTools.WindowsSoft.get_windows import GetHandleList


is_car_in: bool = False  # 是否在车上
is_first_find_car: bool = True  # 是否是首次查找镖车
is_not_in_car_sum: int = 0  # 打怪后，是否连续多次状态还没有更新到上车
is_stop_find_car: bool = False  # 是否停止寻找镖车
is_need_walk: bool = True  # 是否需要走2步前往镖车
is_fight_npc_end: bool = False  # 是否已经和NPC战斗，如有没有战斗，就直接上车。 如果已经战斗，那么就需要查询点击镖车再上车
is_fight_npc_visible: bool = False  # 是否出现NPC
person_viewpoint: int = 0  # 0，默认，无， 1：平视， 2：俯视
map_name: str = ""


# 给全局变量加把锁
mutex = threading.Lock()


class TruckCarTaskQth(QThread):
    """
    本线程负责接镖和检测是否结束
    """
    sin_out = Signal(str)
    next_step = Signal(int)  # 下一步: 1 是扫描打怪。 2 是重新查找 镖车并开车
    sin_work_status = Signal(bool)
    sin_status_bar_out = Signal(str, int)  # 底部状态栏日志

    def __init__(self):
        super().__init__()

        self.truck_count = None
        self.TruckCarTaskQth_working = False
        self.cond = QWaitCondition()

        self.windows_opt = GetHandleList()

        self.is_close: bool = False

        self.mutex = QMutex()
        self.windows_handle = 0

        self.__team = TeamFunc()  # 创建队伍
        self.__find_npc = FindTaskNPCFunc()  # 查找当地的NPC
        self.__get_task = ReceiveTruckTask()  # 接任务
        self.__transport_task = TransportTaskFunc()  # 开始运镖
        self.__use_goods = UserGoods()

    def __del__(self):
        # 线程状态改为和线程终止
        # self.wait()
        self.TruckCarTaskQth_working = False

    def set_close(self):
        self.TruckCarTaskQth_working = False

    def get_param(self, windows_handle: int, truck_count: int):
        """
        线程用到的参数初始化一下
        :return:
        """
        self.windows_handle = windows_handle
        self.truck_count = truck_count
        self.TruckCarTaskQth_working = True

    def run(self):
        # 声明一下全局变量
        global person_viewpoint, is_stop_find_car, is_fight_npc_end, is_need_walk, is_fight_npc_visible, \
            is_first_find_car, is_not_in_car_sum, map_name, is_car_in

        # 修改全局变量，已经发现怪了，停止寻找车辆
        is_stop_find_car = False
        is_fight_npc_end = False
        is_need_walk = True  # 需要根据实际情况修改
        is_fight_npc_visible = False
        is_car_in = False

        self.mutex.lock()  # 先加锁
        self.sin_out.emit(f"线程:5秒后开始启动押镖...")
        self.sin_out.emit(f"本轮押镖次数为: {self.truck_count} 次")
        self.sin_status_bar_out.emit(f"已经押镖了 {0} 次", 0)
        time.sleep(5)
        for count_i in range(self.truck_count):

            self.sin_out.emit(f"开始执行第 {count_i + 1} 次押镖")
            # 0: 初始化  1: 完成组队  2: 已经找到接镖NPC,正在前往  3: 已经接取押镖任务  4: 已经驾驶镖车行驶  5: 已经打完怪 6: 已经再次上车
            __task_status: int = 0

            mutex.acquire()
            is_not_in_car_sum = 0
            mutex.release()

            self.__get_task.reply_person_perspective(self.windows_handle)  # 初始化视角

            while 1:

                if self.TruckCarTaskQth_working is False:
                    self.next_step.emit(0)
                    self.quit()
                    self.wait()  # 等待线程结束
                    self.mutex.unlock()  # 解锁
                    self.sin_work_status.emit(False)
                    self.sin_out.emit("线程:已停止押镖...")
                    return None

                if map_name == "":
                    __city_name: str = self.__team.get_map_and_person(self.windows_handle)
                    map_name = __city_name

                if map_name in ["苏州", "成都"]:
                    # 如果是成都和苏州，就不需要走了，直接上车就行了
                    is_need_walk = False
                # print(f"当前地图是: {map_name}, is_need_walk:{is_need_walk}")

                if __task_status == 0:

                    # 创建队伍
                    if self.__team.create_team(self.windows_handle) is False:
                        continue
                    # 检测是否使用了御风
                    self.sin_out.emit("步骤一:创建队伍...")

                    self.__use_goods.use_yu_feng_shen_shui(self.windows_handle)
                    __task_status = 1
                    self.sin_out.emit("步骤一:检测是否使用御风神水...")

                elif __task_status == 1:

                    # 队伍已经创建，开始寻找接镖NPC
                    if self.__find_npc.find_truck_task_npc(self.windows_handle) is False:
                        continue
                    __task_status = 2
                    self.sin_out.emit("步骤二:寻找押镖NPC,寻路中...")

                elif __task_status == 2:

                    # 正在跑路中，等待进入接取任务界面
                    if self.__get_task.receive_task(self.windows_handle) is False:
                        continue
                    __task_status = 3
                    self.next_step.emit(1)  # 等待劫镖NPC出现
                    self.sin_out.emit("步骤三:已接镖,等待劫镖NPC...")

                elif __task_status == 3:

                    # 已经接取了任务，寻找一下镖车,驾车上路
                    if is_fight_npc_visible is True:
                        # 出怪了，这里等一下啊,等打完怪再说
                        time.sleep(0.5)
                        print("出怪了，continue")
                        continue

                    if is_not_in_car_sum == 10:
                        # 如果连续10次没有成功上车，调整一下视角
                        self.__get_task.reply_person_perspective(self.windows_handle)
                    elif is_not_in_car_sum == 20:
                        # 20次没有上车成功，再调整一下视角
                        self.__get_task.reply_person_perspective_up(self.windows_handle)
                    elif is_not_in_car_sum == 30:
                        # 没救了，放弃了，退组重新接镖吧
                        if self.__team.close_team(self.windows_handle) is False:
                            continue
                        self.next_step.emit(0)  # 全部结束
                        self.sin_out.emit(f"尝试 {is_not_in_car_sum + 1} 次没有成功上车，队伍解散重组")
                        __task_status = 0

                    # 已经接取了任务，寻找一下镖车,驾车上路
                    if self.__transport_task.driver_truck_car(self.windows_handle, car_area_type=0, map_name=map_name) is False:
                        # 失败次数+1
                        mutex.acquire()
                        is_not_in_car_sum += 1
                        mutex.release()
                        continue
                    self.sin_out.emit("步骤四:驾驶镖车,运输中...")
                    __task_status = 4
                    self.__get_task.reply_person_perspective_up(self.windows_handle)

                    mutex.acquire()
                    is_not_in_car_sum = 0
                    mutex.release()

                elif __task_status == 4:
                    # 首次上车成功，开始等怪出现
                    if is_fight_npc_end is True:
                        __task_status = 5
                        self.sin_out.emit("步骤五:打怪结束...")

                elif __task_status == 5:
                    # 首次上车成功，开始等怪出现
                    if is_fight_npc_end is False:
                        time.sleep(0.5)
                        continue

                    if is_not_in_car_sum == 10:
                        # 如果连续10次没有成功上车，调整一下视角
                        self.__get_task.reply_person_perspective(self.windows_handle)
                    elif is_not_in_car_sum == 20:
                        # 20次没有上车成功，再调整一下视角
                        self.__get_task.reply_person_perspective_up(self.windows_handle)
                    elif is_not_in_car_sum == 30:
                        # 没救了，放弃了，退组重新接镖吧
                        if self.__team.close_team(self.windows_handle) is False:
                            continue
                        self.next_step.emit(0)  # 全部结束
                        self.sin_out.emit(f"尝试 {is_not_in_car_sum + 1} 次没有成功上车，队伍解散重组,5秒后重新接镖")
                        __task_status = 0
                        time.sleep(5)

                    # 打完怪了，开始继续找镖车
                    if self.__transport_task.driver_truck_car_v2(self.windows_handle, car_area_type=1) is False:

                        self.sin_out.emit(f"上车失败(次数:{is_not_in_car_sum + 1}),往前走1步")
                        SetGhostBoards().click_press_and_release_by_key_name_hold_time("w", 0.1)  # 往前走一步

                        # 失败次数+1
                        mutex.acquire()
                        is_not_in_car_sum += 1
                        mutex.release()
                        continue
                    __task_status = 6
                    self.sin_out.emit("步骤六:重新驾车,等待结束...")

                elif __task_status == 6:
                    # 打怪结束，上车成功，等待任务结束
                    if self.__transport_task.check_task_status(self.windows_handle) is True:
                        time.sleep(0.5)
                        continue
                    else:
                        if self.__transport_task.check_task_end(self.windows_handle):
                            self.sin_out.emit(f"本次押镖(第{count_i + 1}轮已经完成)")
                        else:
                            self.sin_out.emit("押镖未完成，超时或者镖车被毁")

                    mutex.acquire()
                    # 参数初始化我
                    is_first_find_car = True  # 是否是首次查找镖车
                    is_not_in_car_sum = 0  # 已经连续多少次没有找到镖车
                    is_stop_find_car = False  # 是否停止寻找镖车
                    is_need_walk = True  # 是否需要走2步前往镖车
                    is_fight_npc_end = False  # 是否已经和NPC战斗，如有没有战斗，就直接上车。 如果已经战斗，那么就需要查询点击镖车再上车
                    is_fight_npc_visible = False  # 是否出现NPC
                    person_viewpoint = 0  # 0，默认，无， 1：平视， 2：俯视
                    is_car_in = False
                    map_name = ""
                    mutex.release()
                    self.sin_status_bar_out.emit(f"已经押镖了 {count_i + 1} 次", count_i + 1)
                    break

            #
            #
            #
            #
            # person_viewpoint = 1
            #
            # pos = coordinate_change_from_windows(self.windows_handle, (100, 100))
            # SetGhostMouse().move_mouse_to(pos[0], pos[1])
            #
            # self.next_step.emit(2)  # 等待上车
            #
            # while 1:
            #
            #     if self.TruckCarTaskQth_working is False:
            #         self.quit()
            #         self.wait()  # 等待线程结束
            #         self.mutex.unlock()  # 解锁
            #         self.sin_work_status.emit(False)
            #         self.sin_out.emit("线程:已停止接取/检测任务")
            #         return None
            #
            #     if is_fight_npc_end is True and is_car_in is True:
            #         # 如果已经打了怪并且在车旁，那么就可以把处了主线程之外的其他线程都停止了
            #         self.next_step.emit(0)  # 全部结束
            #
            #     self.__get_task.break_other_truck_car(self.windows_handle)  # 不小心点到劫镖了，就退出一下
            #
            #     if is_not_in_car_sum > 10:
            #         self.next_step.emit(0)  # 全部结束
            #         self.sin_out.emit(f"尝试 {is_not_in_car_sum} 次没有成功上车，队伍解散重组")
            #         self.__team.close_team(self.windows_handle)
            #
            #     if self.__transport_task.check_task_status(self.windows_handle) is False:
            #
            #         if self.__get_task.break_npc_talk(self.windows_handle):  # 检测是否误触了NPC对话
            #             self.sin_out("不小心点到路人NPC对话了")
            #             time.sleep(2)
            #             break
            #
            #         if self.__transport_task.check_task_end(self.windows_handle):
            #             self.sin_out.emit(f"本次押镖(第{count_i + 1}轮已经完成)")
            #         else:
            #             self.sin_out.emit("押镖未完成，超时或者镖车被毁")
            #         self.next_step.emit(4)
            #         self.next_step.emit(6)
            #         mutex.acquire()
            #         # 参数初始化我
            #         is_first_find_car = True  # 是否是首次查找镖车
            #         is_not_in_car_sum = 0  # 已经连续多少次没有找到镖车
            #         is_stop_find_car = False  # 是否停止寻找镖车
            #         is_need_walk = True  # 是否需要走2步前往镖车
            #         is_fight_npc_end = False  # 是否已经和NPC战斗，如有没有战斗，就直接上车。 如果已经战斗，那么就需要查询点击镖车再上车
            #         is_fight_npc_visible = False  # 是否出现NPC
            #         person_viewpoint = 0  # 0，默认，无， 1：平视， 2：俯视
            #         is_car_in = False
            #         map_name = ""
            #         mutex.release()
            #         self.sin_status_bar_out.emit(f"已经押镖了 {count_i+1} 次", count_i+1)
            #         break

        self.mutex.unlock()  # 解锁
        self.sin_work_status.emit(False)
        self.next_step.emit(0)  # 全部结束
        return None


class TruckTaskFindCarQth(QThread):
    """
    以下原因出现时 查找镖车并上车
    1、接取任务后 开车 失败
    2、打了怪后，重新上车
    """
    sin_out = Signal(str)
    next_step = Signal(int)  # 下一步: 1 是扫描打怪。 2 是重新查找 镖车并开车
    sin_work_status = Signal(bool)

    def __init__(self):
        super().__init__()
        self.working = True
        self.mutex = QMutex()
        self.windows_handle = 0

        self.__transport_task = TransportTaskFunc()  # 开始运镖

    def __del__(self):
        # 线程状态改为和线程终止
        self.working = False

    def stop_execute_init(self):
        """
        线程暂停,所有参数重置为null
        :return:
        """
        self.working = False
        self.windows_handle = 0

    def get_param(self, windows_handle: int, working: bool):
        """
        线程用到的参数初始化一下
        :return:
        """
        self.working = working
        self.windows_handle = windows_handle

    def run(self):
        global person_viewpoint, is_need_walk, is_first_find_car, is_fight_npc_end, is_car_in, is_not_in_car_sum
        self.sin_out.emit("线程:开始尝试驾驶镖车")
        self.mutex.lock()  # 先加锁
        while 1:
            if self.working is False:
                # 结束了
                self.quit()
                self.wait()  # 等待线程结束
                self.mutex.unlock()  # 解锁
                self.sin_out.emit("线程:已停止尝试驾驶镖车")
                return None

            if is_first_find_car is True and is_need_walk is False:
                # 如果不需要走2步，那么就是苏州和成都了，直接上车就行。其他的都要走2步
                if self.__transport_task.transport_truck(self.windows_handle):
                    self.sin_out.emit("开始驾驶镖车")
                    # 如果出现了“驾车”的按钮，尝试点击 “驾车”
                    self.__transport_task.reply_person_perspective_up(self.windows_handle)  # 成功上车，拉远一下视角
                    person_viewpoint = 2
                    # 成功开车
                    self.working = False  # 好了，找镖车结束，等待打怪后再次来找镖车
                    self.next_step.emit(1)  # 等待出怪
                    mutex.acquire()
                    is_first_find_car = False
                    is_car_in = True  # 成功上车
                    is_not_in_car_sum = 0
                    mutex.release()
                    continue
                else:
                    mutex.acquire()
                    is_not_in_car_sum += 1
                    mutex.release()
            # 以下的逻辑可以适用于往前走2步并上车
            # 特别注意，在进行此操作时，R需要随时注意释放出怪了，一旦出怪了就需要停止
            elif is_first_find_car is True and is_need_walk is True:
                self.sin_out.emit("开始在屏幕中寻找并驾驶镖车...")
                __first_car_pos = self.__transport_task.find_truck_car_center_pos(self.windows_handle)
                if __first_car_pos is not None:
                    # 如果是已经转到了屏幕中间
                    # 如果发现镖车在 画面中间的位置附近，就往前走2秒，靠近镖车
                    time.sleep(1)
                    if map_name == "金陵":
                        SetGhostBoards().click_press_and_release_by_key_name_hold_time("w", 2.5)  # 金陵太远了
                        self.sin_out.emit("往前走一大步")
                    else:
                        SetGhostBoards().click_press_and_release_by_key_name_hold_time("w", 2)  # 往前走一步
                        self.sin_out.emit("往前走2步")
                else:
                    mutex.acquire()
                    is_not_in_car_sum += 1
                    mutex.release()
                    continue
                if is_stop_find_car or is_fight_npc_visible:
                    # 出怪了，停止查找
                    self.working = False
                    continue

                if self.__transport_task.transport_truck(self.windows_handle):
                    # 如果出现了“驾车”的按钮，尝试点击 “驾车”
                    self.__transport_task.reply_person_perspective_up(self.windows_handle)  # 成功上车，拉远一下视角
                    self.sin_out.emit("开始驾驶镖车")
                    person_viewpoint = 2
                    # 成功开车
                    self.next_step.emit(1)  # 等待出怪

                    self.working = False
                    mutex.acquire()
                    is_first_find_car = False
                    is_car_in = True  # 成功上车
                    is_not_in_car_sum = 0  # 成功上车，将计数归0
                    mutex.release()
                    if is_fight_npc_end:
                        self.next_step.emit(5)
                    continue
                else:
                    mutex.acquire()
                    is_not_in_car_sum += 1
                    mutex.release()

            else:
                # 如果是打完怪后
                __car_center_pos = self.__transport_task.find_car_in_center_display_v3(hwnd=self.windows_handle, display_area=1)
                if __car_center_pos is None:
                    continue
                self.next_step.emit(5)
                time.sleep(1)
                SetGhostMouse().move_mouse_to(__car_center_pos[0], __car_center_pos[1])  # 鼠标移动到初始化位置
                time.sleep(0.5)

                __find_car_sum: int = 0

                while 1:

                    if is_stop_find_car or is_fight_npc_visible:
                        # 成功开车
                        self.working = False
                        break

                    if __find_car_sum == 5:
                        self.sin_out.emit("往前走1步")
                        SetGhostBoards().click_press_and_release_by_key_name_hold_time("w", 0.5)  # 往前走一步
                        __find_car_sum = 0
                        self.next_step.emit(3)
                        break

                    pos = SetGhostMouse().get_mouse_x_y()

                    #  先下移50个像素点击一次
                    SetGhostMouse().move_mouse_to(pos[0], pos[1] + 50)
                    time.sleep(0.2)
                    SetGhostMouse().click_mouse_left_button()
                    time.sleep(1)

                    __find_car_sum += 1

                    __transport_pos = self.__transport_task.find_driver_truck_type(self.windows_handle)
                    if __transport_pos is not None:

                        if is_stop_find_car or is_fight_npc_visible:
                            # 成功开车
                            self.working = False
                            break

                        SetGhostBoards().click_press_and_release_by_code(27)
                        time.sleep(1)
                        SetGhostMouse().click_mouse_right_button()  # 右键主动靠近
                        time.sleep(2)  # 等待2秒，让人物主动靠近
                        if self.__transport_task.transport_truck(self.windows_handle):
                            # 如果 运镖 方式 界面出现，并且还成功运行了.
                            # 那么本次任务就可以结束了
                            self.sin_out.emit("开始驾驶镖车")
                            person_viewpoint = 2
                            self.working = False
                            mutex.acquire()
                            is_car_in = True  # 成功上车
                            is_not_in_car_sum = 0  # 成功上车，将计数归0
                            mutex.release()
                            break
                        else:
                            SetGhostMouse().release_all_mouse_button()
                            # 如果点了 运镖 但是 没有开车，那么就表示距离太远了，需要靠近
                            self.sin_out.emit("往前走1步")
                            SetGhostBoards().click_press_and_release_by_key_name_hold_time("w", 0.5)  # 往前走一步
                            # 退出循环，从头再来一次
                            self.next_step.emit(3)
                            mutex.acquire()
                            is_not_in_car_sum += 1
                            mutex.release()
                            break


class TruckTaskFightMonsterQth(QThread):
    """
    检测并打怪。
    打怪之前先尝试点击一下镖车(屏幕中心点)，打完怪后就可以直接上车
    """
    sin_out = Signal(str)
    next_step = Signal(int)  # 下一步: 1 是扫描打怪。 2 是重新查找 镖车并开车, 3: 打怪中，暂时查找车辆， 4：打怪结束，重新查找车辆

    def __init__(self):
        super().__init__()

        self.working = True
        self.cond = QWaitCondition()

        self.mutex = QMutex()
        self.windows_handle = 0

        self.__fight_monster = FightMonster()

    def __del__(self):
        # 线程状态改为和线程终止
        self.working = False

    def get_param(self, windows_handle: int, working_status: bool = True):
        """
        线程用到的参数初始化一下
        :return:
        """
        self.working = working_status
        self.windows_handle = windows_handle

    def run(self):
        self.sin_out.emit("线程:开始查找/检测劫匪NPC")
        self.mutex.lock()  # 先加锁
        while 1:
            if self.working is False:
                # 结束了
                self.quit()
                self.wait()  # 等待线程结束
                self.mutex.unlock()  # 解锁
                self.sin_out.emit("线程:已经停止查找/检测劫匪NPC")
                return None
            if self.__fight_monster.check_fight_status(self.windows_handle):
                # 声明一下全局变量
                global is_stop_find_car, is_fight_npc_end, is_fight_npc_visible, is_car_in
                # 修改全局变量，已经发现怪了，停止寻找车辆
                mutex.acquire()
                is_stop_find_car = True
                is_fight_npc_end = False
                is_fight_npc_visible = True
                is_car_in = False  # 出怪了，需要下车
                mutex.release()
                self.sin_out.emit("劫镖NPC出现...")

                self.next_step.emit(4)  # 打怪中，暂时查找车辆
                self.next_step.emit(5)  # 打怪中，暂时查找车辆

                # 开始战斗
                if self.__fight_monster.fight_monster(self.windows_handle) is True:
                    self.working = False

                    self.sin_out.emit("劫镖NPC已消失(击杀)...")
                    # 修改一下全局变量，已经和NPC战斗过了
                    mutex.acquire()
                    is_stop_find_car = False
                    is_fight_npc_end = True
                    is_fight_npc_visible = False
                    mutex.release()
                    # 修改全局变量，战斗结束，继续寻找车辆
                    # self.next_step.emit(2)  # 打怪结束，继续上车跑路
                    # self.next_step.emit(3)  # 打怪结束，继续保持车辆在屏幕上


class FollowTheTrailOfTruckQth(QThread):
    """
    保持镖车在屏幕中间的附近
    """

    sin_out = Signal(str)
    next_step = Signal(int)  # 下一步: 1 是扫描打怪。 2 是重新查找 镖车并开车, 3: 打怪中，暂时查找车辆， 4：打怪结束，重新查找车辆

    def __init__(self):
        super().__init__()

        self.is_wait = False
        self.working = True
        self.cond = QWaitCondition()

        self.mutex = QMutex()
        self.windows_handle = 0

        self.__team = TeamFunc()  # 创建队伍
        self.__transport_task = TransportTaskFunc()  # 查找镖车

    def __del__(self):
        # 线程状态改为和线程终止
        self.working = False

    def stop_flag(self):
        """
        线程暂停,所有参数重置为null
        :return:
        """
        self.working = False

    def get_param(self, windows_handle: int, working_status: bool):
        """
        线程用到的参数初始化一下
        :return:
        """
        self.working = working_status
        self.windows_handle = windows_handle

    def run(self):

        self.sin_out.emit("线程:开始保持镖车在画面中")
        self.mutex.lock()  # 先加锁
        global is_not_in_car_sum

        while 1:
            if self.working is False:
                # 结束了
                self.quit()
                self.wait()  # 等待线程结束
                self.mutex.unlock()  # 解锁
                self.sin_out.emit("线程:已停止保持镖车在画面中")
                return None

            if is_stop_find_car or is_fight_npc_visible:
                continue

            __car_pos = self.__transport_task.find_truck_car_in_display(hwnd=self.windows_handle)
            if __car_pos is True:
                if person_viewpoint == 1:
                    __car_center_pos = self.__transport_task.find_car_in_center_display_v3(hwnd=self.windows_handle, display_area=0)
                else:
                    __car_center_pos = self.__transport_task.find_car_in_center_display_v3(hwnd=self.windows_handle, display_area=1)
                if __car_center_pos is not None:
                    # 存储一下镖车在屏幕哪个位置
                    continue

            follow_car_quadrant = self.__transport_task.find_car_pos_in_display_quadrant(self.windows_handle)

            if self.working is False:
                # 结束了
                # 这里判断一下是因为打完怪后再押镖，就不一定需要一定在画面中间了
                self.quit()
                self.wait()  # 等待线程结束
                self.mutex.unlock()  # 解锁
                self.sin_out.emit("线程:已停止保持镖车在画面中")
                return None

            if is_not_in_car_sum == 5:
                self.sin_out.emit("旋转了5次依旧没有找到镖车,将人物视角平视继续尝试")
                self.__transport_task.reply_person_perspective(self.windows_handle)
            if follow_car_quadrant == 0:
                # 如果镖车本身就就没有出现在屏幕上，那么就转一下大的
                SetGhostBoards().click_press_and_release_by_key_code_hold_time(37, 0.4)
                continue
            elif follow_car_quadrant == 1:
                # 如果镖车在画面中消失前，是在第1象限，那么就往这个方向走一下
                SetGhostBoards().click_press_and_release_by_key_code_hold_time(37, 0.2)
            elif follow_car_quadrant == 2:
                # 第二象限，右上角
                SetGhostBoards().click_press_and_release_by_key_code_hold_time(39, 0.2)
            elif follow_car_quadrant == 3:
                # 第三象限，左下角
                SetGhostBoards().click_press_and_release_by_key_code_hold_time(37, 0.4)
            elif follow_car_quadrant == 4:
                # 第四象限，右下角
                SetGhostBoards().click_press_and_release_by_key_code_hold_time(39, 0.4)
            is_not_in_car_sum += 1
