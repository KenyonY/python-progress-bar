from collections import deque
from .compose import _Thread_probar, _Thread_bar
import time


class probar():
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
        self.threadbar = _Thread_probar(self.q, self.total_steps, time_interval,
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
    global threadbar, q
    _index = index + 1
    if text == '':
        q.append(_index)
    else:
        q.append((_index, text))

    if index == 0:
        t0 = time.time()
        threadbar = _Thread_bar(q, total_steps, time_interval,
                                symbol_1, symbol_2,
                                color, text, terminal,t0)
        threadbar.setDaemon(True)
        threadbar.start()

    if _index == total_steps:
        threadbar.join()
        print('')


if __name__ == "__main__":
    pass

