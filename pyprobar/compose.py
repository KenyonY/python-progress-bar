import time, datetime
from datetime import timedelta
import abc
import random
from pyprobar.styleString import setRGB, rgb_str, OFF, rgb_dict
from pyprobar.cursor import Cursor
import numpy as np
from threading import Thread
import inspect
import ctypes
from functools import wraps, partial

__all__ = ["_Thread_probar", "_Thread_bar", "stop_thread","trydecorator", "trydecorator2"]


cursor = Cursor()

class Progress(metaclass=abc.ABCMeta):
    unit_percent = 0.034
    total_space = 30
    COLOR_bar = None

    def currentProgress(self, percent, t0, terminal):
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
        _ETC = f" ETC: {(datetime.datetime.now() + remain_time).strftime('%m-%d %H:%M:%S')}"
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
    def get_color(N_color, update=True, COLOR=[0]):
        """Choice random n colors
        """

        if update == True or COLOR[0] == 0:

            # specify the first color
            rgb_list = [setRGB(rgb_dict["浅绿"])]
            for i in range(N_color - 2):
                rgb = rgb_dict[(random.choice(list(rgb_dict)))]
                rgb_list.append(setRGB(rgb))

            # specify the last color
            rgb_list.append(setRGB(rgb_dict["紫色"]))
            COLOR[0] = rgb_list
            return COLOR[0]
        else:
            return COLOR[0]

    def get_bar_color(self, N1, color, N_colors=4, flag_update_color=[None]):
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
    def appearance(self, idx, total_steps, symbol_1, symbol_2, t0, color, N_colors,terminal):
        counts = idx + 1
        percent = counts / total_steps
        if idx == 0:
            print(f"\r{0:.2f}% \t  {0:.1f}|{float('inf'):.1f}s{cursor.EraseLine(0)}", end='', flush=True)
        else:

            SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
            _PERCENT, _REMAIN , _ETC = self.currentProgress(percent, t0, terminal)
            color_percent, color_bar, color_etc, color_etc2 = self.get_bar_color(N1, color, N_colors=N_colors)
            # color_percent,color_bar, color_etc, color_etc2 = setRGB(rgb_dict["灰色"]),setRGB(rgb_dict["粉色"]),
            # setRGB(rgb_dict["浅绿"]), setRGB(rgb_dict["天蓝"])
            print('\r' + color_percent + f"{_PERCENT}" + color_bar + SIGN + \
                  color_etc  + _REMAIN + color_etc2 + _ETC + OFF + cursor.EraseLine(0), end='',
                  flush=True)


class _Thread_probar(Thread, IntegProgress):
    def __init__(self, deq, N, time_interval, symbol_1, symbol_2,
                            t0, color, N_colors, terminal):
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

    def run(self):
        while not self.stop:
            # idx = self.queue.get()
            idx = self.deq[0]
            self.appearance(idx, self.N, self.symbol_1, self.symbol_2,
                            self.t0, self.color, self.N_colors, self.terminal)
            time.sleep(self.time_interval)
            if idx == self.N-1:
                self.stop = True


class SepaProgress(Progress):
    def appearance(self, idx, total_size,
                   color='const_random',
                   symbol_1="█", symbol_2='>',
                   text='',
                   terminal=True,
                   t0=time.time()):

        percent = idx / total_size
        SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
        PERCENT, ETC_1, ETC_2 = self.currentProgress(percent, t0, terminal)
        color_percent, color_bar, color_etc, color_etc2 = self.get_bar_color(N1, color, N_colors=4)
        if text != '': text += "|"
        print(f"\r{text}{color_percent}{PERCENT}{color_bar}{SIGN}{color_etc}{ETC_1}{color_etc2}{ETC_2}{OFF}{cursor.EraseLine(0)}",
            end='', flush=True)


class _Thread_bar(Thread, SepaProgress):
    def __init__(self, deq, N, time_interval,
                 symbol_1, symbol_2,
                 color, text, terminal,t0):

        super().__init__()
        self.deq = deq
        self.t0 = t0
        self.N = N
        self.time_interval = time_interval
        self.symbol_1=symbol_1
        self.symbol_2=symbol_2
        self.color=color
        self.terminal=terminal
        self.q_flag = 1 if isinstance(self.deq[0],tuple) else 0

    def run(self):
        while True:
            if self.q_flag:
                idx = self.deq[0][0]
                text = self.deq[0][1]
            else:
                idx = self.deq[0]
                text = ''

            self.appearance(idx, self.N, self.color,
                            self.symbol_1, self.symbol_2,
                            text,
                            self.terminal,
                            self.t0)
            time.sleep(self.time_interval)
            if idx == self.N:
                break

def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def trydecorator(__threadname=None):
    def middle(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                stop_thread(__threadname)
                raise
        return wrap
    return middle

def trydecorator2(func=None, __threadname=None):
    if func is None:
        return partial(trydecorator2, __threadname=__threadname)
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            stop_thread(__threadname)
            raise
    return wrap


