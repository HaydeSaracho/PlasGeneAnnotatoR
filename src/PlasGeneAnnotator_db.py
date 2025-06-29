import os

try:
    import gdown
except ImportError:
    raise ImportError("El paquete 'gdown' no está instalado. Ejecutá: pip install gdown")

def download_from_drive(file_id, dest_path):
    """
    Descarga un archivo desde Google Drive si no existe en el destino.
    """
    url = f"https://drive.google.com/uc?id={file_id}"
    if not os.path.exists(dest_path):
        print(f"⬇️ Descargando {os.path.basename(dest_path)}...")
        gdown.download(url, dest_path, quiet=False)
    else:
        print(f"📁 {os.path.basename(dest_path)} ya existe. Descarga omitida.")

def main():
    os.makedirs("db", exist_ok=True)

    files = {
        "plasmid_marker_db.faa": "1VD-4FYBAlkdBJa4dllqkJveLIEYdtsi5",
        "plasmid_marker_db.dmnd": "1w7IDecP7sj_r3FAKPv6edF__CndQTizt"
    }

    print("📦 Iniciando descarga de base de datos de genes plasmídicos...\n")

    for filename, file_id in files.items():
        dest = os.path.join("db", filename)
        download_from_drive(file_id, dest)

    print("\n✅ Archivos descargados en la carpeta 'db/'.")

if __name__ == "__main__":
    main()
