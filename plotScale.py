import ROOT as r

files = [
"./scalingParams_ch1.csv",
"./scalingParams_ch2.csv",
"./scalingParams_ch3.csv",
]

#run dates
#4307 - april 18
#4310-4320 - april 19
#4321-4343 - april 20
#4344-4356 - april 21
#4356-end  - april 22
g0 = r.TGraphErrors()
g1 = r.TGraphErrors()
g2 = r.TGraphErrors()
g = [g0,g1,g2]
det= ["NaI","smallNaI 1","smallNaI 2"]
m = r.TMultiGraph()

colors = [r.kRed+1, r.kBlue+2, r.kGreen+2]
leg = r.TLegend(0.15,0.6,0.45,0.85)
count = 0
for f in files:
  file = open(f, 'r')
  lines = file.readlines()
 

  i =0
  for line in lines:
    if i==0:
        i=i+1
        continue
    run = int(line.split(",")[0][-4:])
    scale = float(line.split(",")[1])
    chi2 =float(line.split(",")[2])
    print("run: "+str(run) +" scale: "+str(scale))
    g[count].SetPoint(i-1, run, scale)
   # g[count].SetPointError(i-1, 0,  chi2/100)
    i=i+1
    
  g[count].SetLineStyle(0)
  g[count].SetMarkerColor(colors[count])
  g[count].SetMarkerStyle(23)
  leg.AddEntry(g[count],"Channel "+str(count+1)+": "+det[count])
  m.Add(g[count])
  count=count+1
  
can = r.TCanvas()
m.SetTitle("Scaling factors for LYSO calibration at LANSCE test beam;Run number;Scaling factor")
m.Draw("APL")
leg.Draw()
can.SaveAs("./plots/ScaleVrun.pdf")
  
  
