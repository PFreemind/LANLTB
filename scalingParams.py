#script to check run1 4353 of the LANL test beam
###############################################
# scripting for quick analysis of the LANL test beam from April 15-22
# Patrick Freeman
# UCSB
# pmfreeman@ucsb.edu
###############################################
import ROOT as r
import argparse
import array
from datetime import datetime
#################################################################################################

#class LANL analysis (run?)


def getEnergy(ch, area):
    
    a = [7.78E-10, 1.07E-09,8.87E-10]
    b= [8.59E-04, 8.03E-04, 7.73E-04]
    c= [6.53E-01, 1.53E+00,1.21E+00]
    energy = area * area * a[ch] + area *b[ch] + c[ch]
    return energy

def compHists(h1, h2):
    sum =0
    nBins =h1.GetNbinsX()
    nBins2 =h2.GetNbinsX()
    if nBins != nBins2:
      print("Histograms have different numbers of bins!")
      return 0
      
    for i in range(nBins):
      x1 = h1.GetBinContent(i)
      x2 =  h2.GetBinContent(i)
      diff = h1.GetBinContent(i) - h2.GetBinContent(i)
      if x1+x2==0:continue
      sum = sum + pow(diff*diff,0.5)/(x1+x2)
    return sum
      


def getEMD( defaultRun = "Run4307.root", testRun = "Run4361.root", ch = 0, alpha= 1.0):

    #read the root files and get trees
    fD = r.TFile(defaultRun,"READ")
    fT = r.TFile(testRun,"READ")
    dTree = fD.Get("Events")
    tTree = fT.Get("Events")

    #fill histogram with cut on ch4 with LYSO
    hD = r.TH1F("hD","Default LYSO calibration compared to test;energy [keV];Entries", 100, 0, 500)
    hT = r.TH1F("hT","Test LYSO calibration compared to default;energy [keV];Entries", 100, 0, 500)

    area = []
    amp = []

    k=0
    for evt in dTree:
      dTree.GetEntry(k)
      amp.append(dTree.vMax_3046_1)
      amp.append(dTree.vMax_3046_2)
      amp.append(dTree.vMax_3046_3)
      area.append(dTree.area_3046_1)
      area.append(dTree.area_3046_2)
      area.append(dTree.area_3046_3)
      energy = getEnergy(ch, area[ch])
      if dTree.vMax_3046_4>20 and  energy>10 and amp[ch]<930: hD.Fill(energy)
      k= k+1
      area = []
      amp = []
    hD.Scale(1000/hD.GetEntries())
      
    k=0
    for evt in tTree:
      tTree.GetEntry(k)
      amp.append(tTree.vMax_3046_1)
      amp.append(tTree.vMax_3046_2)
      amp.append(tTree.vMax_3046_3)
      area.append(tTree.area_3046_1)
      area.append(tTree.area_3046_2)
      area.append(tTree.area_3046_3)
      energy = getEnergy(ch, area[ch])
      energy = energy *alpha
      if tTree.vMax_3046_4>20 and  energy>10 and amp[ch]<930: hT.Fill(energy)
      k= k+1
      area = []
      amp = []
  
    hT.Scale(1000/hT.GetEntries())
    '''
    can = r.TCanvas()
    hD.Draw()
    hT.SetLineColor(2)
    hT.Draw("same")
    can.SaveAs("./plots/calComp.pdf")
    '''

    EMD =  compHists(hT, hD)
    fT.Close()
    fD.Close()
    return EMD
        
       
