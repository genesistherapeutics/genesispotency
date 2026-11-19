# Validation report

File `data/GenesisPotency-2026/data.parquet`, SHA-256 `b494807d2051af1b3d820d596c92b37a46962087539c4c9c933eddf7fa1c6df1`, 5,410,616 rows.

Every check below runs on every row unless stated, comparing the file with the training
data and the upstream ChEMBL 37 and BindingDB 2026-07 records. All passed.

- **Schema:** exact column names, order and types; the footer holds only release name, schema
  version, license, release counts and upstream versions, and the counts match the file.
- **Identity:** `row_id` dense in file order; assay contexts contiguous, dense, and each one maps
  to exactly one upstream assay on one target.
- **Membership:** exactly the public-source training rows, one row each.
- **Training data unchanged:** task, category, readout, label, relation, binary call and target
  sequence equal the training data on every row; every `smiles` is the training molecule
  (same InChIKey) in canonical form; `pX = label + 6`; `pX_is_clipped` exactly where the upstream
  pX exceeds 12; sequence MD5s recomputed.
- **Upstream records:** on every linked ChEMBL row, endpoint, relation, value, units, assay,
  document, DOI, assay description, molecule and origin equal ChEMBL 37; on every linked BindingDB
  row, value, relation, units, DOI, PMID, patent and origin equal the BindingDB record; every
  linked PubChem row has AID, CID and SIDs, and its accession is the assay's (where the assay
  names one); `source_smiles` equals the upstream SMILES on every linked row.
- **Ambiguous rows:** 2+ distinct candidate measurements; the row's own record ID and value
  columns are null.
- **Decoys:** every non-decoy column null, partner present, partner InChIKey recomputed.
- **Agent corrections:** flags match the curation record; compound IDs null on structure-corrected
  rows, including inside candidates.
- **Cross-references and duplicates:** `xref_source` recomputed on every row;
  `duplicate_of_row_id` set exactly on BindingDB rows whose ChEMBL activity is a ChEMBL row of the
  same task.
- **Text:** ID columns numeric or ChEMBL-formatted; no unexpected source names in any column.

## Benchmarks

Files `data/GenesisPotency-2026-benchmarks/ranking.parquet` (SHA-256 `3e8ac79aaac47ffc332d79009f882f1f12456e79cef5794c135665f57769bedf`, 1,454 rows) and `data/GenesisPotency-2026-benchmarks/hitid.parquet` (SHA-256 `7310e92cec28bd04e35f239829936c20eb62a616c75c7b7eb64014e462248bb2`, 9,364 rows).
All passed.

- **Inputs:** every input is the paper's evaluation data, identified by SHA-256.
- **Membership:** `ranking` holds OpenFE (873), FEP+4 (87) and OpenBind (494) observations;
  `hitid` holds the paper's seven hit-identification sets (9,364 compounds, 1,008 active).
  CASP16 (140) is rebuilt by the fetch script.
- **Labels:** every ranking label equals the paper's; every hit-ID label equals the paper's,
  joined one-to-one on set and stereo-aware InChIKey. CACHE #1 has 101 actives at Kd <= 150 uM;
  the 88 compounds it moves from active to inactive are the only calls that differ from the
  source.
- **Structures:** `smiles` and `inchikey` are recomputed from the deposited structure on every
  row and equal the paper's InChIKeys.
- **Training overlap:** target identity uses the paper's training-exclusion rule (identity >=
  0.90 over >= 50% coverage). A training target with one residue changed must be flagged and its
  reversed sequence must not; a training (compound, target) pair must be flagged. All did.
- **CASP16 fetch script:** run on the organizers' files, it rebuilds the 140 CASP16 rows with the
  same structures, InChIKeys and relations, and pX within 1e-9.
