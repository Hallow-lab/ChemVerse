"""Molecule catalog for ChemVerse.

Each entry: (name, SMILES, category, short description).
Add your own rows here and they appear in the gallery automatically.
"""

CATEGORIES = [
    "Basic & Inorganic",
    "Hydrocarbons",
    "Alcohols, Acids & Carbonyls",
    "Aromatics",
    "Solvents & Industrial",
    "Drugs & Pharmaceuticals",
    "Biomolecules",
    "Natural Products & Flavours",
]

MOLECULES = [
    # ---------------- Basic & Inorganic ----------------
    ("Water", "O", "Basic & Inorganic", "Bent triangular molecule; the universal solvent of life."),
    ("Ammonia", "N", "Basic & Inorganic", "Trigonal pyramidal gas, a key industrial feedstock for fertilisers."),
    ("Carbon Dioxide", "O=C=O", "Basic & Inorganic", "Linear molecule (180 degree bond angle) produced by respiration and combustion."),
    ("Hydrogen Peroxide", "OO", "Basic & Inorganic", "Simple peroxide used as a bleach and antiseptic."),
    ("Hydrogen Sulfide", "S", "Basic & Inorganic", "Foul-smelling toxic gas, a bent molecule like water."),
    ("Sodium Chloride", "[Na+].[Cl-]", "Basic & Inorganic", "Table salt; an ionic compound written as two fragments in SMILES."),
    ("Ammonium Ion", "[NH4+]", "Basic & Inorganic", "Tetrahedral cation, a textbook SMILES example for charges."),
    ("Hydrocyanic Acid", "C#N", "Basic & Inorganic", "Hydrogen cyanide, a linear molecule with a C-N triple bond."),
    ("Sulfuric Acid", "OS(=O)(=O)O", "Basic & Inorganic", "Strong mineral acid, the most produced industrial chemical."),
    ("Nitric Acid", "O[N+](=O)[O-]", "Basic & Inorganic", "Strong oxidising acid used for fertilisers."),

    # ---------------- Hydrocarbons ----------------
    ("Methane", "C", "Hydrocarbons", "Simplest hydrocarbon; tetrahedral, bond angle 109.5 degrees."),
    ("Ethane", "CC", "Hydrocarbons", "Two-carbon alkane showing staggered and eclipsed conformations."),
    ("Propane", "CCC", "Hydrocarbons", "Three-carbon alkane used as LPG fuel."),
    ("Butane", "CCCC", "Hydrocarbons", "Classic example for anti and gauche torsion angles."),
    ("Cyclohexane", "C1CCCCC1", "Hydrocarbons", "Six-membered ring that adopts a strain-free chair shape."),
    ("Ethene", "C=C", "Hydrocarbons", "Ethylene, the simplest alkene (one sigma and one pi bond)."),
    ("Ethyne", "C#C", "Hydrocarbons", "Acetylene, the simplest alkyne with a C-C triple bond."),
    ("cis-2-Butene", "C/C=C\\C", "Hydrocarbons", "Geometrical (cis) isomer: methyl groups on the same side of the double bond."),
    ("trans-2-Butene", "C/C=C/C", "Hydrocarbons", "Geometrical (trans) isomer: methyl groups on opposite sides."),

    # ---------------- Alcohols, Acids & Carbonyls ----------------
    ("Methanol", "CO", "Alcohols, Acids & Carbonyls", "Simplest alcohol, a toxic solvent and fuel."),
    ("Ethanol", "CCO", "Alcohols, Acids & Carbonyls", "Common alcohol, C2H6O; isomer of dimethyl ether."),
    ("Dimethyl Ether", "COC", "Alcohols, Acids & Carbonyls", "Ether isomer of ethanol: same formula C2H6O, different connectivity."),
    ("Isopropanol", "CC(O)C", "Alcohols, Acids & Carbonyls", "Rubbing alcohol, a secondary alcohol and solvent."),
    ("Glycerol", "OCC(O)CO", "Alcohols, Acids & Carbonyls", "Triol that forms the backbone of fats."),
    ("Formaldehyde", "C=O", "Alcohols, Acids & Carbonyls", "Simplest aldehyde, used as a preservative."),
    ("Acetaldehyde", "CC=O", "Alcohols, Acids & Carbonyls", "Two-carbon aldehyde, an intermediate in ethanol metabolism."),
    ("Acetone", "CC(=O)C", "Alcohols, Acids & Carbonyls", "Simplest ketone; a classic SMILES example with branching."),
    ("Formic Acid", "OC=O", "Alcohols, Acids & Carbonyls", "Simplest carboxylic acid, found in ant venom."),
    ("Acetic Acid", "CC(=O)O", "Alcohols, Acids & Carbonyls", "Main component of vinegar, a carboxylic acid."),
    ("Lactic Acid", "CC(O)C(=O)O", "Alcohols, Acids & Carbonyls", "Hydroxy acid with one stereocentre, produced in muscles."),
    ("Citric Acid", "OC(=O)CC(O)(CC(=O)O)C(=O)O", "Alcohols, Acids & Carbonyls", "Tricarboxylic acid of citrus fruits and the Krebs cycle."),
    ("Urea", "NC(N)=O", "Alcohols, Acids & Carbonyls", "First organic compound synthesised from inorganic material."),

    # ---------------- Aromatics ----------------
    ("Benzene", "c1ccccc1", "Aromatics", "Prototype aromatic ring; all C-C bonds are 1.39 angstrom."),
    ("Toluene", "Cc1ccccc1", "Aromatics", "Methylbenzene, a common solvent."),
    ("Phenol", "Oc1ccccc1", "Aromatics", "Hydroxybenzene, weakly acidic aromatic alcohol."),
    ("Aniline", "Nc1ccccc1", "Aromatics", "Aminobenzene, a precursor of dyes and drugs."),
    ("Styrene", "C=Cc1ccccc1", "Aromatics", "Vinylbenzene, the monomer of polystyrene."),
    ("Benzoic Acid", "OC(=O)c1ccccc1", "Aromatics", "Simplest aromatic carboxylic acid, a food preservative."),
    ("Nitrobenzene", "[O-][N+](=O)c1ccccc1", "Aromatics", "Nitro-substituted benzene used to make aniline."),
    ("Naphthalene", "c1ccc2ccccc2c1", "Aromatics", "Two fused benzene rings, the moth-ball hydrocarbon."),
    ("Anthracene", "c1ccc2cc3ccccc3cc2c1", "Aromatics", "Three linearly fused benzene rings."),
    ("Pyridine", "c1ccncc1", "Aromatics", "Aromatic ring with one nitrogen; a basic heterocycle."),
    ("Dicloran", "Nc1c(Cl)cc(cc1Cl)[N+](=O)[O-]", "Aromatics", "2,6-dichloro-4-nitroaniline, an agricultural fungicide."),

    # ---------------- Solvents & Industrial ----------------
    ("Bromomethane", "CBr", "Solvents & Industrial", "Halomethane, a SMILES textbook example."),
    ("Chloroform", "ClC(Cl)Cl", "Solvents & Industrial", "Trichloromethane, a dense laboratory solvent."),
    ("Acetonitrile", "CC#N", "Solvents & Industrial", "Polar aprotic solvent common in HPLC."),
    ("DMSO", "CS(C)=O", "Solvents & Industrial", "Dimethyl sulfoxide, a strongly polar solvent."),
    ("Tetrahydrofuran", "C1CCOC1", "Solvents & Industrial", "Cyclic ether solvent."),
    ("Diethyl Ether", "CCOCC", "Solvents & Industrial", "Classic volatile ether solvent."),
    ("Ethyl Acetate", "CCOC(C)=O", "Solvents & Industrial", "Fruity-smelling ester solvent."),

    # ---------------- Drugs & Pharmaceuticals ----------------
    ("Aspirin", "CC(=O)Oc1ccccc1C(=O)O", "Drugs & Pharmaceuticals", "Acetylsalicylic acid; analgesic and anti-inflammatory."),
    ("Paracetamol", "CC(=O)Nc1ccc(O)cc1", "Drugs & Pharmaceuticals", "Acetaminophen, a widely used pain and fever reducer."),
    ("Ibuprofen", "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "Drugs & Pharmaceuticals", "Non-steroidal anti-inflammatory drug (NSAID)."),
    ("Naproxen", "COc1ccc2cc(ccc2c1)C(C)C(=O)O", "Drugs & Pharmaceuticals", "NSAID built on a naphthalene core."),
    ("Caffeine", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "Drugs & Pharmaceuticals", "Xanthine stimulant found in coffee and tea."),
    ("Nicotine", "CN1CCCC1c1cccnc1", "Drugs & Pharmaceuticals", "Pyridine alkaloid of the tobacco plant."),
    ("Metformin", "CN(C)C(=N)N=C(N)N", "Drugs & Pharmaceuticals", "First-line drug for type 2 diabetes."),
    ("Diazepam", "CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc12", "Drugs & Pharmaceuticals", "Benzodiazepine used as an anxiolytic."),
    ("Penicillin G", "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O", "Drugs & Pharmaceuticals", "Beta-lactam antibiotic."),
    ("Acenocoumarol", "CC(=O)CC(C1=C(C2=CC=CC=C2OC1=O)O)C3=CC=C(C=C3)[N+](=O)[O-]", "Drugs & Pharmaceuticals", "Coumarin-derived anticoagulant (vitamin K antagonist)."),
    ("Retinol", "CC1=C(C(C)(C)CCC1)C=CC(C)=CC=CC(C)=CCO", "Drugs & Pharmaceuticals", "Vitamin A, a conjugated polyene alcohol."),

    # ---------------- Biomolecules ----------------
    ("Glucose", "OCC1OC(O)C(O)C(O)C1O", "Biomolecules", "C6H12O6, the main energy sugar of cells (pyranose form)."),
    ("Fructose", "OCC1(O)OCC(O)C(O)C1O", "Biomolecules", "Fruit sugar, an isomer of glucose."),
    ("Sucrose", "OCC1OC(CO)(OC2OC(CO)C(O)C(O)C2O)C(O)C1O", "Biomolecules", "Table sugar, a glucose-fructose disaccharide."),
    ("Vitamin C", "OCC(O)C1OC(=O)C(O)=C1O", "Biomolecules", "Ascorbic acid, an antioxidant vitamin."),
    ("Glycine", "NCC(=O)O", "Biomolecules", "Simplest amino acid and the only achiral one."),
    ("Alanine", "CC(N)C(=O)O", "Biomolecules", "Small chiral amino acid."),
    ("Tryptophan", "NC(Cc1c[nH]c2ccccc12)C(=O)O", "Biomolecules", "Essential amino acid with an indole side chain."),
    ("Dopamine", "NCCc1ccc(O)c(O)c1", "Biomolecules", "Neurotransmitter linked to reward and movement."),
    ("Serotonin", "NCCc1c[nH]c2ccc(O)cc12", "Biomolecules", "Neurotransmitter that regulates mood."),
    ("Adrenaline", "CNCC(O)c1ccc(O)c(O)c1", "Biomolecules", "Epinephrine, the fight-or-flight hormone."),
    ("Adenine", "Nc1ncnc2[nH]cnc12", "Biomolecules", "Purine base of DNA and RNA."),
    ("Guanine", "NC1=NC2=C(N=CN2)C(=O)N1", "Biomolecules", "Purine base of DNA and RNA."),
    ("Cytosine", "NC1=NC(=O)NC=C1", "Biomolecules", "Pyrimidine base of DNA and RNA."),
    ("Thymine", "CC1=CNC(=O)NC1=O", "Biomolecules", "Pyrimidine base found in DNA."),
    ("Uracil", "O=c1cc[nH]c(=O)[nH]1", "Biomolecules", "Pyrimidine base found in RNA."),
    ("Cholesterol", "CC(C)CCCC(C)C1CCC2C1(CCC3C2CC=C4C3(CCC(C4)O)C)C", "Biomolecules", "Steroid lipid of animal cell membranes."),
    ("Testosterone", "CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34C", "Biomolecules", "Primary male sex hormone, a steroid."),

    # ---------------- Natural Products & Flavours ----------------
    ("Vanillin", "COc1cc(C=O)ccc1O", "Natural Products & Flavours", "Main flavour compound of vanilla."),
    ("Menthol", "CC(C)C1CCC(C)CC1O", "Natural Products & Flavours", "Cooling terpene alcohol from mint."),
    ("Capsaicin", "COc1cc(CNC(=O)CCCCC=CC(C)C)ccc1O", "Natural Products & Flavours", "The pungent compound of chilli peppers."),
    ("Limonene", "CC1=CCC(CC1)C(C)=C", "Natural Products & Flavours", "Citrus-scented terpene."),
    ("Eugenol", "COc1cc(CC=C)ccc1O", "Natural Products & Flavours", "Aromatic oil of cloves."),
]
