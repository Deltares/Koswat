import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.ticker import MaxNLocator
import numpy as np
import json
import os
import warnings
import ipywidgets as widgets
from ipywidgets import interact, FloatSlider
from IPython.display import display


warnings.filterwarnings("ignore")

def plot_profile(filename, pad, scenarios):

    jsonfile = os.path.join(pad, f"{filename}.json")
    scenariofile = os.path.join(scenarios, f"{filename}.json")

    def profilepoints(jsonfile):
        # Open and load a JSON file
        with open(jsonfile, "r") as file:
            data = json.load(file)
        
        # Determine the reinforcement scenario
        with open(scenariofile, "r") as file:
            scenario = json.load(file)

        dh = scenario["scenario"]["dh"]
        ds = scenario["scenario"]["ds"]
        dp = scenario["scenario"]["dp"]
        
        Dijkprofiel = data["dijkprofiel"]
        y0 = Dijkprofiel["buiten_maaiveld"]
        y1 = Dijkprofiel["buiten_maaiveld"]
        y2 = Dijkprofiel["buiten_berm_hoogte"]
        y3 = Dijkprofiel["buiten_berm_hoogte"]
        y4 = Dijkprofiel["kruin_hoogte"]
        y5 = Dijkprofiel["kruin_hoogte"]
        y6 = Dijkprofiel["binnen_berm_hoogte"]
        y7 = Dijkprofiel["binnen_berm_hoogte"]
        y8 = Dijkprofiel["binnen_maaiveld"]
        y9 = Dijkprofiel["binnen_maaiveld"]
        
        # Binnendijks
        x4 = 0
        x5 = x4 + Dijkprofiel["kruin_breedte"]
        x6 = x5 + (y5-y6)*Dijkprofiel["binnen_talud"]
        x7 = x6 + Dijkprofiel["binnen_berm_lengte"]
        x8 = x7 + (y6-y8)*Dijkprofiel["binnen_talud"]
        x9 = x8 + dp + 10
        
        # Buitendijks
        x3 = x4 - (y4-y3)*Dijkprofiel["buiten_talud"]
        x2 = x3 - Dijkprofiel["buiten_berm_lengte"]
        x1 = x2 - (y2-y1)*Dijkprofiel["buiten_talud"]
        x0 = x1 - 5
        
        dike = np.array([[x0, y0], [x1, y1], [x2, y2], [x3, y3], [x4, y4], [x5, y5], [x6, y6], [x7, y7], [x8, y8], [x9, y9]])
        
        wx0 = x0
        wy0 = max(Dijkprofiel["kruin_hoogte"] - 0.5, Dijkprofiel["buiten_maaiveld"] + 0.1)
        wx1 = x4 - (y4-wy0)*Dijkprofiel["buiten_talud"]
        wy1 = wy0
        
        water = np.array([[wx0, wy0], [wx1, wy1]])
        ref = np.array([[0, y4 + 0.2], [0, min(y0,y9) - 5]])
        
        return dike, water, ref

    def jitter(values, scale=0.01):
        return values + np.random.normal(0, scale, size=len(values))

    def update_plot(dh, ds, dp):
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

        x_dh = [water_x[-1], water_x[-1]]
        y_dh = [water_y[-1], (water_y[-1] + dh)]

        x_ds = [dike_x[6], (dike_x[6] + ds)]
        y_ds = [(dike_y[9] - 0.5), (dike_y[9] - 0.5)]

        x_dp = [dike_x[8], (dike_x[8] + dp)]
        y_dp = [(dike_y[9] - 1.0), (dike_y[9] - 1.0)]

        
        fig, ax = plt.subplots(figsize=(8, 5))
            
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
        ax.fill_between(dike_line_x, dike_line_y, y2=min(dike_line_y)-5, color='#B7D167', alpha=0.2, hatch='\\\\\\\\')

        # Second plot, without xkcd
        ax.set_title(f"KOSWAT - Dijksectie: {filename} ", loc='left', pad=20)
        ax.set_ylabel("[m + NAP]", ha='right')
        ax.yaxis.set_label_coords(-0.06, 0.9)
        ax.set_xlabel("Afstand [m] -->", ha='right')
        ax.xaxis.set_label_coords(0.9, -0.12)

        ax.plot(x_dh, y_dh, color='red', linewidth=2, linestyle='--')
        ax.plot(x_ds, y_ds, color='red', linewidth=2, linestyle='--')
        ax.plot(x_dp, y_dp, color='red', linewidth=2, linestyle='--')    


        # Add text at the end of each line
        ax.text(x_dh[-1], y_dh[-1], r'$\Delta H$', va='bottom', ha='center')
        ax.text(x_ds[-1], y_ds[-1], r'$\Delta S$', va='center', ha='left')
        ax.text(x_dp[-1], y_dp[-1], r'$\Delta P$', va='center', ha='left')


        # Slightly jitter tick labels for natural look
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            dx, dy = np.random.uniform(-0.003, 0.003, 2)
            label.set_x(label.get_position()[0] + dx)
            label.set_y(label.get_position()[1] + dy)
                
        # --- Add text box with parameters ---
        # Format the dictionary into a readable multi-line string
        with open(jsonfile, "r") as file:
            data = json.load(file)
        Dijkprofiel = data["dijkprofiel"]
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
        y_labels = [y_dh[-1], y_ds[-1], y_dp[-1]]
        ymax_new = max(y_labels)

        current_ymin, current_ymax = ax.get_ylim()

        # Add a small offset
        offset = 0.05 * (current_ymax - current_ymin)
        ax.set_ylim(current_ymin, ymax_new + offset)            
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.show()
            # plt.savefig(jsonfile.replace(".json",".png"), bbox_inches="tight")
            # plt.close(fig)
    
        # Determine the reinforcement scenario
    with open(scenariofile, "r") as file:
        scenario = json.load(file)

    dh0 = scenario["scenario"]["dh"]
    ds0 = scenario["scenario"]["ds"]
    dp0 = scenario["scenario"]["dp"]

    print("Adjust ΔH, ΔS, ΔP interactively:")
    interact(
        update_plot,
        dh=FloatSlider(min=(0.5 * dh0), max=(2 * dh0), step=0.1, value=dh0, description="ΔH"),
        ds=FloatSlider(min=(0.5 * ds0), max=(2 * ds0), step=0.1, value=ds0, description="ΔS"),
        dp=FloatSlider(min=(0.5 * dp0), max=(2 * ds0), step=0.1, value=dp0, description="ΔP"),
    )

def kies_dijksectie(df, func, pad_profielen, pad_scenarios):
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
                func(change['new'], pad_profielen, pad_scenarios)

    dropdown.observe(on_change)

    display(dropdown, out)