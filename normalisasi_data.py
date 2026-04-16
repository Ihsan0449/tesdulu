from google.colab import files
import pandas as pd
import io

# ============================================================
# UPLOAD FILE
# ============================================================
print("Silakan upload file Excel (.xlsx) ...")
uploaded = files.upload()

file_name = list(uploaded.keys())[0]
df = pd.read_excel(io.BytesIO(uploaded[file_name]))
df.columns = df.columns.str.strip()
print(f"\nFile '{file_name}' berhasil dibaca — {len(df)} baris\n")

# ============================================================
# NORMALISASI MIN-MAX
# Rumus: (x - min) / (max - min)
# ============================================================
def normalisasi(kolom):
    return (kolom - kolom.min()) / (kolom.max() - kolom.min())

df['norm_iradiasi'] = normalisasi(df['Iradiasi'])
df['norm_suhu']     = normalisasi(df['Suhu'])
df['norm_daya']     = normalisasi(df['Daya Keluaran'])

# ============================================================
# BUAT LABEL TIMESTEP
# ============================================================
WINDOW = 5

def label_timestep(i):
    rel = i - WINDOW
    if rel < 0:    return f't-{abs(rel)}'
    elif rel == 0: return 't'
    else:          return f't+{rel}'

df['Timestep'] = [label_timestep(i) for i in range(len(df))]

df_out = df[['Timestep',
             'Iradiasi', 'norm_iradiasi',
             'Suhu',     'norm_suhu',
             'Daya Keluaran', 'norm_daya']].copy()
df_out.columns = ['Timestep',
                  'iradiasi', 'norm_iradiasi',
                  'suhu',     'norm_suhu',
                  'daya',     'norm_daya']

# ============================================================
# SPLIT 70% TRAINING — 30% TESTING
# ============================================================
total   = len(df_out)
n_train = int(total * 0.7)
n_test  = total - n_train

df_train = df_out.iloc[:n_train].reset_index(drop=True)
df_test  = df_out.iloc[n_train:].reset_index(drop=True)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.float_format', '{:.4f}'.format)

# ============================================================
# TAMPILKAN TRAINING & TESTING BERDAMPINGAN
# ============================================================
print("=" * 70)
print(f"TOTAL DATA   : {total} baris")
print(f"TRAINING 70% : {n_train} baris  ({df_train['Timestep'].iloc[0]} s/d {df_train['Timestep'].iloc[-1]})")
print(f"TESTING  30% : {n_test} baris   ({df_test['Timestep'].iloc[0]} s/d {df_test['Timestep'].iloc[-1]})")
print("=" * 70)

PREVIEW = 5

for df_tampil, label in [(df_train, f"TRAINING 70% — {n_train} baris"),
                          (df_test,  f"TESTING  30% — {n_test} baris")]:
    print(f"\n{'─' * 70}")
    print(f"  {label}")
    print(f"{'─' * 70}")
    print(f"\n  [ {PREVIEW} baris pertama ]")
    print(df_tampil.head(PREVIEW).to_string(index=False))
    print(f"\n  [ {PREVIEW} baris terakhir ]")
    print(df_tampil.tail(PREVIEW).to_string(index=False))

print(f"\n{'=' * 70}")
