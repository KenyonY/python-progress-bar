# Pyprobar

[![image](https://img.shields.io/badge/Pypi-0.1.1.5-green.svg)](https://pypi.org/project/pyprobar)
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-K.y-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)




An easy-to-use and colorful progress bar for python.


## Installation

```bash
pip install pyprobar
```

nightly version:

```bash
python night_workflow.py
```



## Synopsis

```bash
28.71% |████████>>>>>>>>>>>>>>>>>  | 0:00:22|0:00:31 ETC: 05-20 18:08:15
```

<img src="picture/color=1.gif" />

<img src="picture/color=5.gif" />

## Performance

```python
from pyprobar import probar
from tqdm import tqdm

N = 100000000
print("probar")
for i in probar(range(N)):
    pass
print("tqdm")
for i in tqdm(range(N)):
    pass
```

```bash
probar
100.00%|█████████████████████████████| 0:00:00|0:00:23  ETC: 06-05 13:30:56
tqdm
100%|██████████| 100000000/100000000 [00:26<00:00, 3802766.45it/s]
```



## Usage

Use `probar` or `bar` for different situations:

`probar`:

  ```python
  from pyprobar import bar, probar
  import time
  
  for idx, x in probar(range(1234), enum=True): 
      time.sleep(0.02)
  ```
  ```bash
  >>> 18.31%|█████>>>>>                  | 0:00:20|0:00:25  ETC: 05-20 19:00:39
  ```
Or  used in  List comprehensions:

```python
res = [i for i in probar(range(10))]
print(res)
```

```bash
>>> 100.00%|███████████████████████████| 0:00:00|0:00:00 ETC: 05-20 12:14:33
>>> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```



`bar`:

  ```python
  import numpy as np
  N = 1024
  a = np.linspace(2, 5, N)
  for idx, i in enumerate(a):
      time.sleep(0.01)
      bar(idx, N)
  ```
  ```bash
 >>> 100.00% |███████████████████████████| 0:00:00|0:00:10  ETC: 05-20 20:33:34 
  ```



You can set your own progress bar by using the parameters `symbol_1` and `symbol_2` :

```python
for i in probar(range(1234), symbol_2="o"):
    time.sleep(0.01)
```
```bash
>>> 23.10%|██████ooooooooooooooooooo    | 0:00:10|0:00:14  ETC: 05-20 17:29:57
```

Tip: Search`charmap`  in win10 start menu, you can find a lot of interesting characters.



**Supports progress bars in different colors**:

```python
for idx, i in enumerate(a):
    bar(idx, N, color='1') # `color` options: '1','2','3','4','5','0','update_random'
    time.sleep(0.01)
```

<img src="picture/color=1.gif" />



Of course, you can also add text or variables to the progress bar:

```python
for idx, i in enumerate(a):
    text = f"what you want see is {x}"
    bar(idx, N, text=text)
```

<img src=picture/text.gif />

multi-line text :

```python
for idx, i in enumerate(a):
    text = f"{v1}, frame:{idx}\n"
    bar(idx, N, text=text)
```

<img src="picture/multi_text.jpg" alt="multi_text" style="zoom:80%;" />



print RGB color string:

```python
from pyprobar.styleString import rgb_str
    text = rgb_str("I'm green!", RGB_fore=[0,255,0])
    print(text)
```

<img src="picture/rgb_str.jpg" />





