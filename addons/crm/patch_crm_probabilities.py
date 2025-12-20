import os

file_path = r'd:\odoo-19.0\odoo-19.0\addons\crm\models\crm_lead.py'
print(f"Patching: {file_path}")

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the _compute_probabilities function
start_idx = -1
for i, line in enumerate(lines):
    if 'def _compute_probabilities(self):' in line:
        start_idx = i
        print(f"Found _compute_probabilities at line {i+1}")
        break

if start_idx != -1:
    # Find the problematic line
    for i in range(start_idx, min(start_idx + 20, len(lines))):
        if 'lead_probabilities, _unused = self._pls_get_naive_bayes_probabilities()' in lines[i]:
            print(f"Found problematic line at {i+1}")
            # Replace with safe version
            indent = len(lines[i]) - len(lines[i].lstrip())
            lines[i] = ' ' * indent + 'pls_result = self._pls_get_naive_bayes_probabilities()\n'
            lines.insert(i+1, ' ' * indent + 'lead_probabilities = pls_result[0] if pls_result else {}\n')
            print("Patch applied!")
            break
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("File saved successfully!")
else:
    print("Error: Could not find function")
