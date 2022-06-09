#script to check run1 4353 of the LANL test beam

import ROOT as r 
import argparse



parser = argparse.ArgumentParser(description='Process srun4353.')
parser.add_argument('-f', '--filename', type=str, default= "./Run4353.root",
                    help='an integer for the accumulator')
parser.add_argument('-o', '--output', type=str, default= "testOutPF.root",
                    help='an integer for the accumulator')
args = parser.parse_args()



#read in desired root file, can also use sys.argv
f = r.TFile(args.filename,"READ")
fout = r.TFile(args.filename,"RECEREATE")

tree = f.Get("Events")
#output root tree


#histograms to be filled

h2V1 = r.TH2F("h2V1","Amplitude in NaI (Ch1) throughout run 4353;Entry;Peak amplitude [mV]", 100, 0, 100000, 100, 20, 930)
h2V2 = r.TH2F("h2V2","Amplitude in smallNaI 1 (Ch2) throughout run 4353;Entry;Peak amplitude [mV]", 100, 0, 100000, 100, 20, 930)
h2V3 = r.TH2F("h2V3","Amplitude in smallNaI 2 (Ch3) throughout run 4353;Entry;Peak amplitude [mV]", 100, 0, 100000, 100, 20, 930)
h2V4 = r.TH2F("h2V4","Amplitude in LYSO (Ch4) throughout run 4353;Entry;Peak amplitude [mV]", 100, 0, 100000, 100, 20, 930)
h2S1 = r.TH2F("h2S1","Hardware Scaler in NaI (Ch1) throughout run 4353;Entry;Hardware scaler [Hz]", 100, 0, 100000, 1000, 1, 1e5)
h2S2 = r.TH2F("h2S2","Hardware Scaler  in smallNaI 1 (Ch2) throughout run 4353;Entry;Hardware scaler [Hz]", 100, 0, 100000, 1000, 1, 1e5)
h2S3 = r.TH2F("h2S3","Hardware Scaler  in smallNaI 2 (Ch3) throughout run 4353;Entry;Hardware scaler [Hz]", 100, 0, 100000, 1000,1, 1e5)
h2S4 = r.TH2F("h2S4","Hardware Scaler  in LYSO (Ch4) throughout run 4353;Entry;Hardware scaler [Hz]", 100, 0, 100000, 1000, 1, 1e5)
h2V1z = r.TH2F("h2V1z","Area in NaI (Ch1) throughout run 4353;Entry;Peak amplitude [mV]", 100, 70000, 95000, 100, 20, 930)
h2V2z = r.TH2F("h2V2z","Area in smallNaI 1 (Ch2) throughout run 4353;Entry;Peak amplitude [mV]", 100, 70000, 95000, 100, 20, 930)
h2V3z = r.TH2F("h2V3z","Area in smallNaI 2 (Ch3) throughout run 4353;Entry;Peak amplitude [mV]", 100, 70000, 95000, 100, 20, 930)
h2V4z = r.TH2F("h2V3z","Area in LYSO (Ch4) throughout run 4353;Entry;Peak amplitude [mV]", 100, 70000, 95000, 100, 20, 930)






i=0



for entry in tree:
  tree.GetEntry(i)
  h2V1.Fill(i, tree.vMax_3046_1)
  h2V2.Fill(i, tree.vMax_3046_2)
  h2V3.Fill(i, tree.vMax_3046_3)
  h2V4.Fill(i, tree.vMax_3046_4)
  h2S1.Fill(i, tree.scaler_3046_1)
  h2S2.Fill(i, tree.scaler_3046_2)
  h2S3.Fill(i, tree.scaler_3046_3)
  h2S4.Fill(i, tree.scaler_3046_4)
  if i>= 70000 and i < 95000:
    h2V1z.Fill(i, tree.vMax_3046_1)
    h2V2z.Fill(i, tree.vMax_3046_2)
    h2V3z.Fill(i, tree.vMax_3046_3)
    h2V4z.Fill(i, tree.vMax_3046_4)
  if i%10000 == 0:
    print ("processed "+str(i)+" events...")
  i= i+1


can = r.TCanvas()
h2V1.Draw("colz")
can.SaveAs("Run4353Ch1AmpEntry.pdf")
h2V2.Draw("colz")
can.SaveAs("Run4353Ch2AmpEntry.pdf")
h2V3.Draw("colz")
can.SaveAs("Run4353Ch3AmpEntry.pdf")
h2V4.Draw("colz")
can.SaveAs("Run4353Ch4AmpEntry.pdf")

h2V1z.Draw("colz")
can.SaveAs("Run4353Ch1AmpEntryz.pdf")
h2V2z.Draw("colz")
can.SaveAs("Run4353Ch2AmpEntryz.pdf")
h2V3z.Draw("colz")
can.SaveAs("Run4353Ch3AmpEntryz.pdf")
h2V4z.Draw("colz")
can.SaveAs("Run4353Ch4AmpEntryz.pdf")
can.SetLogy(1)
h2S1.Draw("colz")
can.SaveAs("Run4353Ch1ScaleEntry.pdf")
h2S2.Draw("colz")
can.SaveAs("Run4353Ch2ScaleEntry.pdf")
h2S3.Draw("colz")
can.SaveAs("Run4353Ch3ScaleEntry.pdf")
h2S4.Draw("colz")
can.SaveAs("Run4353Ch4ScaleEntry.pdf")

leg = r.TLegend()
start = 80000
colors = [r.kBlue, r.kBlue+1,r.kBlue+2,r.kBlue+3,r.kBlue+4,r.kMagenta+4,r.kMagenta+3,r.kMagenta+2,r.kMagenta+1, r.kMagenta]
for i in range (10):
  tree.SetLineColor(colors[i])
  if i == 0:
    tree.Draw("vMax_3046_1","Entry$>"+str(start+i*1000)+"&&Entry$<"+str(start+(i+1)*1000),"APL")
  if i>0:
   tree.Draw("vMax_3046_1","Entry$>"+str(start+i*1000)+"&&Entry$<"+str(start+(i+1)*1000),"same")
   
    
can.BuildLegend()
can.SaveAs("Run3453Spectra.pdf")

# scatter plot/2d hist of the pulse height/area/hardware scalars vs event number

#check calibration before and after - get scale factor between two calibration spectra

#make projections of the amplitude v entry histogram




