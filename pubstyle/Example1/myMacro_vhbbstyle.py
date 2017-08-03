import array

import ROOT

from vhbbtools.plotting import CMSCanvas


canvas = CMSCanvas()
with canvas:
    h = ROOT.TH1F('h', 'h; m_{e^{+}e^{-}} (GeV); Events / 0.5 GeV', 80, 70, 110)
    h.SetMaximum(260)
    h.GetXaxis().SetNdivisions(6, 5, 0)
    h.GetYaxis().SetNdivisions(6, 5, 0)
    h.GetYaxis().SetTitleOffset(1)
    h.Draw()

    f = ROOT.TFile('histo.root')
    h_mc = f.Get('MC')
    h_mc.Draw('histsame')
    h_data = f.Get('data')
    h_data.Draw('esamex0')

    canvas.decorate(lumi_text='18.3 fb^{-1} (8 TeV) + 4.8 fb^{-1} (7 TeV)', cms_position='outside', extra_text='Preliminary')
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()

    # Set the colors and size for the legend
    histLineColor = ROOT.kOrange + 7
    histFillColor = ROOT.kOrange - 2
    markerSize = 1.0

    latex = ROOT.TLatex()
    n_ = 2

    x1_l = 0.92
    y1_l = 0.60
    dx_l = 0.30
    dy_l = 0.18
    x0_l = x1_l - dx_l
    y0_l = y1_l - dy_l

    legend = ROOT.TPad('legend_0', 'legend_0', x0_l, y0_l, x1_l, y1_l)
    legend.Draw()
    legend.cd()

    ar_l = dy_l / dx_l
    gap_ = 1. / (n_+1)
    bwx_ = 0.12
    bwy_ = gap_ / 1.5

    x_l = [1.2 * bwx_]
    y_l = [1 - gap_]
    ex_l = [0]
    ey_l = [0.04 / ar_l]

    #array must be converted
    x_l = array.array('f', x_l)
    ex_l = array.array('f', ex_l)
    y_l = array.array('f', y_l)
    ey_l = array.array('f', ey_l)

    gr_l =  ROOT.TGraphErrors(1, x_l, y_l, ex_l, ey_l)

    ROOT.gStyle.SetEndErrorSize(0)
    gr_l.SetMarkerSize(0.9)
    gr_l.Draw('0P')

    latex.SetTextFont(42)
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)
    latex.SetTextSize(0.25)
    latex.SetTextAlign(12)

    box_ = ROOT.TBox()
    xx_ = x_l[0]
    yy_ = y_l[0]
    latex.DrawLatex(xx_ + 1.*bwx_, yy_, 'Data')

    yy_ -= gap_
    box_.SetLineStyle(ROOT.kSolid)
    box_.SetLineWidth(1)
    box_.SetLineColor(histLineColor)
    box_.SetFillColor(histFillColor)
    box_.DrawBox(xx_ - bwx_/2, yy_ - bwy_/2, xx_ + bwx_/2, yy_ + bwy_/2)
    box_.SetFillStyle(0)
    box_.DrawBox(xx_ - bwx_/2, yy_ - bwy_/2, xx_ + bwx_/2, yy_ + bwy_/2)
    #Draw Z->ee text
    latex.DrawLatex(xx_ + 1.*bwx_, yy_, 'Z #rightarrow e^{+}e^{-} (MC)')

    #update the canvas to draw the legend
    canvas.Update()

    raw_input("Press Enter to end")
    f.Close()

