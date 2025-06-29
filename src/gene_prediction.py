import os
import subprocess

def run_prodigal(fasta_path, output_dir, sample_name):
    faa = os.path.join(output_dir, f"{sample_name}.proteins.faa")
    ffn = os.path.join(output_dir, f"{sample_name}.genes.ffn")

    print("🚀 Ejecutando Prodigal para predicción de ORFs...")

    cmd = [
        "prodigal",
        "-i", fasta_path,
        "-a", faa,
        "-d", ffn,
        "-p", "meta",   # modo metagenómico
        "-q"            # quiet mode (sin logs innecesarios)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Error en Prodigal:")
        print(result.stderr)
        return None, None

    print(f"✅ ORFs predichos guardados en:\n - Proteínas: {faa}\n - Nucleótidos: {ffn}")
    return faa, ffn
