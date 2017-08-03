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
    # Modify primitives.
    primitives = pad.GetListOfPrimitives()
    stack = primitives[1]
    data = primitives[3]
    annotations = primitives[4:]
    legends = primitives[4:6]
    texts = primitives[6:]
    ### Stack
    for hist in stack.GetHists():
        hist.SetLineWidth(1)
        #hist.SetFillColor(COLOR_CONVERSION[hist.GetTitle()])
    if gap:
        stack.GetXaxis().SetLabelSize(0.)
        stack.GetXaxis().SetTitleSize(0.)
    else:
        stack.SetMinimum(0.001)
    stack.GetYaxis().SetTitleOffset(1.2)
    ### Data
    data_new = data.Clone()
    data_new.SetMarkerSize(0.9)
    data.Reset()
    primitives.Add(data_new, 'E1SAME')
    ### Legends
    for legend in legends:
        primitives.Remove(legend)
    legend1, legend2 = [legend.Clone() for legend in legends]
    legend1.GetListOfPrimitives()[0].SetOption('ep')
    set_coordinates_NDC(legend1, 0.52, 0.56, 0.77, 0.88)
    primitives.Add(legend1)
    legend2.GetListOfPrimitives()[-1].SetLabel('MC Unc. (Stat.)')
    legend2.GetListOfPrimitives()[-1].SetOption('f')
    set_coordinates_NDC(legend2, 0.69, 0.56, 0.94, 0.88)
    primitives.Add(legend2)
    ### Texts
    for text in texts:
        primitives.Remove(text)
    _, _, text3, text4 = [text.Clone() for text in texts]
    text3.SetTitle('0-lepton')
    text3.SetY(0.73)
    primitives.Add(text3)
    text4.SetTitle('Z+b#bar{b} Enriched')
    text4.SetY(0.68)
    primitives.Add(text4)


def transform_lower_pad(pad, gap=True):
    # Modify pad.
    if gap:
        pad.SetPad(0.0, 0.0, 1.0, 0.299)
        pad.SetTopMargin(0)
        pad.SetFillColor(0)
        pad.SetFillStyle(0)
    else:
        pad.SetPad(0.0, 0.0, 1.0, 0.3)
    # Modify primitives.
    primitives = pad.GetListOfPrimitives()
    _, ratio1, legend, uncertainty, ratio2, _, text1, text2 = primitives
    ### Ratio
    ratio1.SetMaximum(1.999)
    ratio1.SetMinimum(0)
    ratio1.SetMarkerSize(0.9)
    #ratio1.GetXaxis().SetTitle('#||{#Delta#varphi(j_{1}, j_{2})}')
    #ratio1.GetXaxis().SetTitle('#it{E}_{T}^{miss} [GeV]')
    ratio1.GetXaxis().SetTitle('p_{T}(V) [GeV]')
    ratio1.GetXaxis().SetTitleOffset(1.2)
    ratio1.GetYaxis().SetTitle('Data / MC')
    ratio1.GetYaxis().SetTitleOffset(0.55)
    ratio2.SetMarkerSize(0.9)
    ### Uncertainty
    uncertainty.GetYaxis().SetLabelSize(0.)
    ### Legend
    legend.GetListOfPrimitives()[0].SetLabel('MC Unc. (Stat.)')
    set_coordinates_NDC(legend, 0.32, 0.86, 0.93, 0.97)
    ### Text
    primitives.Remove(text2)


def restyle(path):
    ROOT.gROOT.SetBatch(True)
    name, _ = os.path.splitext(path)
    with root_open(path) as f:
        old_canvas = f.GetListOfKeys()[0].ReadObj()
        upper_pad = old_canvas.GetPrimitive('oben')
        lower_pad = old_canvas.GetPrimitive('unten')
        with CMSCanvas(height=800) as new_canvas:
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
        'Vpt.root',
        #'dPhi_j1_j2.root',
    ]:
        restyle(path)

