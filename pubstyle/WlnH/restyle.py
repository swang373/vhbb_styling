import os

from rootpy import ROOT
from rootpy.io import root_open
from vhbbtools.plotting import CMSCanvas


COLOR_CONVERSION = {
    'ST_s': ROOT.kBlue-9,
    'TT': ROOT.kBlue+3,
    'WJetsHT100_2b': ROOT.kGreen-10,
    'WJetsHT100_1b': ROOT.kGreen-8,
    'WJetsHT100_0b': ROOT.kGreen-5,
    'ZJetsHT100_2b': ROOT.kOrange-4,
    'ZJetsHT100_1b': ROOT.kOrange,
    'ZJetsHT100_0b': ROOT.kOrange-3,
    'WW_1b': ROOT.kMagenta-5,
    'WW_0b': ROOT.kMagenta-8,
    'QCDHT700': ROOT.kGray+1,
    'ggZH': 632-7,
    'WminusH': 632+2,
    'ZH': 632,
}


def set_coordinates_NDC(obj, x1, y1, x2, y2):
    obj.SetX1NDC(x1)
    obj.SetY1NDC(y1)
    obj.SetX2NDC(x2)
    obj.SetY2NDC(y2)


def transform_upper_pad(pad, gap=True):
    # Modify pad.
    if gap:
        pad.SetPad(0.0, 0.301, 1.0, 1.0)
        pad.SetBottomMargin(0.018)
    else:
        pad.SetPad(0.0, 0.3, 1.0, 1.0)
    pad.SetTopMargin(0.08)
    pad.SetLeftMargin(0.13)
    # Modify primitives.
    primitives = pad.GetListOfPrimitives()
    stack = primitives[1]
    lines = primitives[2:14]
    data = primitives[14]
    legends = primitives[15:17]
    texts = primitives[17:]
    ### Stack
    for hist in stack.GetHists():
        hist.SetLineWidth(1)
        #hist.SetFillColor(COLOR_CONVERSION[hist.GetTitle()])
    if gap:
        stack.GetXaxis().SetLabelSize(0.)
        stack.GetXaxis().SetTitleSize(0.)
    else:
        stack.SetMinimum(0.001)
    y_axis = stack.GetYaxis()
    y_axis.SetTitle('Entries / 10 GeV')
    y_axis.SetTitleOffset(1.2)
    y_axis.SetTitleSize(0.05)
    ### Lines
    for line in lines:
        line.SetLineWidth(1)
    ### Data
    data_new = data.Clone()
    data_new.SetMarkerSize(0.9)
    data.Reset()
    primitives.Add(data_new, 'E1SAME')
    ### Legends
    for legend in legends:
        primitives.Remove(legend)
    legend1, legend2 = [legend.Clone() for legend in legends]
    set_coordinates_NDC(legend1, 0.46, 0.56, 0.71, 0.88)
    primitives.Add(legend1)
    #legend2.GetListOfPrimitives()[-1].SetLabel('MC Unc. (Stat.)')
    set_coordinates_NDC(legend2, 0.68, 0.56, 0.93, 0.88)
    primitives.Add(legend2)
    ### Texts
    for text in texts:
        primitives.Remove(text)
    _, text2 = [text.Clone() for text in texts]
    set_coordinates_NDC(text2, 0.17, 0.72, 0.3, 0.76)
    text2.GetListOfLines()[0].SetTitle('1-lepton (e)')
    primitives.Add(text2)
    text_new = text2.Clone()
    text_new.GetListOfLines()[0].SetTitle('t#bar{t} Enriched')
    set_coordinates_NDC(text_new, 0.17, 0.68, 0.3, 0.72)
    primitives.Add(text_new)


def transform_lower_pad(pad, gap=True):
    # Modify pad.
    if gap:
        pad.SetPad(0.0, 0.0, 1.0, 0.299)
        pad.SetTopMargin(0)
        pad.SetFillColor(0)
        pad.SetFillStyle(0)
    else:
        pad.SetPad(0.0, 0.0, 1.0, 0.3)
    pad.SetBottomMargin(0.349)
    pad.SetLeftMargin(0.13)
    pad.SetGrid(0, 0)
    # Modify primitives.
    primitives = pad.GetListOfPrimitives()
    _, ratio, uncertainty, text = primitives
    ### Ratio
    ratio.SetMaximum(1.999)
    ratio.SetMinimum(0)
    x_axis, y_axis = ratio.GetXaxis(), ratio.GetYaxis()
    x_min = x_axis.GetBinLowEdge(x_axis.GetFirst())
    x_max = x_axis.GetBinUpEdge(x_axis.GetLast())
    x_axis.SetLabelFont(42)
    x_axis.SetLabelOffset(0.007)
    x_axis.SetLabelSize(0.11)
    #x_axis.SetTitle('p_{T}(V) [GeV]')
    x_axis.SetTitleFont(42)
    x_axis.SetTitleOffset(1.25)
    x_axis.SetTitleSize(0.11)
    y_axis.SetLabelFont(42)
    y_axis.SetLabelOffset(0.007)
    y_axis.SetLabelSize(0.11)
    y_axis.SetTitle('Data / MC')
    y_axis.SetTitleFont(42)
    y_axis.SetTitleOffset(0.55)
    y_axis.SetTitleSize(0.11)
    y_axis.CenterTitle()
    ratio_new = ratio.Clone()
    ratio_new.SetMarkerSize(0.9)
    ratio_new.SetLineWidth(1)
    ratio.Reset()
    primitives.Add(ratio_new, 'E1SAME')
    ### Text
    text.SetTextSize(0.078)
    set_coordinates_NDC(text, 0.17, 0.89, 0.3, 0.95)
    ### Unity Line
    line = ROOT.TLine(x_min, 1, x_max, 1)
    primitives.Add(line, 'SAME')
    ### Legend
    legend = ROOT.TLegend(0.32, 0.86, 0.93, 0.97)
    legend.SetLineWidth(2)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(4000)
    legend.SetTextSize(0.075)
    legend.SetNColumns(2)
    legend.AddEntry(uncertainty, 'MC Unc. (Stat.)', 'f')
    primitives.Add(legend, 'SAME')


def restyle(path):
    ROOT.gROOT.SetBatch(True)
    name, _ = os.path.splitext(path)
    with root_open(path) as f:
        old_canvas = f.GetListOfKeys()[0].ReadObj()
        upper_pad = old_canvas.GetPrimitive('can_0')
        lower_pad = old_canvas.GetPrimitive('can_1')
        with CMSCanvas(height=800) as new_canvas:
            ROOT.TGaxis.SetMaxDigits(3)
            ROOT.gStyle.SetErrorX(0)
            # Port over the upper pad in context of the new canvas.
            transform_upper_pad(upper_pad)
            upper_pad.Draw()
            upper_pad.cd()
            new_canvas.decorate(lumi_text='35.9 fb^{-1} (13 TeV)', extra_text='Preliminary')
            upper_pad.Modified()
            upper_pad.Update()
            upper_pad.RedrawAxis()
            new_canvas.cd()
            # Port over the lower pad in context of the new canvas.
            transform_lower_pad(lower_pad)
            lower_pad.Draw()
            lower_pad.Modified()
            lower_pad.Update()
            lower_pad.RedrawAxis()
            new_canvas.SaveAs('{}_restyled.pdf'.format(name))


if __name__ == '__main__':

    for path in [
        #'Vpt_TTCR_Wmn.root',
        'TopMass_TTCR_Wen.root',
    ]:
        restyle(path)

