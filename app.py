"""ChemVerse - an interactive molecule database.

Browse a catalog of molecules, then open any entry to see its 2D structure,
interactive 3D view, calculated properties, SMILES / InChI identifiers,
downloadable file formats and 3D geometry (bond lengths, angles, torsions).

Run with:  streamlit run app.py
"""

import base64
import json
import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski, rdMolDescriptors
from rdkit.Chem import rdMolTransforms as rdmt
from rdkit.Chem.Draw import rdMolDraw2D

from molecules import CATEGORIES, MOLECULES

# ----------------------------------------------------------------------------
# Page setup and styling
# ----------------------------------------------------------------------------
st.set_page_config(page_title="ChemVerse | Molecule Database", page_icon="🧬", layout="wide")

st.markdown(
    """
<style>
.block-container {padding-top: 1.4rem; max-width: 1250px;}
.hero {
  background: linear-gradient(120deg, #0f2a4a 0%, #1d5c8f 55%, #1f9d8a 100%);
  color: #fff; padding: 26px 32px; border-radius: 16px; margin-bottom: 18px;
}
.hero h1 {margin: 0; font-size: 2.1rem; color: #fff;}
.hero p {margin: 6px 0 0 0; font-size: 1.02rem; opacity: .92;}
.pill {
  display: inline-block; padding: 2px 12px; border-radius: 999px; font-size: .8rem;
  background: #e3f1fb; color: #0f4c81; margin-right: 6px; font-weight: 600;
}
.structbox {background: #fff; border: 1px solid #d8e2ec; border-radius: 12px; padding: 6px;}
.cardname {font-weight: 700; font-size: 1.02rem; margin: 4px 0 0 0;}
.cardmeta {font-size: .82rem; opacity: .75; margin-bottom: 6px;}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Catalog helpers
# ----------------------------------------------------------------------------


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


@st.cache_data(show_spinner=False)
def load_catalog() -> pd.DataFrame:
    rows = []
    for name, smiles, category, desc in MOLECULES:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            continue
        rows.append(
            {
                "slug": slugify(name),
                "name": name,
                "smiles": smiles,
                "category": category,
                "desc": desc,
                "formula": rdMolDescriptors.CalcMolFormula(mol),
                "mw": round(Descriptors.MolWt(mol), 2),
            }
        )
    return pd.DataFrame(rows)


CATALOG = load_catalog()


def get_entry(slug: str):
    """Return the catalog entry (dict) for a slug, or the user's custom SMILES entry."""
    if slug == "custom" and st.session_state.get("custom_entry"):
        return st.session_state["custom_entry"]
    hit = CATALOG[CATALOG["slug"] == slug]
    return None if hit.empty else hit.iloc[0].to_dict()


# ----------------------------------------------------------------------------
# Navigation (the open molecule lives in the URL: ?mol=aspirin)
# ----------------------------------------------------------------------------


def open_molecule(slug: str):
    st.query_params["mol"] = slug


def go_home():
    st.query_params.clear()


def open_custom():
    smi = st.session_state.get("custom_input", "").strip()
    mol = Chem.MolFromSmiles(smi) if smi else None
    if mol is None:
        st.session_state["custom_error"] = True
        return
    st.session_state["custom_error"] = False
    st.session_state["custom_entry"] = {
        "slug": "custom",
        "name": "Custom molecule",
        "smiles": smi,
        "category": "User input",
        "desc": "Structure generated from the SMILES you entered.",
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "mw": round(Descriptors.MolWt(mol), 2),
    }
    st.query_params["mol"] = "custom"


# ----------------------------------------------------------------------------
# 2D rendering
# ----------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def draw_svg(smiles: str, width: int, height: int, show_h: bool = False, show_idx: bool = False) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if show_h:
        mol = Chem.AddHs(mol)  # expanded structural formula
    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    opts = drawer.drawOptions()
    opts.addAtomIndices = show_idx
    opts.padding = 0.08
    drawer.DrawMolecule(mol)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()


def svg_img_tag(svg: str) -> str:
    """Embed SVG as a base64 data-URI <img>. Always encodes str -> bytes explicitly."""
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{b64}" style="width:100%;display:block;">'


# ----------------------------------------------------------------------------
# 3D generation, file formats and viewer
# ----------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def build_3d(smiles: str):
    """Embed and optimise a 3D conformer. Returns dict of file formats, or None."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    mh = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    status = AllChem.EmbedMolecule(mh, params)
    if status != 0:
        params.useRandomCoords = True
        status = AllChem.EmbedMolecule(mh, params)
    if status != 0:
        return None
    try:
        if AllChem.MMFFHasAllMoleculeParams(mh):
            AllChem.MMFFOptimizeMolecule(mh, maxIters=2000)
        else:
            AllChem.UFFOptimizeMolecule(mh, maxIters=2000)
    except Exception:
        pass
    molblock = Chem.MolToMolBlock(mh)
    return {
        "mol": molblock,
        "sdf": molblock + "$$$$\n",
        "pdb": Chem.MolToPDBBlock(mh),
        "xyz": Chem.MolToXYZBlock(mh),
    }


VIEWER_TEMPLATE = """
<div id="box" style="width:100%;height:__H__px;position:relative;border:1px solid #d8e2ec;border-radius:12px;overflow:hidden"></div>
<script src="https://3Dmol.org/build/3Dmol-min.js"></script>
<script>
(function () {
  var v = $3Dmol.createViewer(document.getElementById('box'), {backgroundColor: '__BG__'});
  v.addModel(__MOL__, 'sdf');
  v.setStyle({}, __STYLE__);
  __SURFACE__
  __LABELS__
  v.zoomTo();
  v.render();
  __SPIN__
})();
</script>
"""

STYLE_JS = {
    "Ball & stick": "{stick:{radius:0.15},sphere:{scale:0.28}}",
    "Stick": "{stick:{radius:0.2}}",
    "Space-filling": "{sphere:{scale:1.0}}",
    "Wireframe": "{line:{linewidth:2}}",
}


def viewer_html(molblock, style, spin, labels, surface, bg, height=520):
    surface_js = (
        "v.addSurface($3Dmol.SurfaceType.VDW, {opacity:0.6, color:'lightblue'});" if surface else ""
    )
    labels_js = (
        "v.getModel().selectedAtoms({}).forEach(function(a){ if(a.elem!=='H'){"
        "v.addLabel(a.elem+a.index,{position:a,fontSize:12,fontColor:'black',"
        "backgroundColor:'white',backgroundOpacity:0.55,showBackground:true});}});"
        if labels
        else ""
    )
    spin_js = "v.spin('y', 0.6);" if spin else ""
    return (
        VIEWER_TEMPLATE.replace("__H__", str(height))
        .replace("__BG__", bg)
        .replace("__MOL__", json.dumps(molblock))
        .replace("__STYLE__", STYLE_JS[style])
        .replace("__SURFACE__", surface_js)
        .replace("__LABELS__", labels_js)
        .replace("__SPIN__", spin_js)
    )


# ----------------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------------

PROP_MEANING = {
    "Molecular formula": "Types and numbers of atoms in one molecule.",
    "Molecular weight (g/mol)": "Average molecular mass.",
    "Exact mass (Da)": "Monoisotopic mass, useful for mass spectrometry.",
    "LogP (Crippen)": "Lipophilicity: preference for fat-like over water-like environments.",
    "Molar refractivity": "Molecular volume and polarisability.",
    "TPSA (A^2)": "Topological polar surface area from polar atoms.",
    "H-bond donors": "Sites that can donate a hydrogen bond.",
    "H-bond acceptors": "Sites that can accept a hydrogen bond.",
    "Rotatable bonds": "Bonds giving conformational flexibility.",
    "Rings": "Total number of rings.",
    "Aromatic rings": "Rings with delocalised pi-electrons.",
    "Heavy atoms": "Non-hydrogen atoms.",
    "Total atoms (with H)": "All atoms including hydrogens.",
    "Heavy-atom bonds": "Bonds in the hydrogen-suppressed graph.",
    "Sigma bonds": "One per bonded atom pair (hydrogens included).",
    "Pi bonds": "From double (1), triple (2) and aromatic (Kekule) bonds.",
    "Fraction Csp3": "Share of sp3 carbons; higher means more 3D/saturated.",
    "Formal charge": "Net charge of the structure.",
    "Stereocentres": "Atoms with possible chirality.",
}


@st.cache_data(show_spinner=False)
def compute_properties(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    mh = Chem.AddHs(mol)

    kek = Chem.Mol(mol)
    try:
        Chem.Kekulize(kek, clearAromaticFlags=True)
    except Exception:
        pass
    pi = int(sum(max(b.GetBondTypeAsDouble() - 1, 0) for b in kek.GetBonds()))

    mw = Descriptors.MolWt(mol)
    logp = Crippen.MolLogP(mol)
    hbd = Lipinski.NumHDonors(mol)
    hba = Lipinski.NumHAcceptors(mol)
    violations = sum([mw > 500, logp > 5, hbd > 5, hba > 10])
    centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False)

    props = {
        "Molecular formula": rdMolDescriptors.CalcMolFormula(mol),
        "Molecular weight (g/mol)": round(mw, 3),
        "Exact mass (Da)": round(Descriptors.ExactMolWt(mol), 4),
        "LogP (Crippen)": round(logp, 3),
        "Molar refractivity": round(Crippen.MolMR(mol), 3),
        "TPSA (A^2)": round(rdMolDescriptors.CalcTPSA(mol), 3),
        "H-bond donors": hbd,
        "H-bond acceptors": hba,
        "Rotatable bonds": Lipinski.NumRotatableBonds(mol),
        "Rings": Lipinski.RingCount(mol),
        "Aromatic rings": rdMolDescriptors.CalcNumAromaticRings(mol),
        "Heavy atoms": mol.GetNumHeavyAtoms(),
        "Total atoms (with H)": mh.GetNumAtoms(),
        "Heavy-atom bonds": mol.GetNumBonds(),
        "Sigma bonds": mh.GetNumBonds(),
        "Pi bonds": pi,
        "Fraction Csp3": round(rdMolDescriptors.CalcFractionCSP3(mol), 3),
        "Formal charge": Chem.GetFormalCharge(mol),
        "Stereocentres": len(centers),
    }
    return props, violations


@st.cache_data(show_spinner=False)
def identifiers(smiles: str):
    mol = Chem.MolFromSmiles(smiles)
    out = {
        "Input SMILES": smiles,
        "Canonical SMILES": Chem.MolToSmiles(mol, isomericSmiles=False),
        "Isomeric SMILES": Chem.MolToSmiles(mol, isomericSmiles=True),
    }
    try:
        out["InChI"] = Chem.MolToInchi(mol)
        out["InChIKey"] = Chem.MolToInchiKey(mol)
    except Exception:
        out["InChI"] = "unavailable in this RDKit build"
        out["InChIKey"] = "unavailable in this RDKit build"
    return out


# ----------------------------------------------------------------------------
# Geometry (bond lengths, angles, torsions) from the 3D structure
# ----------------------------------------------------------------------------

# Typical bond lengths in angstrom (reference table from the course slides).
TYPICAL = {
    ("H", "H", 1.0): 0.74, ("C", "H", 1.0): 1.09, ("C", "C", 1.0): 1.54,
    ("C", "C", 2.0): 1.34, ("C", "C", 3.0): 1.20, ("C", "O", 1.0): 1.43,
    ("C", "O", 2.0): 1.23, ("C", "N", 1.0): 1.47, ("C", "Cl", 1.0): 1.77,
    ("C", "C", 1.5): 1.39,
}


def tag(atom):
    return f"{atom.GetSymbol()}{atom.GetIdx()}"


@st.cache_data(show_spinner=False)
def geometry_tables(molblock: str):
    mol = Chem.MolFromMolBlock(molblock, removeHs=False)
    conf = mol.GetConformer()

    bonds = []
    for b in mol.GetBonds():
        a1, a2 = b.GetBeginAtom(), b.GetEndAtom()
        order = b.GetBondTypeAsDouble()
        key = tuple(sorted([a1.GetSymbol(), a2.GetSymbol()])) + (order,)
        typical = TYPICAL.get(key)
        bonds.append(
            {
                "Bond": f"{tag(a1)} - {tag(a2)}",
                "Order": order,
                "Length (A)": round(rdmt.GetBondLength(conf, a1.GetIdx(), a2.GetIdx()), 3),
                "Typical (A)": typical if typical is not None else "",
            }
        )

    angles = []
    for center in mol.GetAtoms():
        nbrs = [n.GetIdx() for n in center.GetNeighbors()]
        for i in range(len(nbrs)):
            for j in range(i + 1, len(nbrs)):
                angles.append(
                    {
                        "Angle": f"{tag(mol.GetAtomWithIdx(nbrs[i]))} - {tag(center)} - {tag(mol.GetAtomWithIdx(nbrs[j]))}",
                        "Degrees": round(rdmt.GetAngleDeg(conf, nbrs[i], center.GetIdx(), nbrs[j]), 1),
                    }
                )

    torsions = []
    for b in mol.GetBonds():
        bb, cc = b.GetBeginAtom(), b.GetEndAtom()
        a_opts = [n.GetIdx() for n in bb.GetNeighbors() if n.GetIdx() != cc.GetIdx()]
        d_opts = [n.GetIdx() for n in cc.GetNeighbors() if n.GetIdx() != bb.GetIdx()]
        if a_opts and d_opts and bb.GetDegree() > 1 and cc.GetDegree() > 1:
            a, d = a_opts[0], d_opts[0]
            torsions.append(
                {
                    "Torsion": f"{tag(mol.GetAtomWithIdx(a))} - {tag(bb)} - {tag(cc)} - {tag(mol.GetAtomWithIdx(d))}",
                    "Degrees": round(rdmt.GetDihedralDeg(conf, a, bb.GetIdx(), cc.GetIdx(), d), 1),
                }
            )
    return pd.DataFrame(bonds), pd.DataFrame(angles), pd.DataFrame(torsions)


# ----------------------------------------------------------------------------
# Gallery page
# ----------------------------------------------------------------------------


def render_gallery():
    st.markdown(
        """
<div class="hero">
  <h1>🧬 ChemVerse</h1>
  <p>A cheminformatics molecule database. Browse the collection, then open any molecule
  for its 2D structure, interactive 3D model, properties and SMILES.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([3, 2, 2])
    query = c1.text_input("Search", placeholder="Name, formula, category or SMILES (e.g. aspirin, C6H6, drug)")
    category = c2.selectbox("Category", ["All categories"] + CATEGORIES)
    sort_by = c3.selectbox("Sort by", ["Name (A-Z)", "Molecular weight (low-high)", "Molecular weight (high-low)"])

    df = CATALOG.copy()
    if category != "All categories":
        df = df[df["category"] == category]
    if query.strip():
        q = query.strip().lower()
        mask = (
            df["name"].str.lower().str.contains(q, regex=False)
            | df["formula"].str.lower().str.contains(q, regex=False)
            | df["category"].str.lower().str.contains(q, regex=False)
            | df["smiles"].str.lower().str.contains(q, regex=False)
        )
        df = df[mask]
    if sort_by == "Name (A-Z)":
        df = df.sort_values("name")
    elif sort_by.endswith("low-high)"):
        df = df.sort_values("mw")
    else:
        df = df.sort_values("mw", ascending=False)

    st.caption(f"Showing {len(df)} of {len(CATALOG)} molecules")
    if df.empty:
        st.info("No molecules match your search.")
        return

    cols_per_row = 4
    rows = [df.iloc[i : i + cols_per_row] for i in range(0, len(df), cols_per_row)]
    for chunk in rows:
        cols = st.columns(cols_per_row)
        for col, (_, m) in zip(cols, chunk.iterrows()):
            with col:
                with st.container(border=True):
                    svg = draw_svg(m["smiles"], 300, 220)
                    st.markdown(f'<div class="structbox">{svg_img_tag(svg)}</div>', unsafe_allow_html=True)
                    st.markdown(f'<p class="cardname">{m["name"]}</p>', unsafe_allow_html=True)
                    st.markdown(
                        f'<p class="cardmeta">{m["formula"]} · {m["mw"]} g/mol</p>',
                        unsafe_allow_html=True,
                    )
                    st.button(
                        "Open molecule",
                        key=f"open_{m['slug']}",
                        use_container_width=True,
                        on_click=open_molecule,
                        args=(m["slug"],),
                    )


# ----------------------------------------------------------------------------
# Molecule detail page
# ----------------------------------------------------------------------------


def render_detail(entry: dict):
    smiles = entry["smiles"]
    slug = entry["slug"]

    top_l, top_r = st.columns([1, 3])
    top_l.button("← All molecules", on_click=go_home)

    # previous / next navigation (catalog molecules only)
    if slug != "custom":
        names = list(CATALOG["slug"])
        i = names.index(slug)
        with top_r:
            p, n = st.columns(2)
            if i > 0:
                p.button("◀ " + CATALOG.iloc[i - 1]["name"], on_click=open_molecule, args=(names[i - 1],), key="prev")
            if i < len(names) - 1:
                n.button(CATALOG.iloc[i + 1]["name"] + " ▶", on_click=open_molecule, args=(names[i + 1],), key="next")

    st.markdown(
        f"""
<div class="hero">
  <h1>{entry['name']}</h1>
  <p><span class="pill">{entry['category']}</span> {entry['formula']} · {entry['mw']} g/mol</p>
  <p>{entry['desc']}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    props, violations = compute_properties(smiles)
    ids = identifiers(smiles)
    model3d = build_3d(smiles)

    t2d, t3d, tprop, tsmi, tgeo = st.tabs(
        ["🖼 2D Structure", "🧊 3D View", "📊 Properties", "🔤 SMILES & Identifiers", "📐 Geometry"]
    )

    # ---- 2D ----
    with t2d:
        c_left, c_right = st.columns([3, 1])
        with c_right:
            show_h = st.checkbox("Show all hydrogens (expanded formula)", key="h2d")
            show_idx = st.checkbox("Show atom indices", key="idx2d")
        svg = draw_svg(smiles, 700, 480, show_h, show_idx)
        with c_left:
            st.markdown(f'<div class="structbox">{svg_img_tag(svg)}</div>', unsafe_allow_html=True)
        c_right.download_button(
            "Download SVG",
            data=svg.encode("utf-8"),
            file_name=f"{slug}_2d.svg",
            mime="image/svg+xml",
        )
        st.caption(
            "Skeletal formula: carbon atoms sit at line ends and vertices, hydrogens on carbon are omitted, "
            "heteroatoms are labelled. Tick the box above to see the expanded structural formula."
        )

    # ---- 3D ----
    with t3d:
        if model3d is None:
            st.warning("A 3D conformer could not be generated for this structure.")
        else:
            c_view, c_ctl = st.columns([4, 1])
            with c_ctl:
                style = st.radio("Style", list(STYLE_JS.keys()), key="style3d")
                spin = st.checkbox("Auto-rotate", key="spin3d")
                labels = st.checkbox("Atom labels", key="lab3d")
                surface = st.checkbox("Van der Waals surface", key="surf3d")
                bg = st.selectbox("Background", ["white", "black", "#eef3f8"], key="bg3d")
            with c_view:
                components.html(
                    viewer_html(model3d["mol"], style, spin, labels, surface, bg),
                    height=540,
                )
            st.caption("Drag to rotate, scroll to zoom, right-drag (or two fingers) to pan. "
                       "Geometry is a force-field (MMFF94/UFF) optimised conformer.")

    # ---- Properties ----
    with tprop:
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Mol. weight", props["Molecular weight (g/mol)"])
        m2.metric("LogP", props["LogP (Crippen)"])
        m3.metric("TPSA", props["TPSA (A^2)"])
        m4.metric("H-bond donors", props["H-bond donors"])
        m5.metric("H-bond acceptors", props["H-bond acceptors"])

        if violations == 0:
            st.success("Lipinski rule of five: no violations (drug-like by this rule).")
        else:
            st.warning(f"Lipinski rule of five: {violations} violation(s).")

        table = pd.DataFrame(
            {
                "Property": list(props.keys()),
                "Value": [str(v) for v in props.values()],
                "Meaning": [PROP_MEANING.get(k, "") for k in props.keys()],
            }
        )
        st.dataframe(table, hide_index=True, use_container_width=True, height=min(740, 38 * len(table) + 40))
        st.download_button(
            "Download properties (CSV)",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name=f"{slug}_properties.csv",
            mime="text/csv",
        )

    # ---- SMILES & identifiers ----
    with tsmi:
        st.subheader("SMILES")
        st.caption("Click the copy icon at the top-right of a box to copy it.")
        st.markdown("**Canonical SMILES**")
        st.code(ids["Canonical SMILES"], language=None)
        if ids["Isomeric SMILES"] != ids["Canonical SMILES"]:
            st.markdown("**Isomeric SMILES (with stereochemistry)**")
            st.code(ids["Isomeric SMILES"], language=None)
        if ids["Input SMILES"] not in (ids["Canonical SMILES"], ids["Isomeric SMILES"]):
            st.markdown("**Catalog SMILES (as written)**")
            st.code(ids["Input SMILES"], language=None)

        st.subheader("InChI")
        st.markdown("**InChI**")
        st.code(ids["InChI"], language=None)
        st.markdown("**InChIKey**")
        st.code(ids["InChIKey"], language=None)

        st.subheader("Download structure files")
        if model3d is None:
            st.info("3D file formats are unavailable because no 3D structure could be generated.")
        else:
            d1, d2, d3, d4 = st.columns(4)
            d1.download_button("MOL (.mol)", model3d["mol"].encode("utf-8"), f"{slug}.mol", "chemical/x-mdl-molfile")
            d2.download_button("SDF (.sdf)", model3d["sdf"].encode("utf-8"), f"{slug}.sdf", "chemical/x-mdl-sdfile")
            d3.download_button("PDB (.pdb)", model3d["pdb"].encode("utf-8"), f"{slug}.pdb", "chemical/x-pdb")
            d4.download_button("XYZ (.xyz)", model3d["xyz"].encode("utf-8"), f"{slug}.xyz", "chemical/x-xyz")

    # ---- Geometry ----
    with tgeo:
        if model3d is None:
            st.info("Geometry needs a 3D structure, which could not be generated.")
        else:
            bonds, angles, torsions = geometry_tables(model3d["mol"])
            st.caption("Measured from the optimised 3D model. Atom labels are element symbol + atom index "
                       "(tick 'Show atom indices' on the 2D tab to match them).")
            g1, g2, g3 = st.columns(3)
            with g1:
                st.markdown(f"**Bond lengths** ({len(bonds)})")
                st.dataframe(bonds.astype({"Typical (A)": str}), hide_index=True, use_container_width=True, height=420)
            with g2:
                st.markdown(f"**Bond angles** ({len(angles)})")
                if angles.empty:
                    st.write("No angles (fewer than three bonded atoms).")
                else:
                    st.dataframe(angles, hide_index=True, use_container_width=True, height=420)
            with g3:
                st.markdown(f"**Torsion (dihedral) angles** ({len(torsions)})")
                if torsions.empty:
                    st.write("No torsions (needs four connected atoms).")
                else:
                    st.dataframe(torsions, hide_index=True, use_container_width=True, height=420)


# ----------------------------------------------------------------------------
# Sidebar and routing
# ----------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 🧬 ChemVerse")
    st.button("🏠 Browse all molecules", on_click=go_home, use_container_width=True)
    st.divider()
    st.markdown("**Open any SMILES**")
    st.text_input("SMILES", key="custom_input", placeholder="e.g. CC(=O)Oc1ccccc1C(=O)O", label_visibility="collapsed")
    st.button("Generate molecule page", on_click=open_custom, use_container_width=True)
    if st.session_state.get("custom_error"):
        st.error("That is not a valid SMILES string.")
    st.divider()
    st.caption(f"{len(CATALOG)} molecules in the catalog. Add more in molecules.py.")

selected = st.query_params.get("mol")
if selected:
    entry = get_entry(selected)
    if entry is None:
        st.error("Molecule not found.")
        st.button("← Back to all molecules", on_click=go_home)
    else:
        render_detail(entry)
else:
    render_gallery()
