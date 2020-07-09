import time, datetime
import pendulum
from datetime import timedelta
import abc
import random
from pyprobar.styleString import setRGB, rgb_str, OFF, rgb_dict
from pyprobar.cursor import Cursor
import numpy as np
from threading import Thread
import threading
import inspect
import ctypes
from functools import wraps, partial

__all__ = ["_Thread_probar", "_Thread_bar", "stop_thread","trydecorator", "trydecorator2", 'trydecorator3']


cursor = Cursor()

class Progress(metaclass=abc.ABCMeta):

    unit_percent = 0.034
    total_space = 30
    COLOR_bar = None
    _COLOR = 0

    def currentProgress(self, percent, t0, terminal, time_zone):
        cost_time = time.time() - t0
        total_time = cost_time / percent
        PERCENT = percent * 100

        remain_time = int(total_time - cost_time)
        remain_time = timedelta(seconds=remain_time)
        total_time = timedelta(seconds=int(total_time))
        cost_time = timedelta(seconds=int(cost_time))

        _PERCENT = f"{PERCENT: >6.2f}%"
        _COST = f" {cost_time}|{total_time} "
        _REMAIN = f" {remain_time}|{total_time} "
        _ETC = f" ETC: {(pendulum.now(time_zone) + remain_time).strftime('%m-%d %H:%M:%S')}"
        # _ETC = f" ETC: {(datetime.datetime.now() + remain_time).strftime('%m-%d %H:%M:%S')}"
        return _PERCENT, _REMAIN, _ETC

    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""

        n_sign1, mod_sign1 = divmod(percent, self.unit_percent)
        N1 = int(n_sign1)
        sign1 = symbol_1 * N1
        N0 = int((mod_sign1 / self.unit_percent) * (self.total_space - N1))

        sign0 = symbol_2 * N0
        SIGN = '|' + sign1 + sign0 + (self.total_space - N1 - N0 - 1) * ' ' + '|'
        return SIGN, N1

    @abc.abstractmethod
    def appearance(self, *args, **kwargs):
        pass

    @staticmethod
    def get_color(N_color, update=True):
        """Choice random n colors
        """
        if update == True or Progress._COLOR == 0:
            # specify the first color
            rgb_list = [setRGB(rgb_dict["浅绿"])]
            for i in range(N_color - 2):
                rgb = rgb_dict[(random.choice(list(rgb_dict)))]
                rgb_list.append(setRGB(rgb))

            # specify the last color
            rgb_list.append(setRGB(rgb_dict["紫色"]))
            Progress._COLOR = rgb_list

            return Progress._COLOR
        else:
            return Progress._COLOR

    def get_bar_color(self, N1, color, N_colors=4, flag_update_color=[None], first_flag=True):

        if self.COLOR_bar == None:
            COLOR_bar = [''] * N_colors

        if color == 'const_random':
            return self.get_color(N_color=N_colors, update=False)
        elif color == "1":
            return [setRGB(i) for i in [rgb_dict.灰色, [255, 204, 245],[66,227,35],[117, 181, 244]]]
        elif color == "2":
            return [setRGB(i) for i in [[146,52,247],[250,205,229],[66,227,35],[214,126,209]]]
        elif color == "3":
            return [setRGB(i) for i in [[204,204,204], [28, 199, 212],[66,227,35],rgb_dict.玫瑰红]]
        elif color == '4':
            return [setRGB(i) for i in [[204, 204, 204], rgb_dict.蓝1, [255, 204, 245], rgb_dict.蓝2]]
        elif color == '5':
            return [setRGB(i) for i in [[204, 204, 204], rgb_dict.绿1, rgb_dict.绿2, rgb_dict.绿3]]
        elif color == '0':
            return self.COLOR_bar
        elif type(color).__name__ == "list" or type(color).__name__ == "tuple":
            color = np.array(color)
            rows, cols = color.reshape(-1, 3).shape
            # If specify only one color, that color is given to bar
            if rows == 1:
                self.COLOR_bar[1] = setRGB(color)
                return self.COLOR_bar
            else:
                 return [setRGB(i) for i in color]
        elif color == "update_random":
            if flag_update_color[0] != N1:
                flag_update_color[0] = N1
                self.COLOR_bar = self.get_color(N_color=N_colors, update=True)
                return self.COLOR_bar
            else:
                # print(COLOR)
                return self.COLOR_bar
        else:
            raise ValueError("Invalid input!")

