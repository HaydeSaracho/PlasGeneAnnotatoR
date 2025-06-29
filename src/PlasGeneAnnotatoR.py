import argparse
import os
from gene_prediction import run_prodigal
from module_annotation import annotate_modules

def main():
    parser = argparse.ArgumentParser(description="PlasGeneAnnotatoR - Anotación de genes plasmídicos por módulo funcional")
    parser.add_argument("-i", "--input", required=True, help="Archivo FASTA de secuencias (contigs plasmídicos)")
    parser.add_argument("-o", "--output", required=True, help="Directorio de salida")
    args = parser.parse_args()
    
    # Verificación del formato de archivo de entrada
    if not args.input.endswith(('.fa', '.fasta', '.fna')):
        parser.error("El archivo de entrada debe estar en formato FASTA (.fa, .fasta, .fna)")
    
    # Verificación de existencia del archivo de entrada
    if not os.path.isfile(args.input):
        parser.error(f"El archivo '{args.input}' no existe.")

    # Crear carpeta de salida
    os.makedirs(args.output, exist_ok=True)

    # Nombre base del input
    sample_name = os.path.splitext(os.path.basename(args.input))[0]

    print("🔍 Corriendo predicción de genes con Prodigal...")
    faa, ffn = run_prodigal(args.input, args.output, sample_name)
    print(f"✅ Genes predichos: {faa}")

    print("📡 Corriendo anotación funcional con DIAMOND...")
    hits_file, summary_file = annotate_modules(faa, args.output, sample_name)

    print("\n📁 Archivos generados:")
    print(f"  - Proteínas predichas (.faa): {faa}")
    print(f"  - Genes anotados (.tsv): {hits_file}")
    print(f"  - Resumen por módulo: {summary_file}")
    print("\n🎉 ¡Análisis completo!")

if __name__ == "__main__":
    main()
