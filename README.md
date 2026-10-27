# ChemVerse - interactive molecule database

Browse a catalog of 83 molecules and open any one for:

- 2D structure (skeletal, or expanded with all hydrogens) with SVG download
- Interactive 3D model (3Dmol.js): ball & stick, stick, space-filling, wireframe, labels, surface, auto-rotate
- Calculated properties (MW, LogP, TPSA, H-bond donors/acceptors, sigma/pi bonds, Lipinski check, ...)
- SMILES (canonical + isomeric), InChI, InChIKey
- Downloads: MOL, SDF, PDB, XYZ
- Geometry tables: bond lengths (with typical values), bond angles, torsion angles

You can also paste any SMILES in the sidebar to get a page for it.

## Run

    pip install -r requirements.txt
    streamlit run app.py

Add molecules by appending a tuple to `MOLECULES` in `molecules.py`.
The 3D viewer loads 3Dmol.js from 3Dmol.org, so it needs internet access in the browser.
