import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob
import wepy.basics as we
# import wepy.loopeis as loop
import wepy.eis as weis
import pandas as pd
from impedance.models.circuits import CustomCircuit
from natsort import natsorted


time_start = 0.1
time_end = 19.1
points = 191

Times = np.linspace(time_start,time_end,points)
colors = we.get_colors(len(Times))


E = 1.46
plot = True

file = r"C:\Users\Herman\OneDrive - Univerzita Karlova\TRPEIS paper\TR-GEIS\trgeis_at_0,06A_for_20s_and_220s_OCV\trgeis_at_0,06A_for_20s_and_220s_OCV_GEIS.txt"
rows = []
df = we.read_file(file, skiprows = 0)
for j,t in enumerate(Times):
    Re_query = []
    Im_query= []
    I_query = []
    E_query = []
    freq_query = []
    t_query = np.full(len(np.unique(df['freq/Hz'])[1:]), t)
    # t_query = np.full(len(np.unique(df['Freq'])[1:]), t)
    # for f in np.unique(df['Freq'])[1:]:
    for f in np.unique(df['freq/Hz'])[1:]:
        Re = df.loc[(df["freq/Hz"] == f), 'Re(Z)/Ohm'].values
        Im = -df.loc[(df["freq/Hz"] == f), '-Im(Z)/Ohm'].values
        time = df.loc[(df["freq/Hz"] == f), 'time/s'].values
        I = df.loc[(df["freq/Hz"] == f), 'I/mA'].values
        E = df.loc[(df["freq/Hz"] == f), 'Ewe/V'].values
        freq = df.loc[(df["freq/Hz"] == f), 'freq/Hz'].values


        Re_query.append(np.interp(t, time-time[0], Re))
        Im_query.append(-np.interp(t, time-time[0], Im))
        I_query.append(np.interp(t, time-time[0], I))
        E_query.append(np.interp(t, time-time[0], E))
        freq_query.append(np.interp(t, time-time[0], freq))
  #  spectra.append([freq_query,np.array(Re_query) - 1j*np.array(Im_query),np.array(I_query),np.array(E_query)])
    rows.extend(
        (j+1, t, freq, re, im, current, potential)
        for freq, re, im, current, potential in zip(
            freq_query, Re_query, Im_query, I_query, E_query
        )
    )
    if plot:
        plt.plot(Re_query,np.array(Im_query),'-',c=colors[j])

output_file = os.path.splitext(file)[0] + "_spectra.txt"
pd.DataFrame(
    rows,
    columns=[
        "cycle number",
        "time/s",
        "freq/Hz",
        "Re(Z)/Ohm",
        "-Im(Z)/Ohm",
        "<I>/mA",
        "<Ewe>/V",
    ],
).to_csv(output_file, sep="\t", index=False)

if plot: 
    plt.xlim(0,0.3)
    plt.ylim(-0.1,0.3)
    plt.gca().set_aspect('equal')
    plt.show()
