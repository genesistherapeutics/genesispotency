# Notice and attribution

GenesisPotency-2026 is © 2026 Genesis Molecular AI, released under the Creative Commons
Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0,
https://creativecommons.org/licenses/by-sa/4.0/). It is an adaptation of the public databases
below. When you redistribute or adapt it, keep this notice, credit the sources and share your
adaptation under CC BY-SA 4.0.

The rows were filtered, transformed (units to pX, clipping, binary calls), corrected where an
automated agent found the upstream record to disagree with its source document, and joined
with identifiers from the other sources. Upstream values are kept unmodified in the `source_*`
columns.

## ChEMBL

ChEMBL release 37, EMBL-EBI, https://www.ebi.ac.uk/chembl/. Licensed under CC BY-SA 3.0
(https://creativecommons.org/licenses/by-sa/3.0/). Used for the ChEMBL rows, ChEMBL identifiers,
assay descriptions and target accessions, and for the ChEMBL cross-references on BindingDB rows.
Cite the current ChEMBL database paper: https://chembl.gitbook.io/chembl-interface-documentation/

## BindingDB

BindingDB, release 2026-07, https://www.bindingdb.org/. Data curated by BindingDB are licensed
under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); records BindingDB imported from
ChEMBL remain under ChEMBL's CC BY-SA 3.0. Used for the BindingDB rows and their identifiers and
measurement conditions. Cite the current BindingDB paper: https://www.bindingdb.org/

## PubChem

PubChem BioAssay, National Center for Biotechnology Information (NCBI),
https://pubchem.ncbi.nlm.nih.gov/, retrieved August-October 2025. Assay data are deposited by
many organisations; the depositor of each assay is listed on its AID page
(https://pubchem.ncbi.nlm.nih.gov/bioassay/<AID>). Used for the PubChem rows (AID, CID, SID,
outcome, SMILES, target accession). Cite the current PubChem paper:
https://pubchem.ncbi.nlm.nih.gov/docs/citation-guidelines

## UniProt

UniProt Knowledgebase, the UniProt Consortium, https://www.uniprot.org/. Licensed under CC BY 4.0.
Used for target accessions. Cite the current UniProt paper: https://www.uniprot.org/help/publications

## Benchmark sets (`GenesisPotency-2026-benchmarks`)

The benchmark tables adapt the public evaluation sets below. Each row's `reference` names its
source; cite the original work when you use a set.

- **OpenFE industry benchmark**, https://github.com/OpenFreeEnergy/IndustryBenchmarks2024
  (commit ff41e5ad0fda89b352341e3f6511bee25db0000a). MIT License, Copyright (c) 2024 Open Free
  Energy.
- **Schrödinger public binding free energy benchmark (FEP+)**,
  https://github.com/schrodinger/public_binding_free_energy_benchmark (commit
  a65d86b782a678c75388566ce00446e45283ee63). MIT License, Copyright (c) 2023 Gregory A. Ross.
- **Protein-ligand benchmark (PLB)**, https://github.com/openforcefield/protein-ligand-benchmark
  (commit fd88824f9114244f95a14b485e6d6c96c1de716d). MIT License, Copyright (c) 2019 David F. Hahn.
- **Benchmark labels as tabulated by Mattsson and Walters**,
  https://github.com/bamattsson/paper-identifying_and_addressing_data_leakage (commit
  7e6077bd36ca610b0e5d4d9814bbfab2ec874f7e). MIT License, Copyright (c) 2026 Björn Mattsson,
  W. Patrick Walters. The OpenFE and FEP+4 labels are taken from these tables.
- **OpenBind EV-A71 2A structure–affinity dataset**, OpenBind Consortium, Zenodo
  https://doi.org/10.5281/zenodo.20026661 (version 1, `OpenBind_EV-A71_2A.zip`), described in
  Nelen et al., https://doi.org/10.64898/2026.08.27.747600. Released under CC0 1.0 Universal.
- **CACHE Challenges #1–#4**, CACHE / Conscience, https://cache-challenge.org: hit-finding results
  for LRRK2 WD40 (#1, https://cache-challenge.org/results-cache-challenge-1,
  https://doi.org/10.1021/acs.jcim.4c01267), SARS-CoV-2 Nsp13 (#2,
  https://cache-challenge.org/node/2489, https://doi.org/10.1021/acs.jcim.5c00535), SARS-CoV-2
  Nsp3 Mac1 (#3, https://doi.org/10.1021/acs.jcim.5c02441) and CBL-B TKB (#4,
  https://cache-challenge.org/results-cache-challenge-4). See also Ackloo et al.,
  https://doi.org/10.1038/s41570-022-00363-z. CACHE states that challenge outputs are shared
  under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
- **Large-scale docking campaigns**: the compounds tested and their hit calls, from the
  supplementary data of Liu, F. et al., "The impact of library size and scale of testing on
  virtual screening", *Nature Chemical Biology* 21, 1039–1045 (2025),
  https://doi.org/10.1038/s41589-024-01797-w (AmpC); Lyu, J. et al., "Ultra-large library
  docking for discovering new chemotypes", *Nature* 566, 224–229 (2019),
  https://doi.org/10.1038/s41586-019-0917-9 (D4); and Alon, A. et al., "Structures of the σ2
  receptor enable docking for bioactive ligand discovery", *Nature* 600, 759–764 (2021),
  https://doi.org/10.1038/s41586-021-04175-x (σ2). Compound identifiers are ZINC IDs
  (https://zinc.docking.org). Cite these papers when you use the sets.
- **CASP16 pharma ligand affinities** (autotaxin and chymase, data provided by F. Hoffmann-La
  Roche AG), CASP16 Prediction Center, https://predictioncenter.org; assessment in Gilson et al.,
  https://doi.org/10.1002/prot.70061. The organizers' files state no licence; the
  structures and affinities are shared here with this attribution.
Changes made to the benchmark sets: rows were limited to the compounds the paper evaluates;
structures were canonicalised with RDKit and InChIKeys computed; potency values were expressed as
pX; for CACHE #1 the active call was redefined as curated Kd ≤ 150 µM (the original call is kept
in `source_label`); and columns describing overlap with the training data were added.

The MIT-licensed sources above are provided under these terms:

> Permission is hereby granted, free of charge, to any person obtaining a copy of this software
> and associated documentation files (the "Software"), to deal in the Software without
> restriction, including without limitation the rights to use, copy, modify, merge, publish,
> distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
> Software is furnished to do so, subject to the following conditions: The above copyright notice
> and this permission notice shall be included in all copies or substantial portions of the
> Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
> INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
> PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
> ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
> ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

## Software

Canonical SMILES and InChIKeys were computed with RDKit (BSD 3-Clause, https://www.rdkit.org/).
InChI and InChIKey are © IUPAC and the InChI Trust.
