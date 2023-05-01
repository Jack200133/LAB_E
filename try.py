from LR import canonical_collection
import re

def read_yalp_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content

def split_sections(content):
    sections = content.split('%%')
    tokens_section = sections[0]
    productions_section = sections[1]
    return tokens_section, productions_section

def process_tokens_section(content):
    tokens = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith("%token"):
            line_tokens = line[len("%token"):].strip().split(' ')
            tokens.extend(line_tokens)
    return tokens

def process_productions_section(content):
    productions = {}
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Eliminar comentarios
    lines = content.split('\n')
    current_production = None
    production_rules = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            if current_production:
                productions[current_production] = production_rules
                production_rules = []
            current_production = line[:-1]
        elif line.endswith(';'):
            line = line[:-1]
            production_rules.append(line)
            productions[current_production] = production_rules
            production_rules = []
            current_production = None
        else:
            if (line.startswith('|') or line.startswith('->')) and current_production:
                line = line.strip()
                production_rules.extend(line.split('|'))

            elif ('|' in line) and current_production:
                line = line.strip()
                production_rules.extend(line.split('|'))
            else:
                production_rules.append(line)
    return productions

def parse_yalp_file(filename):
    content = read_yalp_file(filename)
    tokens_section, productions_section = split_sections(content)
    tokens = process_tokens_section(tokens_section)
    productions = process_productions_section(productions_section)
    return tokens, productions

def convert_productions(productions_dict):
    converted_productions = {}
    for key, value in productions_dict.items():
        converted_productions[key] = [rule.split() for rule in value]
    return converted_productions


tokens, productions_dict = parse_yalp_file('input.yalp')
converted_productions = convert_productions(productions_dict)
productions = [(nt, rule) for nt, rules in productions_dict.items() for rule in rules]
print(converted_productions)
states, transitions = canonical_collection(converted_productions)

print('Estados:')
for i, state in enumerate(states):
    print(f'{i}: {state}')

print('Transiciones:')
for transition in transitions:
    print(transition)