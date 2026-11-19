"""Rebuild the CASP16 rows of the GenesisPotency-2026 ranking benchmark.

The CASP16 organizers' affinity files state no licence, so this dataset ships only which
compounds and targets the benchmark uses (``benchmarks/ranking_casp16_membership.parquet``).
This script downloads the organizers' files, checks they are the exact files the paper used,
and restores the structures and labels in the same columns as ``ranking.parquet``.

    python -m pip install polars rdkit
    python benchmarks/fetch_casp16.py --out casp16.parquet

If predictioncenter.org is unreachable, download the two CSVs yourself and pass
``--source-dir``. Then combine the rows with the shipped ranking split::

    ranking = pl.read_parquet("data/GenesisPotency-2026-benchmarks/ranking.parquet")
    pl.concat([ranking, pl.read_parquet("casp16.parquet")])
"""

from __future__ import annotations

import argparse
import hashlib
import math
import urllib.request
from pathlib import Path

import polars as pl
from rdkit import Chem, RDLogger

RDLogger.DisableLog("rdApp.*")

BASE_URL = "https://predictioncenter.org/download_area/CASP16/targets/pharma_ligands/"

#: benchmark -> (file, SMILES column, IC50 column in uM, SHA-256 of the file the paper used)
FILES = {
    "casp16_autotaxin": (
        "L3000_exper_affinity.csv",
        "Structure",
        "IC50",
        "b9b5aec9342c127a5bbb27940aa86ae6cdbaf5d6bf1405600247514fd8ca5695",
    ),
    "casp16_chymase": (
        "L1000_exper_affinity.csv",
        "ligand_smiles",
        "CHYMASE_IC50_COLI_NH",
        "7e1bc9a39d05155884eaa1231bc24756f20bc5e52d85f34ab14277d1a334bfd3",
    ),
}
#: The autotaxin assay's upper limit: a compound at 10 uM is "IC50 >= 10 uM", i.e. pX < 5.
CEILING_UM = {"casp16_autotaxin": 10.0}

COLUMNS = [
    "row_id",
    "benchmark",
    "benchmark_family",
    "task",
    "category",
    "readout",
    "smiles",
    "inchikey",
    "source_smiles",
    "model_input_smiles",
    "target_name",
    "target_sequence",
    "target_sequence_md5",
    "label",
    "label_relation",
    "label_is_hit",
    "pX",
    "label_basis",
    "activity_definition",
    "mae_eligible",
    "source_value",
    "source_units",
    "source_dg_kcal_mol",
    "source_label",
    "source_compound_id",
    "measurement_id",
    "measurement_source",
    "energy_source",
    "reference",
    "note",
    "target_max_identity_in_training",
    "target_in_training",
    "pair_in_training",
]


def read_source(name: str, source_dir: Path | None) -> bytes:
    if source_dir is not None:
        payload = (source_dir / name).read_bytes()
    else:
        with urllib.request.urlopen(BASE_URL + name, timeout=60) as response:
            payload = response.read()
    digest = hashlib.sha256(payload).hexdigest()
    expected = next(sha for file, _, _, sha in FILES.values() if file == name)
    if digest != expected:
        raise SystemExit(
            f"{name}: SHA-256 {digest} is not the file the benchmark was built from ({expected}). "
            "The organizers may have changed it; the rebuilt rows would not match the paper."
        )
    return payload


def structure(smiles: str) -> tuple[str, str]:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise SystemExit(f"unparseable SMILES in the CASP16 file: {smiles!r}")
    return Chem.MolToSmiles(mol), Chem.MolToInchiKey(mol)


def labels(benchmark: str, source_dir: Path | None) -> pl.DataFrame:
    name, smiles_col, ic50_col, _ = FILES[benchmark]
    raw = pl.read_csv(read_source(name, source_dir), infer_schema=False)
    raw = raw.rename({c: c.lstrip("﻿") for c in raw.columns})
    ceiling = CEILING_UM.get(benchmark, math.inf)
    rows = []
    for compound_id, smiles, ic50 in raw.select("Target ID", smiles_col, ic50_col).iter_rows():
        value = float(ic50)
        if not value > 0:
            raise SystemExit(f"{name}: non-positive IC50 for {compound_id}")
        canonical, key = structure(smiles)
        rows.append(
            {
                "benchmark": benchmark,
                "source_compound_id": compound_id,
                "source_smiles": smiles,
                "smiles": canonical,
                "restored_inchikey": key,
                "pX": 6.0 - math.log10(value),
                "label_relation": "<" if value >= ceiling else "=",
            }
        )
    return pl.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--membership",
        type=Path,
        default=Path(__file__).with_name("ranking_casp16_membership.parquet"),
        help="the shipped membership file (default: next to this script)",
    )
    ap.add_argument(
        "--source-dir",
        type=Path,
        help="directory holding L1000_exper_affinity.csv and L3000_exper_affinity.csv, "
        "if you downloaded them yourself (default: download from predictioncenter.org)",
    )
    ap.add_argument("--out", type=Path, required=True, help="output Parquet file")
    args = ap.parse_args()

    membership = pl.read_parquet(args.membership)
    restored = pl.concat([labels(b, args.source_dir) for b in FILES])
    rows = membership.join(restored, on=["benchmark", "source_compound_id"], how="left")
    missing = rows.filter(pl.col("pX").is_null()).height
    if missing:
        raise SystemExit(f"{missing} benchmark compounds are absent from the CASP16 files")
    wrong = rows.filter(pl.col("restored_inchikey") != pl.col("inchikey")).height
    if wrong:
        raise SystemExit(f"{wrong} rebuilt structures differ from the benchmark's InChIKeys")
    rows = rows.with_columns(
        ((pl.col("pX") - 6).clip(-6, 6)).alias("label"),
        pl.lit(None, pl.String).alias("model_input_smiles"),
    ).drop("restored_inchikey")
    rows.select(COLUMNS).sort("row_id").write_parquet(args.out)
    print(f"wrote {rows.height} CASP16 rows to {args.out}")


if __name__ == "__main__":
    main()
