from rootpy import ROOT

from .bases import BaseLabel
from .exceptions import PositionError


__all__ = [
    'CMSLabel',
]


class CMSLabel(BaseLabel):
    """The CMS label. Credits to Gautier Hamel de Monchenault (Saclay), Joshua Hardenbrook
    (Princeton), and Dinko Ferencek (Rutgers) for the initial Python implementation.

    The following style attributes can be modified:
    * text : string
      The CMS label text. The default is 'CMS'.

    * position : string
      The text position on the active canvas:
      - left : top left corner inside the frame (default)
      - center : top center inside the frame
      - right : top right corner inside the frame
      - outside : top left corner outside the frame

    * font : int
      The text font code. The default is 61 (Helvetica Bold).

    * scale : float
      The text size scale relative to the size of the top margin of the active canvas.
      The default is 0.75.

    * padding_left : float
      The amount of padding to the left of the text when positioned inside the frame,
      relative to the frame width of the active canvas. The default is 0.045.

    * padding_right : float
      The amount of padding to the right of the text when positioned inside the frame,
      relative to the frame width of the active canvas. The default is 0.045.

    * padding_top : float
      The amount of padding above the text. When positioned inside of the frame, it is
      relative to the frame height of the active canvas and the default is 0.035. When
      positioned outside of the frame, it is relative to the size of the top margin of
      the active canvas and the default is 0.8.

    * sublabel.text : string
      The sublabel text positioned below the main text inside of the frame or to the
      right of the main text outside of the frame. Common examples are 'Preliminary',
      'Simulation', or 'Unpublished'. The default is empty string for no sublabel.

    * sublabel.font : string
      The sublabel text font code. The default is 52 (Helvetica Italic).

    * sublabel.scale : float
      The sublabel text size scale relative to the size of the main text.
      The default is 0.76.

    * sublabel.padding_left : float
      The amount of padding to the left of the sublabel text relative to the frame
      width of the active canvas. This only applies if the main text is positioned
      outside the frame of the active canvas. The default is 0.12.

    * sublabel.padding_top : float
      The amount of padding above the sublabel text relative to the size of the main
      text. This only applies if the main text is positioned inside the frame of the
      active canvas. The default is 1.2.
    """
    def __init__(self):
        super(CMSLabel, self).__init__()
        self.text = 'CMS'
        self.position = 'left'
        self.font = 61
        self.scale = 0.75
        self.padding_left = 0.045
        self.padding_right = 0.045
        self.padding_top = None
        self.sublabel = BaseLabel()
        self.sublabel.text = ''
        self.sublabel.font = 52
        self.sublabel.scale = 0.76
        self.sublabel.padding_left = 0.12
        self.sublabel.padding_top = 1.2

    def _draw_label_left(self):
        """Draw the label on the top left corner inside the frame and return its coordinates.
        """
        left_margin, right_margin, bottom_margin, top_margin = ROOT.gPad.margin
        self.size = self.scale * top_margin
        self.align = ('left', 'top')
        x = left_margin + self.padding_left * (1 - left_margin - right_margin)
        y = 1 - top_margin - (self.padding_top or 0.035) * (1 - top_margin - bottom_margin)
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_label_center(self):
        """Draw the label on the top center inside the frame and return its coordinates.
        """
        left_margin, right_margin, bottom_margin, top_margin = ROOT.gPad.margin
        self.size = self.scale * top_margin
        self.align = ('center', 'top')
        x = left_margin + 0.5 * (1 - left_margin - right_margin)
        y = 1 - top_margin - (self.padding_top or 0.035) * (1 - top_margin - bottom_margin)
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_label_right(self):
        """Draw the label on the top right corner inside the frame and return its coordinates.
        """
        left_margin, right_margin, bottom_margin, top_margin = ROOT.gPad.margin
        self.size = self.scale * top_margin
        self.align = ('right', 'top')
        x = 1 - right_margin - self.padding_right * (1 - left_margin - right_margin)
        y = 1 - top_margin - (self.padding_top or 0.035) * (1 - top_margin - bottom_margin)
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_label_outside(self):
        """Draw the label on the top left corner outside the frame and return its coordinates.
        """
        left_margin, _, _, top_margin = ROOT.gPad.margin
        self.size = self.scale * top_margin
        self.align = ('left', 'bottom')
        x = left_margin
        y = 1 - (self.padding_top or 0.8) * top_margin
        self.DrawLatexNDC(x, y, self.text)
        return x, y

    def _draw_sublabel_inside(self, x_label, y_label):
        """Draw the sublabel below the label inside the frame.
        """
        self.sublabel.size = self.sublabel.scale * self.size
        self.sublabel.align = self.align
        x_sublabel = x_label
        y_sublabel = y_label - self.sublabel.padding_top * self.size
        self.sublabel.DrawLatexNDC(x_sublabel, y_sublabel, self.sublabel.text)

    def _draw_sublabel_outside(self, x_label, y_label):
        """Draw the sublabel to the right of the label outside the frame.
        """
        left_margin, right_margin, _, _ = ROOT.gPad.margin
        self.sublabel.size = self.sublabel.scale * self.size
        self.sublabel.align = self.align
        x_sublabel = left_margin + self.sublabel.padding_left * (1 - left_margin - right_margin)
        y_sublabel = y_label
        self.sublabel.DrawLatexNDC(x_sublabel, y_sublabel, self.sublabel.text)

    def draw(self):
        """Draw the CMS label and sublabel on the active canvas.
        """
        # Draw the label.
        if self.position == 'left':
            label_coordinates = self._draw_label_left()
        elif self.position == 'center':
            label_coordinates = self._draw_label_center()
        elif self.position == 'right':
            label_coordinates = self._draw_label_right()
        elif self.position == 'outside':
            label_coordinates = self._draw_label_outside()
        else:
            raise PositionError('Unrecognized value: {}'.format(self.position))
        # Draw the sublabel.
        if self.sublabel.text:
            if self.position == 'outside':
                self._draw_sublabel_outside(*label_coordinates)
            else:
                self._draw_sublabel_inside(*label_coordinates)

