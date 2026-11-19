# GenesisPotency-2026 data dictionary

Two configurations: the training data (`GenesisPotency-2026`, below) and the paper's public
evaluation sets (`GenesisPotency-2026-benchmarks`, [at the end](#benchmarks)).

The training data is one Parquet file, 49 columns, one row per training example. IDs are strings even when numeric.
**Null** means not applicable or not available; an **empty list** means known to be none.

## Identity

| Column | Type | Meaning |
|---|---|---|
| `row_id` | string | `GP26-` + 7 digits, dense in file order; stable within this version |
| `assay_context_id` | string | `GP26-A` + 6 digits: one upstream assay on one target. Regression and binary rows of the same assay share it; decoys carry the context they were added to |
| `category` | string | `pX` (potency), `active`, `inactive`, `synthetic_decoy` |
| `task` | string | `regression` or `classification` |
| `readout` | string | `IC50`, `Ki`, `Kd` for regression; `binary` for classification |

## Training data (exactly as trained)

| Column | Type | Meaning |
|---|---|---|
| `smiles` | string | RDKit canonical SMILES of the training molecule (one molecule whose canonical form does not round-trip keeps its training string) |
| `target_sequence` | string | Protein sequence used in training |
| `target_sequence_md5` | string | MD5 of `target_sequence`, to group identical targets |
| `label` | float | Regression only: `clip(pX − 6, −6, 6)` |
| `label_relation` | string | Regression only: `=`, `<`, `>`, `<=`, `>=`, **in pX sense** (upstream "IC50 > 10 µM" is `<` here) |
| `label_is_hit` | int8 | Classification only: 1 active, 0 inactive (all decoys are 0) |
| `pX` | float | Regression only: `label + 6` |
| `pX_is_clipped` | bool | Regression only: true on the 59 rows whose upstream pX was above 12 |

## Upstream measurement

| Column | Type | Meaning |
|---|---|---|
| `measurement_link` | string | `exact` (the training row is this upstream record), `unique_inferred` (one upstream record matches the training row's compound, assay, target and call), `ambiguous` (several measurements match; see candidates), `synthetic` (decoy) |
| `endpoint` | string | Upstream endpoint: `IC50`, `Ki`, `Kd`; `PubChem activity outcome` for PubChem. Null on ambiguous rows whose candidates differ in endpoint |
| `source_relation` | string | Upstream relation in the upstream unit's sense (ChEMBL `standard_relation`; BindingDB's `<`/`>` prefix, else `=`) |
| `source_value` | float | Upstream value (ChEMBL `standard_value`; BindingDB nM value) |
| `source_units` | string | Upstream units (`nM` for BindingDB) |
| `source_pX` | float | pX of the upstream value, before clipping |
| `source_smiles` | string | Upstream SMILES string, unmodified (ChEMBL `canonical_smiles`, BindingDB `Ligand SMILES`, PubChem `SMILES`) |
| `source_record_candidates` | list<struct> | Ambiguous rows only: the 2+ upstream measurements the row matches. Fields: `database`, `record_id_type`, `record_id`, `chembl_activity_id`, `chembl_molecule_id`, `bindingdb_monomer_id`, `pubchem_cid`, `endpoint`, `source_relation`, `source_value`, `source_units`, `document_doi`, `document_pmid`, `patent_number`, `origin`. One BindingDB record can appear several times with different endpoints |

## Provenance and identifiers

| Column | Type | Meaning |
|---|---|---|
| `retrieved_from` | string | `ChEMBL`, `BindingDB`, `PubChem`; null on decoys |
| `retrieved_release` | string | `ChEMBL 37`, `BindingDB 2026-07`, or `PubChem HTS bioassays retrieved Aug-Oct 2025` (a retrieval window, not a PubChem version) |
| `origin` | string | Who originally curated the record. ChEMBL rows: `literature`, `patent`, `deposited_dataset`, or `BindingDB` (ChEMBL's BindingDB patent source). BindingDB rows: `ChEMBL`, `patent`, `literature`, `PubChem`, `PDSP`, `D3R`, `CSAR`, `other`. PubChem rows: `PubChem` |
| `chembl_activity_id` | string | ChEMBL rows: own activity ID. BindingDB rows imported from ChEMBL: the matched ChEMBL 37 activity, when exactly one matches |
| `chembl_assay_id` | string | ChEMBL rows: assay ChEMBL ID |
| `chembl_document_id` | string | ChEMBL rows: document ChEMBL ID |
| `chembl_target_id` | string | ChEMBL rows: target ChEMBL ID |
| `chembl_molecule_id` | string | ChEMBL rows: own molecule ID. BindingDB rows: BindingDB's ChEMBL cross-reference when it names exactly one. Null on structure-corrected rows |
| `bindingdb_reactant_set_id` | string | BindingDB rows: reactant set (record) ID |
| `bindingdb_monomer_id` | string | BindingDB rows: ligand (monomer) ID. Null on structure-corrected rows |
| `pubchem_aid` | string | PubChem rows: assay ID. BindingDB rows: BindingDB's own PubChem deposition AID |
| `pubchem_cid` | string | PubChem compound ID (own or BindingDB cross-reference). Null on structure-corrected rows |
| `pubchem_sids` | list<string> | PubChem substance IDs; a PubChem row can have several SIDs for one CID (up to 9), all with the same outcome. Null on ambiguous PubChem rows |
| `xref_source` | list<string> | BindingDB rows: which of `chembl_activity_id`, `chembl_molecule_id`, `pubchem_aid`, `pubchem_cid`, `pubchem_sids` are cross-references rather than BindingDB's own IDs. Empty elsewhere |
| `target_accession` | string | Target protein accession: UniProt for ChEMBL (single-protein targets) and BindingDB (single-chain targets); the assay's accession for PubChem |
| `target_accession_namespace` | string | `uniprot` or `ncbi_protein`; null when there is no accession (multi-chain BindingDB targets, PubChem assays without one) |
| `document_doi`, `document_pmid`, `patent_number` | string | Source document, as upstream gives it |
| `assay_description` | string | ChEMBL assay description |
| `measurement_ph`, `measurement_temperature` | string | BindingDB measurement conditions, as BindingDB states them (some "C" temperatures are in kelvin) |
| `target_name`, `target_organism` | string | As upstream gives them (ChEMBL target, BindingDB target); null for PubChem |
| `duplicate_of_row_id` | string | BindingDB rows that are the same measurement and task as a ChEMBL row in this file: that row's `row_id`. Drop rows where this is set to keep one copy |

## Agent correction

| Column | Type | Meaning |
|---|---|---|
| `corrected_by_agent` | string | `label` (854 rows: value, relation or binary call corrected), `structure` (597 rows), or `none`. `none` does not mean the row was checked |

## Decoys

| Column | Type | Meaning |
|---|---|---|
| `decoy_partner_smiles` | string | Decoys only: canonical SMILES of the measured compound the decoy was property-matched to (its measurement may have been removed by curation) |
| `decoy_partner_inchikey` | string | Decoys only: its InChIKey (null for one partner with a dummy atom) |

## Benchmarks

`GenesisPotency-2026-benchmarks` has two splits with the same 33 columns:
`ranking` (`data/GenesisPotency-2026-benchmarks/ranking.parquet`, potency values) and `hitid`
(`hitid.parquet`, active/inactive calls). `benchmarks/fetch_casp16.py` writes the CASP16 rows
in the same columns.

| Column | Type | Meaning |
|---|---|---|
| `row_id` | string | `GP26-R` (ranking) or `GP26-H` (hit-ID) + 5 digits, dense; the CASP16 rows written by the fetch script follow the shipped ranking rows. Stable within this version |
| `benchmark` | string | The evaluation set the row belongs to, e.g. `openfe_jacs_set_tyk2`, `hitid_cache2_nsp13`. Score within a set |
| `benchmark_family` | string | `OpenFE`, `FEP+4`, `CASP16`, `OpenBind`, `CACHE`, `Docking screen` (AmpC, D4, σ2) |
| `task`, `category`, `readout` | string | As in the training data: `regression` / `pX` / `IC50`, `Ki`, `Kd`, or `unspecified` (OpenFE, whose tables give a pX without its endpoint); `classification` / `active` or `inactive` / `binary` |
| `smiles` | string | RDKit canonical SMILES of `source_smiles` |
| `inchikey` | string | Stereo-aware InChIKey of `source_smiles`; with `benchmark` it identifies a compound |
| `source_smiles` | string | The structure as the benchmark deposits it (CASP16: the organizers' string) |
| `model_input_smiles` | string | The protonation state the paper's models were given; null on CASP16 rows |
| `target_name` | string | Target as the benchmark names it |
| `target_sequence`, `target_sequence_md5` | string | Protein sequence the paper's models were given, and its MD5 |
| `label`, `label_relation`, `pX` | float, string, float | Regression only, as in the training data: `label = clip(pX − 6, −6, 6)`; relation in pX sense |
| `label_is_hit` | int8 | Hit-ID only: 1 active, 0 inactive, by `activity_definition` |
| `label_basis` | string | Where the label comes from: `benchmark_table_pX` (OpenFE, FEP+4: the pX listed in the Mattsson–Walters benchmark tables), `organizer_IC50` (CASP16: from the organizers' IC50), `reported_pKd` (OpenBind), `binary_call` (hit-ID) |
| `activity_definition` | string | Hit-ID only: what "active" means for this set; it differs between sets |
| `mae_eligible` | bool | OpenFE, FEP+4, CASP16: whether the paper used the row for absolute-error metrics (not for CASP16 autotaxin); null on OpenBind |
| `source_value`, `source_units` | float, string | Upstream concentration (molar) where the benchmark gives one: FEP+4 IC50/Ki, and the curated SPR Kd on CACHE #1 LRRK2 rows |
| `source_dg_kcal_mol` | float | Upstream binding free energy (OpenFE, FEP+4) |
| `source_label` | string | Hit-ID only: the call as the source states it, before any endpoint revision |
| `source_compound_id` | string | The benchmark's own compound ID (CACHE ID, ZINC ID, OpenBind crystal code, CASP16 ligand ID) |
| `measurement_id`, `measurement_source` | string | The source record and the file or page it came from (with commit or SHA-256 where available) |
| `energy_source` | string | OpenFE, FEP+4: the file the free energy came from |
| `reference` | string | Where to find and cite the set |
| `note` | string | Set-specific caveat (CACHE #1 endpoint revision, CACHE #4 hit definition, OpenBind surrogate) |
| `target_max_identity_in_training` | float | Highest sequence identity of this target to any training target (local alignment covering >= 50% of either sequence) |
| `target_in_training` | bool | Some training target has identity >= 0.90 to this one over an alignment covering >= 50% of either sequence (sequence rule only; accessions are not compared) |
| `pair_in_training` | bool | The same compound (InChIKey connectivity block, ignoring stereo and charge) was measured on such a training target |
