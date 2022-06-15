import ROOT as r
import LANLTB as LANL
import argparse


parser = argparse.ArgumentParser(description='convert .txt files from CAEN D5742')
parser.add_argument('-l', '--low', type=float, help='low value of time range in hours', default = '55')
parser.add_argument('-hi', '--high', type=float, help='high value of time range in hours', default = '68')
args = parser.parse_args()

low = args.low
high = args.high

dir = "./data/"
files = ["M1_041822-042222_DTLpwr.csv",
"M2_041822-042222_DTLpwr.csv",
"M3_041822-042222_DTLpwr.csv",
"M4_041822-042222_DTLpwr.csv",
]
filesw =["M1_041822-042222_PW.csv",
"M2_041822-042222_PW.csv",
"M3_041822-042222_PW.csv",
"M4_041822-042222_PW.csv"
]

runs =[
]
'''
outfile = open("startEnd.txt",'w')
for run in LANL.runs:
  N = run.split(".")[0].split("Run")[-1]
  path = "./data_wfm/"+run#LANL.runDir+run
  times = LANL.getStartEnd(path)
  print(run,times)
  outfile.write( str(N)+","+str(times[0]) + "," + str(times[1]) +"\n");
outfile.close()
'''
#run dates
#4307 - april 18
#4310-4320 - april 19
#4321-4343 - april 20
#4344-4356 - april 21
#4356-end  - april 22
tscale = 3600
g = []
det= ["NaI","smallNaI 1","smallNaI 2"]
m = r.TMultiGraph()
mw = r.TMultiGraph()
gw = []

t0 = 0
colors = [r.kRed+1, r.kOrange+2, r.kGreen+2, r.kBlue-1,r.kViolet-1]
leg = r.TLegend(0.15,0.6,0.3,0.85)
count = 0
for f in files:
  print ("reading file "+f)
  file = open(dir+f)
  lines = file.readlines()
  g.append(   r.TGraphErrors() )
  i = 0
  first = False
  for line in lines:
    if i==0:
        i=i+1
        first = True
        continue
    #parse date time info
    
    timedate=line.split(',')[0]
    date =timedate.split(' ')[0]
    day = int(date.split('-')[-1])
    time =timedate.split(' ')[1]
    hour = int(time.split(':')[0])
    min = int(time.split(':')[1])
    sec = int(time.split(':')[2].split('+')[0])
    t = day * 24*3600 + hour *3600 + min *60 + sec
    if count == 0 and first:
      t0 = t
      print (timedate)
      print("t0 = "+str(t0))
      first = False
    t = t-t0
    t= t/tscale
    power = line.split(',')[1]
    if power == '': continue
    power = float(power)
    if count ==0:  power = power/1000.
  #  if i%100==0:
     # print("Event "+str(i)+", time = "+str(hour)+":"+str(min)+":"+str(sec)+", power = "+str(power))
    g[count].SetPoint(i,t,power)
    i=i+1
  g[count].SetLineStyle(0)
  g[count].SetMarkerColor(colors[count])
  g[count].SetLineColor(colors[count])
  g[count].SetMarkerStyle(23)
  leg.AddEntry(g[count],"Module "+str(count+1))
  m.Add(g[count])
  count=count+1
l=[]

for i in range(1,5):
  l.append(r.TLine(86400*i/tscale, 0,86400*i/tscale, 2.7 ))
  l[i-1].SetLineStyle(10)
can = r.TCanvas("c1","c1",1200,600)
m.SetTitle("Maximum power of RF in LANSCE DTL modules;Time [hr]; Maximum RF power [MW]")
m.Draw("APL")
m.GetXaxis().SetLimits(low, high);
for i in range(4):
  l[i].Draw()
