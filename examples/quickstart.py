"""GenesisPotency-2026 quickstart: load, filter, deduplicate, read candidates.

python -m pip install "polars==2.1.0" huggingface_hub
python examples/quickstart.py  # Downloads the pinned release; hf auth login if private.
python examples/quickstart.py data/GenesisPotency-2026/data.parquet
"""

import sys

import polars as pl

path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else "hf://datasets/genesisml/GenesisPotency@v2026.1/data/GenesisPotency-2026/data.parquet"
)
df = pl.read_parquet(path)
print(df.group_by("retrieved_from", "task").len().sort("retrieved_from", "task"))

# Potency regression: label = clip(pX - 6, -6, 6); label_relation is in pX sense.
potency = df.filter(pl.col("task") == "regression")
exact = potency.filter(pl.col("label_relation") == "=")
print("potency rows", potency.height, "uncensored", exact.height)

# One copy per upstream measurement: BindingDB re-hosts many ChEMBL measurements.
dedup = df.filter(pl.col("duplicate_of_row_id").is_null())
print("rows after dropping cross-source duplicates", dedup.height)

# Measured data only (no synthetic decoys), and one target's potency series.
measured = df.filter(pl.col("category") != "synthetic_decoy")
top_target = (
    potency.group_by("target_accession").len().drop_nulls().sort("len", descending=True)[0, 0]
)
series = potency.filter(pl.col("target_accession") == top_target).select(
    "smiles", "readout", "pX", "label_relation", "assay_context_id", "document_doi"
)
print(top_target, series.height, "rows")

# Rows the curation agent corrected: compare with the upstream value or structure.
corrected = df.filter(pl.col("corrected_by_agent") != "none").select(
    "row_id",
    "corrected_by_agent",
    "pX",
    "label_relation",
    "source_pX",
    "source_relation",
    "smiles",
    "source_smiles",
)
print(corrected.head())

# Ambiguous rows: several upstream records match; none is picked.
ambiguous = df.filter(pl.col("measurement_link") == "ambiguous")
print(
    ambiguous.select("row_id", "source_record_candidates")
    .explode("source_record_candidates")
    .unnest("source_record_candidates")
    .head()
)

# Decoys and the measured compound each was matched to.
print(
    df.filter(pl.col("category") == "synthetic_decoy")
    .select("assay_context_id", "smiles", "decoy_partner_smiles")
    .head()
)
