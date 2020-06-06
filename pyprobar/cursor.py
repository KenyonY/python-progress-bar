import abc
from .styleString import setRGB, CSI, OFF, rgb_str
import sys

class BaseCursor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def FORWARD(self,*args, **kwargs):
        '''Forward move'''
        pass

    @abc.abstractmethod
    def BACK(self,*args, **kwargs):
        '''Backward move'''
        pass

    @abc.abstractmethod
    def PreLINE(self,*args, **kwargs):
        """Moves cursor to beginning of the line n (default 1) lines up.
        No any character will be cleared.
        """
        pass

    @abc.abstractmethod
    def EraseLine(self, *args, **kwargs):
        """Erases part of the line.
        If n is 0, clear from cursor to the end of the line.
        If n is 1, clear from cursor to beginning of the line.
        If n is 2, clear entire line. Cursor position does not change.
        """
        pass

    # @abc.abstractmethod
    # def EraseUpLine(self, *args, **kwargs):
    #     """Erase n lines and cursor move up n lines"""
    #     pass

    @abc.abstractmethod
    def savePOS_x(self, *args, **kwargs):
        """Save current position"""
        pass

    @abc.abstractmethod
    def restorePOS_x(self, *args, **kwargs):
        """Restore saved position"""
        pass

    @abc.abstractmethod
    def getPOS(self):
        pass

def send(code):
    sys.stdout.write(code)
    sys.stdout.flush()

def csi(n, code):
    return CSI + str(n) + code

class Cursor(BaseCursor):
    '''See: http://en.wikipedia.org/wiki/ANSI_escape_code'''
    def UP(self, n=1):
        """Moves the cursor n (default 1) cells in the given direction."""
        return csi(n, 'A')
    def DOWN(self, n=1):
        """Moves the cursor n (default 1) cells in the given direction."""
        return csi(n, 'B')
    def FORWARD(self, n=1):
        """Moves the cursor n (default 1) cells in the given direction."""
        return csi(n, 'C')
    def BACK(self, n=1):
        """Moves the cursor n (default 1) cells in the given direction."""
        return csi(n, 'D')
    def NextLINE(self,n=1):
        return csi(n, "E")
    def PreLINE(self, n=1):
        """Moves cursor to beginning of the line n (default 1) lines up.
        No any character are cleared.
        """
        return csi(n, 'F')

    def HorizCol(self, n=1):
        """Moves the cursor to column n"""
        return csi(n, 'G')

    def POS(self, x=1, y=1):
        """Moves the cursor to row n, column m.
        The values are 1-based, and default to 1 (top left corner) if omitted."""
        return CSI + str(y) + ';' + str(x) + 'H'

    def EraseLine(self, n=0):
        """Erases part of the line.
        If n is 0, clear from cursor to the end of the line.
        If n is 1, clear from cursor to beginning of the line.
        If n is 2, clear entire line. Cursor position does not change.
        """
        if n == 0:
            return CSI + "K"
        else:
            return csi(n, 'K')

    def EraseDisplay(self, n=0):
        """Clears part of the screen. 
        If n is 0, clear from cursor to end of screen.
        If n is 1, clear from cursor to beginning of the screen. 
        If n is 2, clear entire screen (and moves cursor to upper left on DOS ANSI.SYS). 
        If n is 3, clear entire screen and delete all lines saved in the scrollback buffer.
        """
        return csi(n, "J")

    def ScrollUp(self, n=1):
        """Scroll whole page up by n (default 1) lines.
        New lines are added at the bottom.
        """
        return csi(n, "S")

    def  ScrollDown(self, n=0):
        """Scroll whole page down by n (default 1) lines.
        New lines are added at the top. """
        return csi(n, "T")

    def savePOS_x(self):
        return "\033[s"  #"\0337"

    def restorePOS_x(self):
        return "\033[u"  #"\0338"

    def getPOS(self):
        return CSI + "6n"

    def hiddenCursor(self):
        return "\033[?25l"


if __name__ == "__main__":
    import time
    cursor = Cursor()
    POS = cursor.getPOS()
    print(POS)

    def test():
        cursor = Cursor()
        POS = cursor.getPOS()
        print(POS)
        print(f"""
        1111111111111111
        2222222222222222
        3333333333333333
        4444444444444444
        5555555555555555
        6666666666666666
        777777777777{cursor.restorePOS_x()}hahahha
        8888888888888888
        9999999999999999
        0000000000000000
        """)

    test()

