import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the logo lines and replace with text logos
# Replace broken emoji logos with text
content = re.sub(
    r"'logo':\s*'[^']*\xf0[^']*'",
    lambda m: (
        "'logo': '1mg', 'logo_bg': '#e53935'" if '1mg' in content[max(0,content.find(m.group())-200):content.find(m.group())]
        else "'logo': 'PE', 'logo_bg': '#1565c0'"
    ),
    content
)

# Simpler approach - just find each platform block and fix logo
lines = content.split('\n')
new_lines = []
i = 0
in_1mg = False
in_pharmeasy = False
in_apollo = False

for line in lines:
    if "'name': '1mg'" in line:
        in_1mg = True
        in_pharmeasy = False
        in_apollo = False
    elif "'name': 'PharmEasy'" in line:
        in_pharmeasy = True
        in_1mg = False
        in_apollo = False
    elif "'name': 'Apollo Pharmacy'" in line:
        in_apollo = True
        in_1mg = False
        in_pharmeasy = False

    if "'logo':" in line and ("'logo': '1mg'" not in line and "'logo': 'PE'" not in line and "'logo': 'Ap'" not in line):
        # This is a broken emoji logo line
        indent = len(line) - len(line.lstrip())
        spaces = ' ' * indent
        if in_1mg:
            new_lines.append(f"{spaces}'logo': '1mg',")
            new_lines.append(f"{spaces}'logo_bg': '#e53935',")
        elif in_pharmeasy:
            new_lines.append(f"{spaces}'logo': 'PE',")
            new_lines.append(f"{spaces}'logo_bg': '#1565c0',")
        elif in_apollo:
            new_lines.append(f"{spaces}'logo': 'Ap',")
            new_lines.append(f"{spaces}'logo_bg': '#0277bd',")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

result = '\n'.join(new_lines)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(result)

print("Done - logos fixed")

# Verify
with open('app.py', 'r', encoding='utf-8') as f:
    c = f.read()
idx = c.find("'logo':")
print("Logo context:", repr(c[idx:idx+50]))
