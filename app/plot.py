import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def plot_neutrinos(spectrums, start, end):
    for reactor in spectrums.keys():
        spectrum = spectrums[reactor]
        label  = spectrum['energy_MeV'].tolist()
        index = np.arange(len(label))
        num_neutrinos = spectrum['neutrinos'].tolist()
        plt.bar(index, num_neutrinos, log=True)
        plt.xlabel('Energy level [MeV]', fontsize=15)
        plt.ylabel('No. anitneutrinos per MeV per second', fontsize=15)
        plt.xticks(index, label, fontsize=6, rotation=30)
        dates = start.strftime("%b %d, %Y") + ' to ' + end.strftime("%b %d, %Y")
        plt.title('Neutrino spectrum for ' + reactor + ' from ' + dates)
        plt.show()
