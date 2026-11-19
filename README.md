<div align="center">
  <img src="assets/genesis-logo.png" width="88" alt="Genesis Molecular AI">
  <h1 align="center">GenesisPotency-2026</h1>
</div>

<div align="center">

**5.4 million public protein–ligand potency and activity measurements, with full upstream provenance.**

[Data on Hugging Face](https://huggingface.co/datasets/genesisml/GenesisPotency) ·
[Docs and examples on GitHub](https://github.com/genesistherapeutics/genesispotency) ·
[Genesis Molecular AI](https://genesis.ml)

</div>

GenesisPotency-2026 is the public-source part of the protein–ligand potency data that Genesis
Molecular AI used to train the potency models in the accompanying paper (see [Citation](#citation)).
Every row is a compound, a protein target and either a potency value (pIC50, pKi, pKd) or an
active/inactive call, exactly as used in training, together with the upstream record it came from.

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
(see the paper). It contains only rows from ChEMBL, BindingDB and PubChem; rows removed during
curation are not included. Rows, labels and model inputs are exactly as used in training; nothing
was re-derived for release.

**Labels.** Regression rows carry `label = clip(pX − 6, −6, 6)`, where pX is −log10 of the molar
IC50, Ki or Kd; `pX = label + 6` is given too. `label_relation` is the training relation **in pX
sense**: an upstream "IC50 > 10 µM" becomes `pX < 5`. 59 regression rows had pX above 12 and were
clipped (`pX_is_clipped`). Classification rows carry `label_is_hit` (1 = active).

**Decoys.** Synthetic decoys are inactive (`label_is_hit = 0`) compounds added to an assay context
and property-matched to a measured compound of the same assay, given as `decoy_partner_smiles` and
`decoy_partner_inchikey`. Every decoy and every partner is a ChEMBL, BindingDB or PubChem compound.
Decoys were generated before curation, and curation later removed some measurements: 2,503
contexts (23,942 decoys) now hold only decoys, and 25,365 decoys have a partner whose
measurement in that assay is not in this file. They are kept because they were part of the training data.
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

**Identifiers.** All row and context IDs (`GP26-…`, for GenesisPotency 2026) are new and stable
for this version. ChEMBL
target accessions come from ChEMBL's target table (single-protein targets). BindingDB records that
BindingDB imported from ChEMBL get the matching ChEMBL activity ID where exactly one ChEMBL 37
activity matches on document, compound, endpoint, relation, value and target (869,258 of the
900,697 such rows that have a single upstream record); `xref_source` lists which ID columns are such cross-references.

## Dataset structure

One Parquet file, one row per training example, 49 columns. The most used ones:

| Column | Meaning |
|---|---|
| `row_id`, `assay_context_id` | Row ID, and the upstream assay on one target the row belongs to |
| `smiles` | Canonical SMILES of the compound as trained |
| `target_sequence`, `target_accession` | Protein sequence as trained, and its UniProt or NCBI accession |
| `task`, `readout` | `regression` (`IC50`, `Ki`, `Kd`) or `classification` (`binary`) |
| `label`, `label_relation`, `pX` | Regression label `clip(pX − 6, −6, 6)`, its relation in pX sense, and pX |
| `label_is_hit` | Classification label: 1 active, 0 inactive |
| `category` | `pX`, `active`, `inactive` or `synthetic_decoy` |
| `retrieved_from`, `chembl_activity_id`, `bindingdb_reactant_set_id`, `pubchem_aid` | Upstream source and record |
| `source_value`, `source_units`, `source_relation`, `source_smiles` | The upstream measurement and structure, unmodified |
| `duplicate_of_row_id` | Set on BindingDB rows that repeat a ChEMBL row in this file |
| `corrected_by_agent` | `label`, `structure` or `none` |

[DATA_DICTIONARY.md](DATA_DICTIONARY.md) describes every column, its type and when it is null.
There is one configuration (`GenesisPotency-2026`) with a single `train` split; `v2026.1` is the
release tag.

## Using it

```bash
python -m pip install polars huggingface_hub   # examples tested with polars 2.1.0
```

```python
import polars as pl

# The full file needs about 11 GB of memory; pass columns=[...] to load less.
df = pl.read_parquet("hf://datasets/genesisml/GenesisPotency@v2026.1/data/GenesisPotency-2026/data.parquet")

potency = df.filter(pl.col("task") == "regression")                  # pIC50 / pKi / pKd
exact = potency.filter(pl.col("label_relation") == "=")              # drop censored values
dedup = df.filter(pl.col("duplicate_of_row_id").is_null())           # one copy per measurement
measured = df.filter(pl.col("category") != "synthetic_decoy")        # no decoys
```

Or stream rows with the `datasets` library:

```python
from datasets import load_dataset

ds = load_dataset("genesisml/GenesisPotency", split="train", revision="v2026.1", streaming=True)
print(next(iter(ds)))
```

To download a local copy and run the quickstart:

```bash
hf download genesisml/GenesisPotency data/GenesisPotency-2026/data.parquet \
  --repo-type dataset --revision v2026.1 --local-dir .
python examples/quickstart.py data/GenesisPotency-2026/data.parquet
```

[examples/quickstart.py](examples/quickstart.py) shows filtering, deduplication, agent-corrected
rows, ambiguous rows and decoys.

## Things to know before using it

- **Duplicates across sources.** BindingDB re-hosts much of ChEMBL. 504,807 BindingDB rows are the
  same measurement as a ChEMBL row in this file and point to it with `duplicate_of_row_id`; both
  copies were used in training. A further 30,961 BindingDB rows share a ChEMBL activity with a
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

## Intended use

Training and benchmarking machine-learning models of protein–ligand potency and activity, and
studying public bioactivity data and its provenance. Targets that overlap the paper's evaluation
benchmarks were removed, so the dataset is not a benchmark for those targets. It is not intended
for clinical or diagnostic decisions.

## Licensing and attribution

GenesisPotency-2026 is released under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). It adapts data from ChEMBL
(CC BY-SA 3.0), BindingDB (CC BY 4.0 for BindingDB curation; ChEMBL-derived records CC BY-SA 3.0),
PubChem (deposited by many organisations; see each AID's depositor) and UniProt (CC BY 4.0, for
target accessions). See [NOTICE.md](NOTICE.md) for the attributions and citations you must keep when you
redistribute or adapt this dataset.

## Citation

If you use this dataset, cite it and the upstream sources listed in [NOTICE.md](NOTICE.md). The
accompanying paper's reference will be added here when it is published.

```bibtex
@misc{genesispotency2026,
  title        = {{GenesisPotency-2026}: public protein--ligand potency data with upstream provenance},
  author       = {{Genesis Molecular AI}},
  year         = {2026},
  howpublished = {\url{https://huggingface.co/datasets/genesisml/GenesisPotency}},
  note         = {Release v2026.1}
}
```

## Contact

Questions and corrections: open an issue on
[GitHub](https://github.com/genesistherapeutics/genesispotency/issues) or a discussion in the
Hugging Face Community tab. For a data problem, include the `row_id`.

## Files and version

| File | Content |
|---|---|
| `data/GenesisPotency-2026/data.parquet` | The dataset (one file, zstd; on Hugging Face) |
| [DATA_DICTIONARY.md](DATA_DICTIONARY.md) | Every column: type, meaning, nulls |
| [examples/quickstart.py](examples/quickstart.py) | Loading, filtering, deduplication, candidates |
| [manifest.json](manifest.json) | Files, sizes, SHA-256, row counts |
| [validation_report.md](validation_report.md) | Checks run on this file before release |
| [NOTICE.md](NOTICE.md), [LICENSE](LICENSE) | Attribution, and the CC BY-SA 4.0 license |

Release v2026.1 (2026). Row and context IDs are stable within this version.
