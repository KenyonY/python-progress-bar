from pyprobar.styleString import rgb_str
from pyprobar import probar, bar
import time

R,G,B = 255,0,0
s1 = rgb_str("I'm red", [R,G,B])
s2 = rgb_str("I'm green", [0, 255, 0])

def test_rgb_string():
    print(s1, s2)

def test_probar1():
    for idx, i in probar(range(1234), enum=True):
        time.sleep(0.0061)

def test_probar2():
    res = [i for i in probar(range(10), enum=False) ]
    print(res)

def test_probar3():
    for i in probar(range(1234), symbol_2="o"):
        time.sleep(0.01)

def test_custom_color():
    """test Custom colors"""
    color = [[146, 52, 247], [250, 205, 229], [66, 227, 35], [214, 126, 209]]
    for idx, i in enumerate(range(1234)):
        bar(idx, 1234, text=s2, color=color)
        time.sleep(0.005)

def test_performance():
    from tqdm import tqdm
    N = 3000000
    print("probar:")
    for i in probar(range(N), color='1', time_interval=0.02):
        pass
    time.sleep(0.5)
    
    print('bar:')
    for idx, i in enumerate(range(N)):
        bar(idx, N, text=f'{idx+1}', color='5')

    print("tqdm:")
    for i in tqdm(range(N)):
        pass

test_performance()


