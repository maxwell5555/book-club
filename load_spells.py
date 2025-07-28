# load_spells.py
import pandas as pd

def load_spells_from_ods(path):
    df = pd.read_excel(path, engine='odf')

    # Define non-wizard columns
    non_wizard_columns = ['Level', 'School', 'Marks', 'Name', '# Known']

    # Identify wizard columns
    wizard_columns = [col for col in df.columns if col not in non_wizard_columns]

    records = []

    for _, row in df.iterrows():
        known_wizards = [wiz for wiz in wizard_columns if str(row[wiz]).strip() == wiz]
        spell = {
            'Spell': row['Name'],
            'Level': int(row['Level']) if not pd.isna(row['Level']) else '',
            'School': row['School'],
            'Wizards': known_wizards
        }
        records.append(spell)

    return records