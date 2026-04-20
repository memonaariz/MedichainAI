import re

text = """haemoglobin l 7.5 12.0 - 15.0 gm
red blood cells erythrocytes 4.11 3.8 - 4.8 x 10^6
haematocrit (pcv) l 25.7 40 - 50
mcv l 62.53 83 - 101 fl
mch l 18.25 27 - 32 pg
mchc l 29.18 31.5 - 34.5
rdw-cv h 18.6 11.6 - 14.0
total w.b.c count 8800 4000 - 10000
neutrophils 58 40 - 80
lymphocytes 32 20 - 40
eosinophils 04 1 - 6
monocytes 06 2 - 10
basophils 00 0 - 2
platelets count h 451 150 - 410"""

patterns = [
    ('Haemoglobin', r'h[ae]e?moglobin\s+([lh])?\s*(\d+\.?\d*)'),
    ('RBC',         r'(?:red\s+blood\s+cells?|erythrocytes)\s+([lh])?\s*(\d+\.?\d*)'),
    ('PCV',         r'h[ae]e?matocrit\s*(?:\(pcv\))?\s*([lh])?\s*(\d+\.?\d*)'),
    ('MCV',         r'\bmcv\s+([lh])?\s*(\d+\.?\d*)'),
    ('MCH',         r'\bmch\s+([lh])?\s*(\d+\.?\d*)'),
    ('MCHC',        r'\bmchc\s+([lh])?\s*(\d+\.?\d*)'),
    ('RDW',         r'rdw[\-\s]cv\s+([lh])?\s*(\d+\.?\d*)'),
    ('WBC',         r'(?:total\s+)?w\.?b\.?c\.?\s+count\s+([lh])?\s*(\d+\.?\d*)'),
    ('Neutrophils', r'neutrophils\s+(\d+\.?\d*)\s+\d'),
    ('Lymphocytes', r'lymphocytes\s+(\d+\.?\d*)\s+\d'),
    ('Eosinophils', r'eosinophils\s+(\d+\.?\d*)\s+\d'),
    ('Monocytes',   r'monocytes\s+(\d+\.?\d*)\s+\d'),
    ('Basophils',   r'basophils\s+(\d+\.?\d*)\s+\d'),
    ('Platelets',   r'platelets?\s+count\s+([lh])?\s*(\d+\.?\d*)'),
]

for name, pat in patterns:
    m = re.search(pat, text)
    if m:
        groups = [g for g in m.groups() if g is not None]
        print(name + ': ' + str(groups))
    else:
        print(name + ': NOT FOUND')
