import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import json
import os
import warnings
import ipywidgets as widgets
from IPython.display import display


warnings.filterwarnings("ignore")

def plot_profile(filename, pad):

    jsonfile = os.path.join(pad, f"{filename}.json")

    def profilepoints(jsonfile):
        # Open and load a JSON file
        with open(jsonfile, "r") as file:
            data = json.load(file)
        
        Dijkprofiel = data["Dijkprofiel"]
        y0 = Dijkprofiel["Buiten_Maaiveld"]
        y1 = Dijkprofiel["Buiten_Maaiveld"]
        y2 = Dijkprofiel["Buiten_Berm_Hoogte"]
        y3 = Dijkprofiel["Buiten_Berm_Hoogte"]
        y4 = Dijkprofiel["Kruin_Hoogte"]
        y5 = Dijkprofiel["Kruin_Hoogte"]
        y6 = Dijkprofiel["Binnen_Berm_Hoogte"]
        y7 = Dijkprofiel["Binnen_Berm_Hoogte"]
        y8 = Dijkprofiel["Binnen_Maaiveld"]
        y9 = Dijkprofiel["Binnen_Maaiveld"]
        
        # Binnendijks
        x4 = 0
        x5 = x4 + Dijkprofiel["Kruin_Breedte"]
        x6 = x5 + (y5-y6)*Dijkprofiel["Binnen_Talud"]
        x7 = x6 + Dijkprofiel["Binnen_Berm_Lengte"]
        x8 = x7 + (y6-y8)*Dijkprofiel["Binnen_Talud"]
        x9 = x8 + 5
        
        # Buitendijks
        x3 = x4 - (y4-y3)*Dijkprofiel["Buiten_Talud"]
        x2 = x3 - Dijkprofiel["Buiten_Berm_Lengte"]
        x1 = x2 - (y2-y1)*Dijkprofiel["Buiten_Talud"]
        x0 = x1 - 5
        
        dike = np.array([[x0, y0], [x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8], [x9, y9]])
        
        wx0 = x0
        wy0 = max(Dijkprofiel["Kruin_Hoogte"] - 0.5, Dijkprofiel["Buiten_Maaiveld"] + 0.1)
        wx1 = x4 - (y4-wy0)*Dijkprofiel["Buiten_Talud"]
        wy1 = wy0
        
        water = np.array([[wx0, wy0], [wx1, wy1]])
        ref = np.array([[0, y4 + 0.2], [0, min(y0,y9) - 5]])
        
        return dike, water, ref

    def jitter(values, scale=0.01):
        return values + np.random.normal(0, scale, size=len(values))


    # xkcd wobble amplitude
    randomness_level = 1

    dike, water, ref = profilepoints(jsonfile)
    dike_x, dike_y = dike.T
    water_x, water_y = water.T
    ref_x, ref_y = ref.T

    x = dike[:4, 0]
    x = np.append(x, water[1, 0])

    y_bottom = dike[:4, 1]
    y_bottom = np.append(y_bottom, water[1, 1])

    y_water = np.ones_like(y_bottom) * (water[1,1])

    with plt.xkcd(randomness=randomness_level):

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title(f"KOSWAT - Dijksectie: {filename} ", loc='left', pad=20)
        
        ymin, ymax = min(dike_y), max(dike_y)
        # margin = 0.2 * (ymax - ymin) * 0.2
        margin = 0.2 * (ymax - ymin if ymax != ymin else 1.0)
        ax.set_ylim(ymin - margin, ymax + margin)
        
        ax.set_ylabel("[m + NAP]", ha='right')
        ax.yaxis.set_label_coords(-0.06, 0.9)
        ax.set_xlabel("Afstand [m] -->", ha='right')
        ax.xaxis.set_label_coords(0.9, -0.12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
            
        # Jittered line
        dike_line_x = jitter(dike_x)
        dike_line_y = jitter(dike_y)
        water_line_x = jitter(water_x)
        water_line_y = jitter(water_y)
        ref_line_x = jitter(ref_x)
        ref_line_y = jitter(ref_y)
            
        ax.plot(water_line_x, water_line_y, color='#74B6D6', linewidth=3, label='Water')    
        ax.fill_between(x, y_water, y_bottom, color='#74B6D6', alpha=0.3)
        
        ax.plot(dike_line_x, dike_line_y, color='#B7D167', linewidth=2, label='Dijkprofiel')
        ax.plot(ref_line_x, ref_line_y, color='#CACCCA', linewidth=2, linestyle='--', label='Referentie')
        ax.plot(dike_line_x, dike_line_y, color='#38312c', linewidth=2, label='Dijkprofiel')    
        
        # ax.fill_between(dike_line_x, dike_line_y, y2=min(dike_line_y)-2, color='white')
        ax.fill_between(dike_line_x, dike_line_y, y2=min(dike_line_y)-2, color='#B7D167', alpha=0.2, hatch='\\\\\\\\')
        
        # Slightly jitter tick labels for natural look
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            dx, dy = np.random.uniform(-0.003, 0.003, 2)
            label.set_x(label.get_position()[0] + dx)
            label.set_y(label.get_position()[1] + dy)
                
        # --- Add text box with parameters ---
        # Format the dictionary into a readable multi-line string
        with open(jsonfile, "r") as file:
            data = json.load(file)
        Dijkprofiel = data["Dijkprofiel"]
        text_str = "\n".join([f"{key}: {value:.2f}" for key, value in Dijkprofiel.items()])

        # Place text box on the right side
        ax.text(
            1.05, 0.5, text_str,
            transform=ax.transAxes,
            fontsize=10,
            va="center",
            ha="left",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="whitesmoke", edgecolor="gray")
        )
                    
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.show()
        # plt.savefig(jsonfile.replace(".json",".png"), bbox_inches="tight")
        # plt.close(fig)


def kies_dijksectie(df, func, pad_profielen):
    # Create dropdown with Dijksectie values
    dropdown = widgets.Dropdown(
        options=sorted(df['Dijksectie'].unique()),
        description='Dijksectie:',
        layout=widgets.Layout(width='300px')
    )

    # Create an output area for the plot
    out = widgets.Output()

    def on_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            with out:
                out.clear_output(wait=True)  # 🧹 clear old plot
                plt.close('all')              # (optional) close any lingering figures
                func(change['new'], pad_profielen)

    dropdown.observe(on_change)

    display(dropdown, out)