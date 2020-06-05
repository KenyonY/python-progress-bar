# import sys
# from queue import Queue
import time, datetime
from datetime import timedelta
import abc
import random
from pyprobar.styleString import setRGB, rgb_str, OFF, rgb_dict
from pyprobar.cursor import Cursor
import numpy as np
from threading import Thread
from collections import deque


cursor = Cursor()

class Progress(metaclass=abc.ABCMeta):
    unit_percent = 0.034
    total_space = 30
    COLOR_bar = None

    @abc.abstractmethod
    def currentProgress(self):
        pass

    @abc.abstractmethod
    def appearance(self):
        pass

    @abc.abstractmethod
    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""

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
            # 如果只指定一个颜色，则这个颜色给bar
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
    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""
        n_sign1, mod_sign1 = divmod(percent, self.unit_percent)
        N1 = int(n_sign1)
        sign1 = symbol_1 * N1
        N0 = int((mod_sign1 / self.unit_percent) * (self.total_space - N1))

        sign0 = symbol_2 * N0
        SIGN = '|' + sign1 + sign0 + (self.total_space - N1 - N0 - 1) * ' ' + '|'
        return SIGN, N1

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
        return _PERCENT, _REMAIN , _ETC

    def appearance(self, idx, total_steps, symbol_1, symbol_2, t0, color, N_colors,terminal):
        counts = idx + 1
        percent = counts / total_steps

        if idx == 0:
            print(f"\r{0:.2f}% \t  {0:.1f}|{float('inf'):.1f}s{cursor.EraseLine(0)}", end='', flush=True)
        else:

            SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
            _PERCENT, _REMAIN , _ETC = self.currentProgress(percent, t0, terminal)
            color_percent, color_bar, color_etc, color_etc2 = sepabar.get_bar_color(N1, color, N_colors=N_colors)
            # color_percent,color_bar, color_etc, color_etc2 = setRGB(rgb_dict["灰色"]),setRGB(rgb_dict["粉色"]),
            # setRGB(rgb_dict["浅绿"]), setRGB(rgb_dict["天蓝"])
            print('\r' + color_percent + f"{_PERCENT}" + color_bar + SIGN + \
                  color_etc  + _REMAIN + color_etc2 + _ETC + OFF + cursor.EraseLine(0), end='',
                  flush=True)
        if counts == total_steps:
            print('')


class ThreadBar(Thread, IntegProgress):
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

class probar(IntegProgress):
    """Colorful progress bar.

    :arg color: options  'const_random', 'update_random', '0','1','2',...,'n?'
        or RGB a list, such as [250,205,229] or [[146,52,247],[250,205,229],[66,227,35],[214,126,209]]
    :arg enum: enumerate mode
    :arg time_interval: Progress bar refresh interval

    Examples
    --------
    >>> for i in probar(range(10)):
    >>>     ...

    >>> for idx, i in probar(range(10), enum=True):
    >>>     ...

    >>> res  = [i for i in probar(range(10))]
    """

    def __init__(self, iterable, total_steps=None, symbol_1="█", symbol_2='>',
                 color='const_random',N_colors=4,
                 enum = False,
                 time_interval=0.02,
                 terminal=False):

        self.iterable = iterable
        self.t0 = time.time()
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.terminal = terminal
        self.color = color
        self.N_colors = N_colors
        self.enum = enum

        if hasattr(iterable, '__len__'):
            self.total_steps = len(iterable)
        else:
            self.total_steps = total_steps
            if self.total_steps == None:
                raise ValueError(f'{iterable} has no __len__ attr, use total_steps param')

        # self.q = Queue(2)
        self.q = deque(maxlen=1)
        self.q.append(0)
        self.threadbar = ThreadBar(self.q, self.total_steps, time_interval,
                              self.symbol_1, self.symbol_2,
                              self.t0, self.color, self.N_colors, self.terminal)

        self.threadbar.setDaemon(True)
        self.threadbar.start()

    def __iter__(self):
        for idx, i in enumerate(self.iterable):
            self.q.append(idx)
            item = (idx, i) if self.enum else i
            yield item
        self.threadbar.join()



