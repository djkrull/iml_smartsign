# -*- coding: utf-8 -*-
"""
Automatisk filtrering av seminarier för SmartSign digital skyltning
- Filtrerar endast denna veckans seminarier (måndag-fredag)
- Tar bort passerade seminarier
- Extraherar talare från HTML-beskrivning
- Formaterar tid för snygg visning
"""

import pandas as pd
import re
from datetime import datetime, timedelta
from html import unescape

def extract_speaker(html_description):
    """
    Extraherar talare från HTML-beskrivning
    Letar efter <b>Speaker</b><br />Namn,Institution
    """
    if pd.isna(html_description) or not html_description:
        return ""

    # Ta bort HTML och unescape
    clean = unescape(str(html_description))

    # Leta efter Speaker-mönster
    # Format: <b>Speaker</b><br />\nNamn,Institution<br />
    pattern = r'<b>Speaker</b><br\s*/?>[\n\s]*([^<]+?)(?:<br|$)'
    match = re.search(pattern, clean, re.IGNORECASE | re.DOTALL)

    if match:
        speaker_line = match.group(1).strip()
        # Ta första raden om det finns flera
        speaker_line = speaker_line.split('\n')[0].strip()
        # Ta bort extra whitespace
        speaker_line = ' '.join(speaker_line.split())
        return speaker_line

    return ""

def format_time(timedelta_obj):
    """
    Konverterar '0 days 17:00:00' till '17:00'
    """
    if pd.isna(timedelta_obj):
        return ""

    # Konvertera till sekunder och sedan till timmar:minuter
    total_seconds = int(timedelta_obj.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

def clean_title(title):
    """
    Rensar titel från prefix som 'WS,'
    """
    if pd.isna(title):
        return ""

    title = str(title).strip()
    # Ta bort vanliga prefix
    title = re.sub(r'^(WS|Workshop|Seminar)[,:\s]+', '', title, flags=re.IGNORECASE)
    return title

def main():
    print("="*80)
    print("AUTOMATISK SEMINARIE-FILTRERING FOR SMARTSIGN")
    print("="*80)

    # Sökvägar
    excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"
    output_csv = r"C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv"

    print(f"\nLaser Excel: {excel_file}")

    try:
        # Läs Excel
        df = pd.read_excel(excel_file)
        print(f"Totalt antal seminarier i Excel: {len(df)}")

        # Konvertera datum
        df['Start date'] = pd.to_datetime(df['Start date'])
        df['End date'] = pd.to_datetime(df['End date'])

        # Beräkna denna vecka (måndag-fredag)
        today = datetime.now()
        # Hitta måndagen denna vecka
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        # Fredag samma vecka
        end_of_week = start_of_week + timedelta(days=4, hours=23, minutes=59, seconds=59)

        print(f"\nDenna vecka: {start_of_week.date()} till {end_of_week.date()}")
        print(f"Idag: {today.date()} kl {today.strftime('%H:%M')}")

        # Filtrera: Endast denna vecka OCH framtida OCH taggade med "website"
        df_filtered = df[
            (df['Start date'] >= start_of_week) &
            (df['Start date'] <= end_of_week) &
            (df['Start date'] >= today) &  # Endast framtida
            (df['Tag(s)'].str.contains('website', na=False))  # Endast "website"-taggade
        ].copy()

        print(f"\nSeminarier denna vecka (framtida, taggade med 'website'): {len(df_filtered)}")

        if len(df_filtered) == 0:
            print("\n[VARNING] Inga seminarier hittade for denna vecka!")
            print("          Skapar tom CSV-fil...")

        # Extrahera talare från Description
        print("\nExtraherar talare fran HTML-beskrivningar...")
        df_filtered['Speaker'] = df_filtered['Description'].apply(extract_speaker)

        # Formatera tid
        df_filtered['Time_Start'] = df_filtered['Start time'].apply(format_time)
        df_filtered['Time_End'] = df_filtered['End time'].apply(format_time)
        df_filtered['Time_Display'] = df_filtered['Time_Start'] + '-' + df_filtered['Time_End']

        # Rensa titel
        df_filtered['Title_Clean'] = df_filtered['Title'].apply(clean_title)

        # Formatera datum för visning (t.ex. "Måndag 1 sep")
        df_filtered['Date_Display'] = df_filtered['Start date'].dt.strftime('%A %d %b')

        # Sortera på datum och tid
        df_filtered = df_filtered.sort_values(['Start date', 'Start time'])

        # Skapa final CSV med endast relevanta kolumner
        output_df = df_filtered[[
            'Title',              # Original titel (för referens)
            'Title_Clean',        # Rensad titel
            'Speaker',            # Extraherad talare
            'Start date',         # Datum (för sortering)
            'Date_Display',       # Formaterat datum
            'Time_Display',       # Formaterad tid (HH:MM-HH:MM)
            'Room location'       # Plats
        ]].copy()

        # Byt namn för SmartSign
        output_df.columns = ['Title_Original', 'Title', 'Speaker', 'Date', 'Date_Formatted', 'Time', 'Location']

        # Spara som CSV
        output_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

        print(f"\n[OK] CSV skapad: {output_csv}")
        print(f"     Antal seminarier: {len(output_df)}")

        # Visa förhandsvisning
        if len(output_df) > 0:
            print("\n" + "="*80)
            print("FORHANDS VISNING AV FILTRERADE SEMINARIER:")
            print("="*80)
            for idx, row in output_df.head(10).iterrows():
                print(f"\n{row['Date_Formatted']} kl {row['Time']}")
                print(f"  Titel: {row['Title']}")
                print(f"  Talare: {row['Speaker']}")
                print(f"  Plats: {row['Location']}")

        print("\n" + "="*80)
        print("[KLART] Filen ar klar for SmartSign Sync!")
        print("="*80)

    except FileNotFoundError:
        print(f"\n[FEL] Excel-filen hittades inte: {excel_file}")
        print("       Kontrollera att filen finns pa korrekt plats.")
    except Exception as e:
        print(f"\n[FEL] Ett oväntat fel uppstod:")
        print(f"      {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
