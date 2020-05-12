# Pyprobar

[![image](https://img.shields.io/badge/Pypi-0.1.1.3-green.svg)](https://pypi.org/project/pyprobar)
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-K.y-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)




An easy-to-use progress bar tool for python.


## Installation

```bash
pip install pyprobar
```

## Synopsis
```bash
28.71% |████████>>>>>>>>>>>>>>>>>  | 0:00:22|0:00:31 ETC: 05-20 18:08:15
```

## Usage

Use `probar` or `bar` for different situations:

  ```python
  from pyprobar import bar, probar
  import time
  
  for idx, x in probar(range(1234)):
      time.sleep(0.02)
  ```
  ```bash
  >>> 18.31%|█████>>>>>                  | 0:00:20|0:00:25  ETC: 05-20 19:00:39
  ```
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
for idx, i in probar(range(1234), symbol_2="o"):
    time.sleep(0.01)
```
```bash
>>> 23.10%|██████ooooooooooooooooooo    | 0:00:10|0:00:14  ETC: 05-20 17:29:57
```

Tip: Search`charmap`  in win10 start menu, you can find a lot of interesting characters.



**Supports progress bars in different colors**:

```python
for idx, i in enumerate(a):
    bar(idx, N, color='1')
    time.sleep(0.01)
```





Of course, you can also add text or variables to the progress bar:

```python
for idx, i in enumerate(a):
	text = f"what you want see is {x}"
    bar(idx, N, text=text)
```



print RGB color string:

```python
from pyprobar.styleString import rgb_str
text = rgb_str("I'm green!", RGB=[0,255,0])
print(text)
```







