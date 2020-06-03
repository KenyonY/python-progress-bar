import sys
import time, datetime
from datetime import timedelta
import abc
import random
from pyprobar.styleString import setRGB, rgb_str, OFF, rgb_dict
from pyprobar.cursor import Cursor
import numpy as np

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
        PERCENT = percent * 100
        if idx == 0:
            print(f"\r{0:.2f}% \t  {0:.1f}|{float('inf'):.1f}s{cursor.EraseLine(0)}", end='', flush=True)
            self.d_percent = 0.01
        else:
            if PERCENT >= self.d_percent:
                self.d_percent += 0.01
                SIGN, N1 = self.current_bar(percent, symbol_1, symbol_2)
                _PERCENT, _REMAIN , _ETC = self.currentProgress(percent, t0, terminal)
                color_percent, color_bar, color_etc, color_etc2 = sepabar.get_bar_color(N1, color, N_colors=N_colors)
                # color_percent,color_bar, color_etc, color_etc2 = setRGB(rgb_dict["灰色"]),setRGB(rgb_dict["粉色"]),
                # setRGB(rgb_dict["浅绿"]), setRGB(rgb_dict["天蓝"])
                print('\r' + color_percent + f"{_PERCENT}" + color_bar + SIGN + \
                      color_etc  + _REMAIN + color_etc2 + _ETC + OFF + cursor.EraseLine(0), end='',
                      flush=True)
        if counts == total_steps:
            print('\n')


class probar(IntegProgress):
    """Simple progress bar display, to instead of tqdm.

    :arg color: options  'const_random', 'update_random', '0','1','2',...,'n?'
        or RGB a list, such as [250,205,229] or [[146,52,247],[250,205,229],[66,227,35],[214,126,209]]
    """

    def __init__(self, iterable, total_steps=None, symbol_1="█", symbol_2='>',
                 color='const_random',N_colors=4,
                 terminal=False):
        self.iterable = iterable
        self.t0 = time.time()
        self.symbol_1 = symbol_1
        self.symbol_2 = symbol_2
        self.terminal = terminal
        self.color = color
        self.N_colors = N_colors

        if hasattr(iterable, '__len__'):
            self.total_steps = len(iterable)
        else:
            self.total_steps = total_steps
            if self.total_steps == None:
                raise ValueError(f'{iterable} has no __len__ attr, use total_steps param')

    def __iter__(self):
        for idx, i in enumerate(self.iterable):
            self.appearance(idx, self.total_steps, self.symbol_1, self.symbol_2,
                            self.t0, self.color, self.N_colors, self.terminal)
            yield idx, i

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

    def appearance(self):
        pass


sepabar = SepaProgress()
def bar(index, total_size,
        color='const_random',
        symbol_1="█", symbol_2='>',
        text='',
        terminal=True):
    """Simple progress bar display, to instead of tqdm.

    :arg color: options  'constant_random', 'update_random', '0','1','2',...,'n?',
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
    global t0
    _index = index + 1
    if index == 0:
        t0 = time.time()
        index = 1
    percent = (_index)/total_size
    SIGN, N1 = sepabar.current_bar(percent, symbol_1, symbol_2)
    PERCENT, ETC_1 , ETC_2 = sepabar.currentProgress(percent, t0, terminal)
    color_percent, color_bar, color_etc, color_etc2 = sepabar.get_bar_color(N1, color, N_colors=4)
    if text != '': text += " |"
    print(f"\r{text}{color_percent}{PERCENT} {color_bar}{SIGN}{color_etc}{ETC_1}{color_etc2}{ETC_2} {OFF} {cursor.EraseLine(0)}",
          end='', flush=True)
    if _index == total_size:
        print('\n')


if __name__ == "__main__":
    # R,G,B = 255,0,0
    # s1 = rgb_str("I'm red", [R,G,B])
    s2 = rgb_str("I'm green", [0, 255, 0])
    # print(s1, s2)
    color = [[146,52,247],[250,205,229],[66,227,35],[214,126,209]]
    for idx, i in enumerate(range(1234)):
        bar(idx, 1234, text=s2,color='update_random')
        time.sleep(0.005)

    # for idx, i in probar(range(1234)):
    #     time.sleep(0.0061)




