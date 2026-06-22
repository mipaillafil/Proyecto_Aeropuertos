import pandas as pd
from pathlib import Path

def obtener_datos():
    """Carga datos de operaciones desde el archivo CSV limpio"""
    csv_path = Path(__file__).parent.parent / "data" / "operaciones_aeropuertos_clean.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Procesar columnas de aeropuertos si existen
    aeropuertos_cols = [c for c in df.columns if c.startswith("aeropuerto_oaci_")]
    if aeropuertos_cols and "aeropuerto" not in df.columns:
        df["aeropuerto"] = (
            df[aeropuertos_cols]
            .idxmax(axis=1)
            .str.replace("aeropuerto_oaci_", "")
        )
    
    return df
