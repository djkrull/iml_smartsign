# -*- coding: utf-8 -*-
"""
Automatisk filtrering av seminarier för SmartSign digital skyltning
- Filtrerar denna veckas seminarier (mån-fre), eller nästa veckas om idag är fre-söndag
- Tar bort passerade seminarier
- Extraherar talare från HTML-beskrivning
- Formaterar tid för snygg visning
"""

import pandas as pd
import re
from datetime import datetime, timedelta
from html import unescape
from pathlib import Path
import glob

def extract_speaker(html_description):
    """
    Extraherar talare från HTML-beskrivning
    Letar efter <b>Speaker</b> följt av namn och institution
    """
    if pd.isna(html_description) or not html_description:
        return ""

    clean = unescape(str(html_description))

    # Look for <b>Speaker</b> tag
    if '<b>Speaker</b>' in clean:
        start_idx = clean.find('<b>Speaker</b>') + len('<b>Speaker</b>')

        # Skip the first <br> tag (usually right after <b>Speaker</b>)
        br_idx = clean.find('<br', start_idx)
        if br_idx != -1:
            br_end = clean.find('>', br_idx)
            if br_end != -1:
                start_idx = br_end + 1

        # Find next <br> tag (end of speaker line)
        end_idx = clean.find('<br', start_idx)
        if end_idx == -1:
            end_idx = start_idx + 200

        speaker_text = clean[start_idx:end_idx].strip()
        # Remove remaining HTML tags
        speaker_text = re.sub(r'<[^>]+>', '', speaker_text).strip()
        # Take only first line (stop at newline before Abstract/etc)
        speaker_text = speaker_text.split('\n')[0].strip()
        # Clean up whitespace
        speaker_text = ' '.join(speaker_text.split())
        return speaker_text if speaker_text else ""

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

def find_latest_export_file():
    """
    Hittar den senaste ProgramExport*.xlsx filen i Downloads-mappen
    Returnerar sökvägen, eller None om ingen fil hittas
    """
    downloads_dir = Path(r"C:\Users\chrwah28.KVA\Downloads")

    # Leta efter alla ProgramExport*.xlsx filer
    pattern = downloads_dir / "ProgramExport*.xlsx"
    matching_files = list(downloads_dir.glob("ProgramExport*.xlsx"))

    if not matching_files:
        return None

    # Sortera efter senaste ändrad tid
    latest_file = max(matching_files, key=lambda p: p.stat().st_mtime)
    return latest_file

def main():
    print("="*80)
    print("AUTOMATISK SEMINARIE-FILTRERING FOR SMARTSIGN")
    print("="*80)

    # Hitta senaste ProgramExport*.xlsx fil
    excel_file = find_latest_export_file()

    if excel_file is None:
        print("\n[FEL] Ingen ProgramExport*.xlsx fil hittades i Downloads!")
        print("       Ladda ner en ny export från ProjectPlace och försök igen.")
        return

    output_csv = r"C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv"

    print(f"\nHittade senaste Excel-fil: {excel_file.name}")
    print(f"Ändrad: {datetime.fromtimestamp(excel_file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # Läs Excel
        df = pd.read_excel(excel_file)
        print(f"Totalt antal seminarier i Excel: {len(df)}")

        # Konvertera datum
        df['Start date'] = pd.to_datetime(df['Start date'])
        df['End date'] = pd.to_datetime(df['End date'])

        # Beräkna vilken vecka som ska visas (denna eller nästa)
        today = datetime.now()
        # Hitta måndagen denna vecka
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        # Om det är fredag-söndag (weekday 4-6), visa nästa veckans seminarier
        if today.weekday() >= 4:  # Friday or later
            start_of_week = start_of_week + timedelta(days=7)

        # Fredag samma vecka
        end_of_week = start_of_week + timedelta(days=4, hours=23, minutes=59, seconds=59)

        week_type = "nästa vecka" if today.weekday() >= 4 else "denna vecka"
        print(f"\nVecka att visa ({week_type}): {start_of_week.date()} till {end_of_week.date()}")
        print(f"Idag: {today.date()} kl {today.strftime('%H:%M')}")

        # Filtrera: Endast denna/nästa vecka OCH framtida OCH taggade med "website"
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
