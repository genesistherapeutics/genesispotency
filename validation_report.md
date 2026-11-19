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