def drawComp( defaultRun = "Run4307.root", testRun = "Run4361.root", ch = 0, alpha= 1.0):

    #read the root files and get trees
    fD = r.TFile(defaultRun,"READ")
    fT = r.TFile(testRun,"READ")
    dTree = fD.Get("Events")
    tTree = fT.Get("Events")

    #fill histogram with cut on ch4 with LYSO
    hD = r.TH1F("hD","Default LYSO calibration compared to test scaled by "+str(alpha)+";energy [keV];Entries", 100, 0, 500)
    hT = r.TH1F("hT","Test LYSO calibration compared to default;energy [keV];Entries", 100, 0, 500)

    area = []
    amp = []

    k=0
    for evt in dTree:
      dTree.GetEntry(k)
      amp.append(dTree.vMax_3046_1)
      amp.append(dTree.vMax_3046_2)
      amp.append(dTree.vMax_3046_3)
      area.append(dTree.area_3046_1)
      area.append(dTree.area_3046_2)
      area.append(dTree.area_3046_3)
      energy = getEnergy(ch, area[ch])
      if dTree.vMax_3046_4>20 and energy>10 and amp[ch]<930: hD.Fill(energy)
      k= k+1
      area = []
      amp = []
    hD.Scale(1000/hD.GetEntries())
      
    k=0
    for evt in tTree:
      tTree.GetEntry(k)
      amp.append(tTree.vMax_3046_1)
      amp.append(tTree.vMax_3046_2)
      amp.append(tTree.vMax_3046_3)
      area.append(tTree.area_3046_1)
      area.append(tTree.area_3046_2)
      area.append(tTree.area_3046_3)
      energy = getEnergy(ch, area[ch])
      energy = energy *alpha
      if tTree.vMax_3046_4>20 and energy>10 and amp[ch]<930: hT.Fill(energy)
      k= k+1
      area = []
      amp =[]
  
    hT.Scale(1000/hT.GetEntries())
    
    can = r.TCanvas()
    hD.Draw()
    hT.SetLineColor(2)
    hT.Draw("same")
    can.SaveAs("./plots/calComp_ch"+str(ch+1)+"_"+defaultRun.split("/")[-1].split(".")[0]+"_"+testRun.split("/")[-1].split(".")[0]+".pdf")
    

    return 0
        
##############################################################################################


start =  datetime.now()

minA=1.0
chs = [0,1,2]
#ch = 2

runDir = "./data/"
runs = [
"Run4307.root",
#"Run4313.root",
"Run4319.root",
"Run4320.root",
"Run4321.root",
"Run4322.root",
"Run4323.root",
"Run4324.root",
"Run4325.root",
"Run4326.root",
"Run4327.root",
"Run4328.root",
"Run4329.root",
"Run4330.root",
"Run4331.root",
"Run4332.root",
"Run4333.root",
"Run4334.root",
"Run4335.root",
"Run4336.root",
"Run4337.root",
"Run4338.root",
"Run4339.root",
"Run4340.root",
"Run4341.root",
"Run4342.root",
"Run4343.root",
"Run4344.root",
"Run4345.root",
"Run4346.root",
"Run4347.root",
"Run4348.root",
"Run4349.root",
"Run4350.root",
"Run4351.root",
"Run4352.root",
"Run4353.root",
"Run4354.root",
"Run4355.root",
"Run4356.root",
"Run4357.root",
"Run4358.root",
"Run4359.root",
"Run4360.root",
"Run4361.root",
"Run4362.root",
"Run4363.root",
"Run4364.root"
]


cal = "Run4226.root"
nPts = 50#int(5*1e1)
span = 0.15

for ch in chs:

    hA = r.TH1F("hA","Scaling parameters from LANL test beam;Scaling parameter;Entries", 40, 0.8,1.2)

    f = open("scalingParams_ch"+str(ch+1)+".txt",'w')
    f.write("Run,Scaling parameter,chi2\n")


    j=0
    for run in runs:
        testRun = runDir+run
        defaultRun= runDir+cal
        print("Getting scaling parameter for file "+testRun+" with calibration run "+str(defaultRun))
        minEMD =  getEMD( defaultRun,testRun, ch, 0.5)
        minA =0.5
        for i in range(nPts):
          #check scaling parameters
          alpha = 1 + float(i) / nPts *span
        #  print(alpha)
          EMD = getEMD(defaultRun,testRun, ch, alpha)
          if EMD < minEMD:
            minEMD = EMD
            minA = alpha
         # print(EMD)

          
        drawComp( defaultRun, testRun, ch, minA)

        print( "The scaling parameter is "+str(minA)+" for "+run +" with calibration from "+cal)
        hA.Fill(minA)
        f.write(testRun.split("/")[-1].split(".")[0]+","+str(minA)+","+str(minEMD)+"\n")
        j=j+1

    can = r.TCanvas()
    hA.Draw("")
    can.SaveAs("./plots/ScalingParams_ch"+str(ch+1)+".pdf")




stop =  datetime.now()

print ("start time: "+str(start))
print("end time: "+str(stop))
