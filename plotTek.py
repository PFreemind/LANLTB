import matplotlib.pyplot as plt
import numpy as np
import tekwfm as tek
import argparse
plt.ion() #why?

#make this for run number with argparse
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--run', type=str, default = "000")
args = parser.parse_args()
run = args.run
dir = "./"
prefix = "Tek"+run+"_004_ch"

for i in range(1,9):
    ans = tek.read_wfm(dir+prefix+str(i)+".wfm")
    vs = ans[0]
    ts = np.linspace( ans[1], ans[2], len(vs) )
    plt.figure()
    plt.plot(ts,vs)
    fig.SaveAs
plt.show()
input("press any key to close")
plt.close('all')
