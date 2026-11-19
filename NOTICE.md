# Notice and attribution

GenesisPotency-2026 is © 2026 Genesis Therapeutics, released under the Creative Commons
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

## Software

Canonical SMILES and InChIKeys were computed with RDKit (BSD 3-Clause, https://www.rdkit.org/).
InChI and InChIKey are © IUPAC and the InChI Trust.