class SepaProgress(Progress):
    def current_bar(self, percent, symbol_1="█", symbol_2='>'):
        """Get the appearance of current  bar"""
        n_sign1, mod_sign1 = divmod(percent, self.unit_percent)
        N1 = int(n_sign1)
        sign1 = symbol_1 * N1
        N0 = int((mod_sign1 / self.unit_percent) * (self.total_space - N1))

        sign0 = symbol_2 * N0
        SIGN = '|' + sign1 + sign0 + (self.total_space - N1 - N0 - 1) * ' ' + '|'
        return SIGN, N1

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
        return _PERCENT, _REMAIN , _ETC

    def appearance(self, _index, total_size,
                   color='const_random',
                   symbol_1="█", symbol_2='>',
                   text='',
                   terminal=True):

        percent = (_index) / total_size
        SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
        PERCENT, ETC_1, ETC_2 = self.currentProgress(percent, t0, terminal)
        color_percent, color_bar, color_etc, color_etc2 = self.get_bar_color(N1, color, N_colors=4)
        if text != '': text += "|"
        print(f"\r{text}{color_percent}{PERCENT} {color_bar}{SIGN}{color_etc}{ETC_1}{color_etc2}{ETC_2} {OFF} {cursor.EraseLine(0)}",
            end='', flush=True)

class _thread_bar(Thread, SepaProgress):
    def __init__(self, deq, N, time_interval,
                 symbol_1, symbol_2,
                 color, text, terminal):

        super().__init__()
        self.deq = deq
        self.N = N
        self.time_interval = time_interval
        self.symbol_1=symbol_1
        self.symbol_2=symbol_2
        self.color=color
        self.terminal=terminal
        self.q_flag = 0 if text=='' else 1

    def run(self):
        while True:
            if self.q_flag == 1:
                idx = self.deq[0][0]
                text = self.deq[0][1]
            else:
                idx = self.deq[0]
                text = ''

            self.appearance(idx, self.N, self.color,
                            self.symbol_1, self.symbol_2,
                            text,
                            self.terminal)

            time.sleep(self.time_interval)

            if idx == self.N:
                break


sepabar = SepaProgress()
q = deque(maxlen=1)
def bar(index, total_steps,time_interval=0.02,
        color='const_random',
        symbol_1="█", symbol_2='>',
        text='',
        terminal=True):
    """Colorful progress bar.

    :arg color: options  'constant_random', '0','1','2',...,'n?',
        or RGB a list, such as [250,205,229] or [[146,52,247],[250,205,229],[66,227,35],[214,126,209]]

    Examples
    --------
    >>> for idx, i in enumerate(range(1000)):
    >>>     bar(idx, 1000)
    >>>     ...

    >>> for idx, i in enumerate(iterable_x):
    >>>     bar(idx, len(iterable_x),text='I want show some texts in progress bar.')
    >>>     ...

    >>> N = len(iterable_x)
    >>> for idx, i in enumerate(iterable_x):
    >>>     bar(idx, N,color='const_random')
    >>>     ...

    >>> N = len(iterable_x)
    >>> for idx, i in enumerate(iterable_x):
    >>>     bar(idx, N,color = [[146,52,247],[250,205,229],[66,227,35],[214,126,209]])
    >>>     ...
    """
    global t0, threadbar
    _index = index + 1
    if text == '':
        q.append(_index)
    else:
        q.append((_index, text))

    if index == 0:
        t0 = time.time()
        threadbar = _thread_bar(q, total_steps, time_interval,
                                symbol_1, symbol_2,
                                color, text, terminal)
        threadbar.setDaemon(True)
        threadbar.start()

    if _index == total_steps:
        threadbar.join()
        print('')


if __name__ == "__main__":
    pass

