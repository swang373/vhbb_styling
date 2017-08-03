from rootpy import ROOT

from .exceptions import TextAlignmentError


class BaseLabel(ROOT.TLatex):
    """The base label class.
    """

    # Tuples of horizontal and vertical text alignment names and
    # their corresponding ROOT text alignment integer values.
    TEXT_ALIGNMENT = {
        ('left', 'bottom'): 11,
        ('left', 'center'): 12,
        ('left', 'top'): 13,
        ('center', 'bottom'): 21,
        ('center', 'center'): 22,
        ('center', 'top'): 23,
        ('right', 'bottom'): 31,
        ('right', 'center'): 32,
        ('right', 'top'): 33,
    }

    def __init__(self):
        super(BaseLabel, self).__init__()

    @property
    def align(self):
        return self.GetTextAlign()

    @align.setter
    def align(self, value):
        if value in self.TEXT_ALIGNMENT:
            self.SetTextAlign(self.TEXT_ALIGNMENT[value])
        elif value in self.TEXT_ALIGNMENT.values():
            self.SetTextAlign(value)
        else:
            raise TextAlignmentError('Unrecognized value: {!s}'.format(value))

    @property
    def font(self):
        return self.GetTextFont()

    @font.setter
    def font(self, value):
        self.SetTextFont(value)

    @property
    def size(self):
        return self.GetTextSize()

    @size.setter
    def size(self, value):
        self.SetTextSize(value)

