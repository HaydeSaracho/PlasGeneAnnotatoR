import os
import subprocess
import csv

def annotate_modules(query_faa, output_dir, sample_name, db_path="db/plasmid_marker_db.dmnd", min_identity=30):
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isfile(query_faa) or os.path.getsize(query_faa) == 0:
        raise ValueError(f"El archivo {query_faa} está vacío o no existe. Verifica la predicción de genes.")

    # Archivos de salida con nombre de muestra
    hits_file = os.path.join(output_dir, f"{sample_name}.annotations.tsv")
    summary_file = os.path.join(output_dir, f"{sample_name}.module_summary.tsv")

    # Archivo temporal sin encabezado
    temp_file = os.path.join(output_dir, "temp_hits.tsv")

    # Ejecutar DIAMOND
    cmd = [
        "diamond", "blastp",
        "-q", query_faa,
        "-d", db_path,
        "-o", temp_file,
        "-f", "6",
        "--evalue", "1e-5",
        "--id", str(min_identity),
        "--max-target-seqs", "1",
        "--threads", "4"
    ]

    print("🚀 Ejecutando DIAMOND...")
    subprocess.run(cmd, check=True)
    print("✅ DIAMOND finalizado.")

    # Agregar encabezado y sobrescribir en el archivo final
    with open(temp_file, "r") as infile, open(hits_file, "w") as outfile:
        outfile.write("query_id\tsubject_id\n")
        for line in infile:
            outfile.write(line)

    os.remove(temp_file)

    # Procesar resultados
    summary = {}
    with open(hits_file) as infile:
        next(infile)  # saltar encabezado
        reader = csv.reader(infile, delimiter="\t")
        for row in reader:
            subject_id = row[1]

            module_name = "unknown"
            gene_name = "unknown"
            try:
                parts = subject_id.split('|')
                for part in parts:
                    if part.startswith("module="):
                        module_name = part.split("=", 1)[1]
                    elif part.startswith("product="):
                        gene_name = part.split("=", 1)[1]
            except Exception as e:
                print(f"⚠️ Error parsing: {subject_id} → {e}")

            summary.setdefault(module_name, []).append(gene_name)

    # Guardar resumen
    with open(summary_file, "w") as outsum:
        outsum.write("Module\t#Hits\tGenes\n")
        for module, genes in summary.items():
            gene_list = ", ".join(genes)
            outsum.write(f"{module}\t{len(genes)}\t{gene_list}\n")

    print("🧾 Resumen por módulo generado:", summary_file)
    return hits_file, summary_file