leg.Draw()
b=[]
t= []
t3 =[]
n = 0
with open('startEnd.txt','r') as f:
    lines = f.readlines()
    i=0
    for line in lines:
        run =  str(line.split(",")[0])
        t0 = 1650265200 #April 18, 2022 midnight unix timestamp
        t1 = (float( line.split(",")[1] ) - t0) /tscale
        t2 = (float( line.split(",")[2] ) - t0 )/tscale
        n= n+1
        print("t0: ",t0,"t1: ",t1,"t2: ",t2)
        can.cd()
        b.append( r.TBox(t1,0.01,t2, 2.7))
       # b[i].SetFillStyle(3001)
        b[i].SetFillColorAlpha(r.kGray,0.5)
        b[i].Draw("same")
        t.append(r.TPaveText(t1-0.1, 2.4,t1+0.1, 2.6 ))
        t[i].AddText(run)
        t3.append(t[i].GetLineWith(run))
        t[i].SetTextSize(0.02)
        t3[i].SetTextAngle(90)
        t[i].Draw("same")
        i=i+1
can.SaveAs("./plots/RFpower.pdf")
can.SaveAs("./plots/RFpower.C")

legw = r.TLegend(0.15,0.15,0.3,0.4)
count = 0
for f in filesw:
  print ("reading file "+f)
  file = open(dir+f)
  lines = file.readlines()
  gw.append(   r.TGraphErrors() )
  i = 0
  first = False
  for line in lines:
    if i==0:
        i=i+1
        first = True
        continue
    #parse date time info
    
    timedate=line.split(',')[0]
    date =timedate.split(' ')[0]
    day = int(date.split('-')[-1])
    time =timedate.split(' ')[1]
    hour = int(time.split(':')[0])
    min = int(time.split(':')[1])
    sec = int(time.split(':')[2].split('+')[0])
    t = day * 24*3600 + hour *3600 + min *60 + sec
    if count == 0 and first:
      t0 = t
      print (timedate)
      print("t0 = "+str(t0))
      first = False
    t = t-t0
    t= t/tscale
    width = line.split(',')[1]
    if width == '': continue
    width = float(width)
 #   if count ==0:  power = power/1000.
   # if i%100==0:
    #  print("Event "+str(i)+", time = "+str(hour)+":"+str(min)+":"+str(sec)+", width = "+str(width))
    gw[count].SetPoint(i,t,width)
    i=i+1
  gw[count].SetLineStyle(0)
  gw[count].SetMarkerColor(colors[count])
  gw[count].SetLineColor(colors[count])
  gw[count].SetMarkerStyle(23)
  legw.AddEntry(g[count],"Module "+str(count+1))
  mw.Add(gw[count])
  count=count+1

#plot the run times and numbers



l=[]
for i in range(1,5):
  l.append(r.TLine(86400*i/tscale, 0,86400*i/tscale, 1200 ))
  l[i-1].SetLineStyle(10)
canw = r.TCanvas("c1","c1",1200,600)
mw.SetTitle("Width of RF pulse in LANSCE DTL modules;Time [hr]; Pulse width [#mus]")
mw.GetXaxis().SetLimits(low, high);
mw.Draw("APL")
for i in range(4):
  l[i].Draw()
legw.Draw()
b=[]
t= []
t3 =[]
n = 0
with open('startEnd.txt','r') as f:
    lines = f.readlines()
    i=0
    for line in lines:
        run =  str(line.split(",")[0])
        t0 = 1650265200 #April 18, 2022 midnight unix timestamp
        t1 = (float( line.split(",")[1] ) - t0) /tscale
        t2 = (float( line.split(",")[2] ) - t0 )/tscale
        n= n+1
        print("t0: ",t0,"t1: ",t1,"t2: ",t2)
        canw.cd()
        b.append( r.TBox(t1,0,t2, 1200))
        #b[i].SetFillStyle(3001)
        b[i].SetFillColorAlpha(r.kGray,0.5)
        b[i].Draw("same")
        b[i].Draw("same")
        t.append(r.TPaveText(t1-0.1, 1000,t1+0.1, 1100 ))
        t[i].AddText(run)
        t3.append(t[i].GetLineWith(run))
        t[i].SetTextSize(0.02)
        t3[i].SetTextAngle(90)
        t[i].Draw("same")
        i=i+1






#b = r.TBox(t1,0,t2, 1200)
#b.Draw("same")
canw.SaveAs("./plots/RFwidth.pdf")
canw.SaveAs("./plots/RFwidth.C")



