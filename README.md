# GenesisPotency-2026

> The data file (`data/GenesisPotency-2026/data.parquet`, 214,000,327 bytes, SHA-256 `b494807d2051af1b3d820d596c92b37a46962087539c4c9c933eddf7fa1c6df1`) is hosted on [Hugging Face](https://huggingface.co/datasets/genesisml/GenesisPotency).

GenesisPotency-2026 is the public-source part of the protein–ligand potency data used to train
the models in [the accompanying paper](#citation). Every row is a compound, a protein target and
either a potency value (pIC50, pKi, pKd) or an active/inactive call, exactly as the model saw it
in training, together with the upstream record it came from.

- Data: [huggingface.co/datasets/genesisml/GenesisPotency](https://huggingface.co/datasets/genesisml/GenesisPotency)
- Documentation and examples: [github.com/genesistherapeutics/genesispotency](https://github.com/genesistherapeutics/genesispotency)

- **5,410,616 rows** from ChEMBL 37, BindingDB (2026-07) and PubChem HTS bioassays.
- **1,773,271 potency measurements** and **3,637,345 binary calls**, including 200,662
  property-matched synthetic decoys.
- **1,038,258 compounds** and **3,640 protein sequences** across **69,939 assay contexts**.
- Each measured row links back to its upstream record: ChEMBL activity, BindingDB reactant set
  or PubChem AID/CID/SID, with the document, target accession and the value as published.
- 1,451 rows were **corrected by an LLM agent** that checked source documents, and are flagged.

## What is in it

| Source | Potency rows | Active | Inactive | Assay contexts | Compounds | Targets |
|---|---:|---:|---:|---:|---:|---:|
| ChEMBL 37 | 751,201 | 259,190 | 91,785 | 29,386 | 403,982 | 2,147 |
| BindingDB 2026-07 | 1,022,070 | 403,598 | 98,930 | 37,533 | 563,569 | 3,066 |
| PubChem HTS | – | 251,761 | 2,331,419 | 517 | 406,461 | 330 |
| Synthetic decoys | – | – | 200,662 | 2,503 decoy-only | 169,077 | – |
| **Total** | **1,773,271** | **914,549** | **2,722,796** | **69,939** | **1,038,258** | **3,640** |

Potency endpoints: IC50 1,148,723 rows, Ki 502,046, Kd 122,502. Targets are counted as distinct
sequences. Every context belongs to one source; decoys sit in the contexts of their source, and
2,503 contexts hold only decoys (see Decoys).

## How it was built

**Scope.** These are the public-source rows of the training set of the paper's potency models,
after removing targets that overlap the paper's evaluation benchmarks and applying a time split
(see the paper). It contains only rows from ChEMBL, BindingDB and PubChem, and no rows the
curation removed. Membership, labels and model inputs are frozen: this file is the training data,
not a re-derivation.

**Labels.** Regression rows carry `label = clip(pX − 6, −6, 6)`, where pX is −log10 of the molar
IC50, Ki or Kd; `pX = label + 6` is given too. `label_relation` is the training relation **in pX
sense**: an upstream "IC50 > 10 µM" becomes `pX < 5`. 59 regression rows had pX above 12 and were
clipped (`pX_is_clipped`). Classification rows carry `label_is_hit` (1 = active).

**Decoys.** Synthetic decoys are inactive (`label_is_hit = 0`) compounds added to an assay context
and property-matched to a measured compound of the same assay, given as `decoy_partner_smiles` and
`decoy_partner_inchikey`. Every decoy and every partner is a ChEMBL, BindingDB or PubChem compound.
Decoys were generated before curation, and curation later removed some measurements: 2,503
contexts (23,942 decoys) now hold only decoys, and 25,365 decoys have a partner whose
measurement in that assay is not in this file. They are kept because the model trained on them.
Decoys have no upstream record, so their measurement and provenance columns are null.

**Agent corrections.** An LLM agent read a sample of the source documents and checked compounds
and values against them. Where the source record was wrong, the training row was corrected:
854 labels (value, relation or binary call) and 597 structures. `corrected_by_agent` marks them. The upstream
value and structure stay in the `source_*` columns, so each correction is visible as a difference.
`corrected_by_agent = none` does **not** mean the row was checked: most rows were not.

**Structures.** `smiles` is RDKit's canonical SMILES of the training molecule. `source_smiles` is
the upstream string, unmodified; it differs in salts, charges or tautomers, and on structure-
corrected rows it is the upstream (wrong) structure. On structure-corrected rows the compound
identifiers (`chembl_molecule_id`, `pubchem_cid`, `pubchem_sids`, `bindingdb_monomer_id`) are null,
because the upstream ones name the uncorrected compound.
Every compound in the file, including decoys and their partners, is a ChEMBL, BindingDB or
PubChem compound. Where another database also records a compound, the published structure
matches a ChEMBL, BindingDB or PubChem structure (largest fragment, InChIKey connectivity); rows
whose structure could not be confirmed this way are not included.

**Identifiers.** All row and context IDs (`GP26-…`) are new and stable for this version. ChEMBL
target accessions come from ChEMBL's target table (single-protein targets). BindingDB records that
BindingDB imported from ChEMBL get the matching ChEMBL activity ID where exactly one ChEMBL 37
activity matches on document, compound, endpoint, relation, value and target (869,258 of the
900,697 such rows that have a single upstream record); `xref_source` lists which ID columns are such cross-references.

## Using it

Examples were tested with Polars 2.1.0. Install it with Hugging Face authentication
support, then run `hf auth login` once while the repository is private:

```bash
python -m pip install "polars==2.1.0" huggingface_hub
```

```python
import polars as pl

# The full file needs about 11 GB of memory; pass columns=[...] to load less.
df = pl.read_parquet("hf://datasets/genesisml/GenesisPotency@v1/data/GenesisPotency-2026/data.parquet")

potency = df.filter(pl.col("task") == "regression")                  # pIC50 / pKi / pKd
exact = potency.filter(pl.col("label_relation") == "=")              # drop censored values
dedup = df.filter(pl.col("duplicate_of_row_id").is_null())           # one copy per measurement
measured = df.filter(pl.col("category") != "synthetic_decoy")        # no decoys
```

See `examples/quickstart.py` and `DATA_DICTIONARY.md` for every column.

The Hugging Face configuration is `GenesisPotency-2026`; `v1` pins this release.
You can also stream rows with the `datasets` library (install with
`python -m pip install datasets`):

```python
from datasets import load_dataset

data = load_dataset(
    "genesisml/GenesisPotency",
    name="GenesisPotency-2026",
    revision="v1",
    token=True,  # Use your saved HF login while the repository is private.
    streaming=True,
)
rows = next(iter(data.values()))
first_row = next(iter(rows))
```

To download a local copy and run the quickstart:

```bash
hf download genesisml/GenesisPotency data/GenesisPotency-2026/data.parquet \
  --repo-type dataset --revision v1 --local-dir .
python examples/quickstart.py data/GenesisPotency-2026/data.parquet
```

- **Duplicates across sources.** BindingDB re-hosts much of ChEMBL. 504,807 BindingDB rows are the
  same measurement as a ChEMBL row in this file and point to it with `duplicate_of_row_id`; the
  model was trained on both copies. A further 30,961 BindingDB rows share a ChEMBL activity with a
  row of the other task; use `chembl_activity_id` to find them. Duplicate pairs can draw the
  compound differently (a few thousand pairs differ by tautomer, e.g. azo vs hydrazone, or by
  stereo only), and about 12,000 pairs carry different target sequences (often the same
  accession). Paired potency labels can differ by up to 0.02 from rounding.
- **Ambiguous rows.** 40,396 classification rows match two or more upstream measurements of the
  same compound in the same assay and target; usually their values differ, and one BindingDB
  record can contribute several endpoints. The measurements are listed in
  `source_record_candidates`; the row's own record and value columns are null, and other scalar
  columns are filled only where every candidate agrees.
- **Assay contexts** group one upstream assay on one target: a ChEMBL assay, a BindingDB deposition
  (its PubChem AID if it has one, otherwise its article or patent), or a PubChem AID. Regression
  and binary rows of the same assay share a context.
- **Origin.** `origin` says who originally curated the record. 933,074 BindingDB rows come from
  ChEMBL and 275,295 ChEMBL rows come from BindingDB's patent curation.

## Known limitations

- Recovered ChEMBL activity IDs on BindingDB rows are matched, not given: an independent audit of
  232 matches found 2 pointing at a different compound (about 1%).
- PubChem target accessions are mostly NCBI protein IDs (`target_accession_namespace`); PubChem
  rows have no target name or organism.
- BindingDB measurement conditions are given as BindingDB states them; some "°C" temperatures are
  in kelvin.
- Two training rows and one decoy partner contain a dummy atom (`*`); that partner has no InChIKey.
- Censored values are clipped into the label range in pX sense; 11 clipped rows turned
  "pX < 13" into "pX < 12".
- Binary calls, decoy generation and the time split follow the paper and are not re-derivable
  from this file alone.

## Licensing and attribution

GenesisPotency-2026 is released under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). It adapts data from ChEMBL
(CC BY-SA 3.0), BindingDB (CC BY 4.0 for BindingDB curation; ChEMBL-derived records CC BY-SA 3.0),
PubChem (deposited by many organisations; see each AID's depositor) and UniProt (CC BY 4.0, for
target accessions). See `NOTICE.md` for the attributions and citations you must keep when you
redistribute or adapt this dataset.

## Citation

If you use this dataset, cite the accompanying paper and the upstream sources listed in
`NOTICE.md`.

```bibtex
@misc{genesispotency2026,
  title  = {GenesisPotency-2026},
  author = {Genesis Therapeutics},
  year   = {2026},
  note   = {Citation to the accompanying paper to be added}
}
```

## Files and version

| File | Content |
|---|---|
| `data/GenesisPotency-2026/data.parquet` | The dataset (one file, zstd) |
| `DATA_DICTIONARY.md` | Every column: type, meaning, nulls |
| `examples/quickstart.py` | Loading, filtering, deduplication, candidates |
| `manifest.json` | Files, sizes, SHA-256, row counts |
| `validation_report.md` | Checks run on this file before release |
| `NOTICE.md`, `LICENSE` | Attribution, and the full CC BY-SA 4.0 license |

Release v1 (2026). Row and context IDs are stable within this version.
