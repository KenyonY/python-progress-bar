from pyprobar.utils import dict_dotable

CSI = '\033['
OSC = '\033]'
OFF = CSI + '0m'

rgb_dict = {
    "浅绿": (66, 227, 35),
    "深绿": (28, 97, 15),
    "嫩绿": (194, 250, 134),
    "天青": (28, 199, 212),
    "紫色": (146, 52, 247),
    "浅紫": (214, 126, 209),
    "浅蓝": (186, 189, 250),
    "天蓝": (56, 116, 217),
    "蓝1": (115, 182, 225),
    "蓝2": (117, 181, 244),
    "绿1": (190, 237, 199),
    "绿2": (140, 199, 181),
    "绿3": (190, 231, 233),
    "玫瑰红": (237, 166, 178),
    "粉色": (250, 205, 229),
    "浅黑": (85, 85, 85),
    "灰色": (112, 112, 112),
    "亮灰": (204, 204, 204)
}
rgb_dict = dict_dotable(rgb_dict)


def setRGB(RGB_fore=[240, 85, 85], SRG=0, RGB_back=None):
    """Get foreground or background color chars
    see https://my.oschina.net/dingdayu/blog/1537064
    inputs:
        RGB_fore: rgb list or tupe of foreground, e.g. [255, 0, 0]
        SRG:  the style of font
        SRG options: see https://en.wikipedia.org/wiki/ANSI_escape_code#SGR
            | 0  |     Close all formats and revert to the original state
            | 1  |     Bold (increased intensity)
            | 2  |     Faint (decreased intensity)
            | 3  |     Italics
            | 4  |     Underline (single line)
            | 5  |     Slow Blink
            | 6  |     Rapid Blink
            | 7  |     Swap the background color with the foreground color
    """
    Fore_color = f"{CSI}{SRG};38;2;{RGB_fore[0]};{RGB_fore[1]};{RGB_fore[2]}m"
    if RGB_back is None:
        Back_color = ''
    else:
        Back_color = f"{CSI}{SRG};48;2;{RGB_back[0]};{RGB_back[1]};{RGB_back[2]}m"
    return Fore_color + Back_color


def rgb_str(string, RGB_fore=[240, 85, 85], SRG=0, RGB_back=None):
    return setRGB(RGB_fore, SRG, RGB_back) + string + OFF