class IntegProgress(Progress):

    def appearance(self, idx, total_steps, symbol_1, symbol_2, t0, color, N_colors,terminal, first_flag,time_zone):
        counts = idx + 1
        percent = counts / total_steps
        if idx == 0:
            print(f"\r{0:.2f}% \t  {0:.1f}|{float('inf'):.1f}s{cursor.EraseLine(0)}", end='', flush=True)
        else:

            SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
            _PERCENT, _REMAIN , _ETC = self.currentProgress(percent, t0, terminal, time_zone)
            color_percent, color_bar, color_etc, color_etc2 = self.get_bar_color(N1, color, N_colors, first_flag=first_flag)
            # color_percent,color_bar, color_etc, color_etc2 = setRGB(rgb_dict["灰色"]),setRGB(rgb_dict["粉色"]),
            # setRGB(rgb_dict["浅绿"]), setRGB(rgb_dict["天蓝"])
            print('\r' + color_percent + f"{_PERCENT}" + color_bar + SIGN + \
                  color_etc  + _REMAIN + color_etc2 + _ETC + OFF + cursor.EraseLine(0), end='',
                  flush=True)


class _Thread_probar(Thread, IntegProgress):
    def __init__(self, deq, N, time_interval, symbol_1, symbol_2,
                            t0, color, N_colors, terminal, time_zone):
        super().__init__()
        self.deq = deq
        self.stop = False
        self.N = N
        self.time_interval = time_interval
        self.symbol_1=symbol_1
        self.symbol_2=symbol_2
        self.t0=t0
        self.color=color
        self.N_colors=N_colors
        self.terminal=terminal
        self.first_flag = True
        self.time_zone=time_zone
        self.lock = threading.Lock()



    def run(self):

        while not self.stop:

            # idx = self.queue.get()
            idx = self.deq[0]
            self.appearance(idx, self.N, self.symbol_1, self.symbol_2,
                            self.t0, self.color, self.N_colors, self.terminal, first_flag=self.first_flag, time_zone=self.time_zone)

            time.sleep(self.time_interval)
            if idx == self.N-1:
                self.stop = True


class SepaProgress(Progress):
    def appearance(self, idx, total_size,
                   color,
                   symbol_1, symbol_2,
                   text,
                   terminal,
                   t0,
                   time_zone):

        percent = idx / total_size
        SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
        PERCENT, ETC_1, ETC_2 = self.currentProgress(percent, t0, terminal, time_zone)
        color_percent, color_bar, color_etc, color_etc2 = self.get_bar_color(N1, color, N_colors=4)
        if text != '': text += "|"
        print(f"\r{text}{color_percent}{PERCENT}{color_bar}{SIGN}{color_etc}{ETC_1}{color_etc2}{ETC_2}{OFF}{cursor.EraseLine(0)}",
            end='', flush=True)


class _Thread_bar(Thread, SepaProgress):
    def __init__(self, deq, N, time_interval,
                 symbol_1, symbol_2,
                 color, text, terminal,t0,time_zone):

        super().__init__()
        self.deq = deq
        self.t0 = t0
        self.N = N
        self.time_interval = time_interval
        self.symbol_1=symbol_1
        self.symbol_2=symbol_2
        self.color=color
        self.terminal=terminal
        self.time_zone=time_zone
        # self.q_flag = 1 if isinstance(self.deq[0],tuple) else 0

    def run(self):
        while True:
            idx = self.deq[0][0]
            self.appearance(idx, self.N, self.color,
                            self.symbol_1, self.symbol_2,
                            self.deq[0][1],
                            self.terminal,
                            self.t0,
                            self.time_zone)
            time.sleep(self.time_interval)
            if idx == self.N:
                break



def stop_thread(thread):
    import ctypes

    id = thread.ident
    code = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(id),
        ctypes.py_object(SystemError)
    )
    if code == 0:
        raise ValueError('invalid thread id')
    elif code != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(id),
            ctypes.c_long(0)
        )
        raise SystemError('PyThreadState_SetAsyncExc failed')

def trydecorator(__threadname=None):
    def middle(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except BaseException as e:
                stop_thread(__threadname)
                raise e
        return wrap
    return middle

def trydecorator2(func=None, __threadname=None):
    if func is None:
        return partial(trydecorator2, __threadname=__threadname)
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BaseException as e:
            stop_thread(__threadname)
            raise e
    return wrap

import sys
def trydecorator3(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        global __threadbar
        isInterrupt = False
        try:
            func(*args, **kwargs)
        except BaseException as e:
            stop_thread(__threadbar)
            isInterrupt = True
            raise e
        finally:
            if isInterrupt:
                stop_thread(__threadbar)
                sys.exit()
    return wrap

