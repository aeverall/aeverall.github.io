import pandas as pd, numpy as np
import selectionfunctions.cog_v as CoGV
import selectionfunctions.cog_ii as CoGII
from selectionfunctions.source import Source


################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################
################################################################################################################


# Real data treatment
# data reading:
data = pd.read_csv("data_test.csv")

# Load DR3 selection function
dr3_sf = CoGII.dr3_sf(version="modelAB",crowding=False)

# Load RVS selection function
rvs_sf = CoGV.subset_sf(map_fname="rvs_cogv.h5")

source = Source(
        data["l"],
        data["b"],
        photometry={'gaia_g':data["phot_g_mean_mag"],
                    'gaia_g_gaia_rp':data["phot_g_mean_mag"]-data["phot_rp_mean_mag"]},
        frame='galactic',
        unit='deg')
source = Source(
        data["l"],
        data["b"],
        photometry={'gaia_g':data["phot_g_mean_mag"],
                    'gaia_rp':data["phot_rp_mean_mag"]},
        frame='galactic',
        unit='deg')


# minimum probability filter:
Pmin = 0.1

probdr3 = pd.DataFrame(dr3_sf(source))
probRV  = pd.DataFrame(rvs_sf(source))
prob    = pd.DataFrame(probdr3*probRV)

Ndr3    = probdr3[probdr3[0] > Pmin].shape[0]
NRV     = probRV[probRV[0] > Pmin].shape[0]
N       = prob[prob[0] > Pmin].shape[0]

print(f"Number of object with probability > {Pmin} of being in EDR3: {Ndr3}")
print(f"Number of object with probability > {Pmin} of having DR2 RV: {NRV}")
print(f"Number of object with probability > {Pmin} of being in EDR3 and having DR2 RV: {N}")

print(f"Expected number of objects in EDR3: {np.sum(Ndr3)}")
print(f"Expected number of objects having DR2 RV: {np.sum(NRV)}")
print(f"Expected number of objects in EDR3 and having DR2 RV: {np.sum(N)}")
