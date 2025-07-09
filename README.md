# PlasGeneAnnotatoR

**PlasGeneAnnotatoR** is a bioinformatics tool for the functional annotation of genes in plasmid contigs.  
It predicts genes using **Prodigal**, and classifies them into functional modules (replication, mobility, stability, and adaptation) through fast similarity searches with **DIAMOND** against a curated reference database.

---

## Requirements

- Python 3.8+
- [DIAMOND](https://github.com/bbuchfink/diamond)
- [Prodigal](https://github.com/hyattpd/Prodigal)
- Biopython
- pandas
- gdown (for database download)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HaydeSaracho/PlasGeneAnnotatoR.git
cd PlasGeneAnnotatoR
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv env
.\env\Scripts\activate      # On Windows
source env/bin/activate     # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note:** 
Make sure you have DIAMOND and Prodigal installed and available in your $PATH.

4. Downloading the Reference Database
```bash
python src/PlasGeneAnnotatoR_db.py
```
---

## Usage
PlasGeneAnnotatoR requires a FASTA file with plasmid contigs as input.

```bash
python src/PlasGeneAnnotatoR.py -i <input_contigs.fasta> -o <output_directory>
```

### Arguments

| Parameter         | Description                                 |
|-------------------|---------------------------------------------|
| `-i`, `--input`   | FASTA file with plasmid contigs             |
| `-o`, `--output`  | Folder where the results will be saved      |

---

## Outputs

### Output files

| File                            | Description                                                        |
| ------------------------------- | -------------------------------------------------------------------|
| `sample_name.proteins.faa`      | Predicted protein sequences from input contigs (Prodigal output)   |
| `sample_name.genes.ffn`         | Nucleotide sequences of predicted genes (Prodigal output)          |
| `sample_name.annotations.tsv`   | DIAMOND matches with functional module annotations                 |
| `sample_name.module_summary.tsv`| Summary of modules, number of hits, and gene product names         |

> **Note:** 
Output file names use the input file basename as `sample_name`.

### File format `*.annotations.tsv`

| Field      | Description                                                         |
| ---------- | --------------------------------------------------------------------|
| query_id   | Identifier of predicted gene from `.faa`/`.ffn`                     |
| subject_id | Annotation info from DIAMOND: includes module and gene product info |

### File format `*.module_summary.tsv`

| Field     | Description                                                    |
| --------- | -------------------------------------------------------------- |
| Module    | Functional module name (e.g., replication, mobility)           |
| #Hits     | Number of hits assigned to that module                         |
| Genes     | Comma-separated list of gene product names within the module   |

> **Nota:** If no matches are found in the database, genes will be annotated as `unknown`.

---

## Example

```bash
# Run PlasGeneAnnotatoR using the following code to annotate and classify into functional modules (replication, motility, stability and adaptation) the plasmid proteins.
python src/PlasGeneAnnotatoR.py -i example/pBR322.fasta -o results/ 
```
