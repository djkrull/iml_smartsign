# -*- coding: utf-8 -*-
import pandas as pd
import sys

# Läs Excel-filen
excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"

try:
    # Läs alla sheets
    excel_data = pd.ExcelFile(excel_file)
    print(f"Excel-fil: {excel_file}")
    print(f"Antal sheets: {len(excel_data.sheet_names)}")
    print(f"Sheet-namn: {excel_data.sheet_names}\n")

    # Läs första sheetet
    df = pd.read_excel(excel_file)

    print("="*80)
    print("STRUKTUR OCH DATA")
    print("="*80)

    # Visa info
    print(f"\nAntal rader: {len(df)}")
    print(f"Antal kolumner: {len(df.columns)}")

    # Visa kolumnnamn och datatyper
    print("\nKOLUMNER OCH DATATYPER:")
    print("-"*80)
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].count()
        print(f"  * {col:30} | Type: {str(dtype):15} | Values: {non_null}/{len(df)}")

    # Visa första 10 raderna
    print("\n" + "="*80)
    print("FORSTA 10 RADERNA:")
    print("="*80)
    print(df.head(10).to_string())

    # Visa unika värden för vissa kolumner om de finns
    print("\n" + "="*80)
    print("DATUMINTERVALL (om datum finns):")
    print("="*80)

    # Leta efter datumkolumner
    date_columns = [col for col in df.columns if 'date' in col.lower() or 'datum' in col.lower()]
    if date_columns:
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
                print(f"\n  {col}:")
                print(f"    Tidigaste: {df[col].min()}")
                print(f"    Senaste: {df[col].max()}")
            except:
                pass

    # Spara en preview som CSV för att se formatet
    preview_file = r"C:\Users\chrwah28.KVA\Development\smartsign\preview.csv"
    df.head(20).to_csv(preview_file, index=False, encoding='utf-8')
    print(f"\n[OK] Preview sparad som: {preview_file}")

except Exception as e:
    print(f"[FEL] Vid lasning av Excel-fil:")
    print(f"   {type(e).__name__}: {e}")
    sys.exit(1)
