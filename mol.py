# Analyzing Molecular Properties Dataset from PubChem

import pandas as pd
import requests
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns

#  Load the dataset
url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244,1983,702,6322,5957/property/MolecularWeight,LogP,InChIKey,CanonicalSMILES/CSV"
response = requests.get(url)
response.raise_for_status()  # Raise an error if the request failed
csv_data = StringIO(response.text)
df = pd.read_csv(csv_data)

# Inspect the data
print("=== Dataset Info ===")
print(df.info())
print("\n=== Missing Values ===")
print(df.isnull().sum())
print("\n=== First 5 Rows ===")
print(df.head())

#  Basic Data Cleaning
df_cleaned = df.dropna()
df_cleaned.rename(columns={
    "MolecularWeight": "MolWeight",
    "CanonicalSMILES": "SMILES"
}, inplace=True)

#  Visualization 1 - Molecular Weight vs LogP
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_cleaned, x="MolWeight", y="LogP")
plt.title("Molecular Weight vs LogP")
plt.xlabel("Molecular Weight")
plt.ylabel("LogP")
plt.grid(True)
plt.tight_layout()
plt.show()

# Visualization 2 - LogP by Compound (CID)
plt.figure(figsize=(10, 6))
sns.barplot(data=df_cleaned, x="CID", y="LogP")
plt.title("LogP Values for Selected Compounds")
plt.xlabel("Compound CID")
plt.ylabel("LogP")
plt.tight_layout()
plt.show()

#  Explanation
print("\n=== How Molecular Properties Support Solvent Selection ===")
print("""
In drug development, LogP (partition coefficient) is used to assess the hydrophilicity or lipophilicity of a compound.
- A high LogP indicates lipophilicity, which favors nonpolar solvents.
- A low or negative LogP suggests hydrophilicity, favoring polar solvents like water.

Molecular weight also affects solubility and permeability.
Analyzing these properties helps researchers select suitable solvents and optimize formulation for drug absorption and delivery.
""")
