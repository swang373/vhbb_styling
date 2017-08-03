from rootpy import ROOT

from .bases import BaseLabel


__all__ = [
    'LuminosityLabel',
]


class LuminosityLabel(BaseLabel):
    """The luminosity label positioned at the top right corner outside of the frame.
    Credits to Gautier Hamel de Monchenault (Saclay), Joshua Hardenbrook (Princeton),
    and Dinko Ferencek (Rutgers) for the initial Python implementation.

    The following style attributes can be modified:
    * font : int
      The text font code. The default is 42 (Helvetica).

    * scale : float
      The text size scale relative to the size of the top margin of the active canvas.
      The default is 0.6.

    * align : int or 2-tuple of strings
      The text alignment relative to the drawing coordinates of the text as either an
      integer code or tuple of horizontal and vertical alignment names, respectively.
      The default is ('right', 'bottom'), which is equivalent to 31.

    * padding_top : float
      The amount of padding above the text relative to the size of the top margin of
      the active canvas. The default is 0.8.

    Parameters
    ----------
    text : string
        The luminosity label text. Data taking periods must be separated by
        the "+" symbol, e.g. '19.7 fb^{-1} (8 TeV) + 4.9 fb^{-1} (7 TeV)'.
    """
    def __init__(self, text):
        super(LuminosityLabel, self).__init__()
        self.text = text
        self.font = 42
        self.scale = 0.6
        self.align = ('right', 'bottom')
        self.padding_top = 0.8

    def draw(self):
        """Draw the luminosity label on the active canvas.
        """
        _, right_margin, _, top_margin = ROOT.gPad.margin
        self.size = self.scale * top_margin
        x = 1 - right_margin
        y = 1 - self.padding_top * top_margin
        self.DrawLatexNDC(x, y, self.text)

