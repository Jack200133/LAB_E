
from yapl import *
from yalex import *


CEND = '\33[0m'
CRED = '\33[91m'
CYELLOW = '\33[93m'
CGREEM = '\33[92m'
CBLUE = '\33[94m'

with open('yalex/lex2.yal', 'r') as f:
    # Leer todas las líneas del archivo
    yalex_content = f.read()


header_result = ''
regex = {}
simple_pattern = r"\[(\w)\s*-\s*(\w)\]"
compound_pattern = r"\[(\w)\s*-\s*(\w)\s*(\w)\s*-\s*(\w)\]"
simple_regex_pattern = r"^let\s+\w+\s+=\s+(.*?)$"

# Llamando a las funciones en orden
file_content = yalex_content

header_result, trailer_result, file_content,i = build_header_and_trailer(file_content)
file_content = clean_comments(file_content)
file_content = replace_quotation_mark(file_content)
regex,errorStack,fin = build_regex(file_content,i)
LEXtokens,errorStack = build_tokens(file_content, regex,errorStack,fin+1)

tokens, productions_dict,errorStack = parse_yalp_file('yapar/lex2.yalp',errorStack)
if errorStack:
    print(CRED,"Error stack:")
    for error in errorStack:
        print(error)
    print(CEND)
    exit()

gooTokens = []

for token in tokens:
    for lex_token in LEXtokens:
        evald = evalToken(lex_token)
        if token == evald:
            gooTokens.append(token)
    if token not in gooTokens:
        errorStack.append(f"Token {token} no definido en el YALEX")

if len(gooTokens) < len(LEXtokens):
    errorStack.append("Faltaron Definir tokens en el YAPAR")


if errorStack:
    print(CRED,"Error stack:")
    for error in errorStack:
        print(error)
    print(CEND)
    exit()

converted_productions = convert_productions(productions_dict)
# productions = [(nt, rule) for nt, rules in productions_dict.items() for rule in rules]
print("----------------------")
print(converted_productions)
print("----------------------")

states, transitions = canonical_collection(converted_productions)

print('Estados:')
for i, state in enumerate(states):
    print(f'{i}: {state}')

print('Transiciones:')
for transition in transitions:
    print(transition)
# Ejemplo de uso:

visualize_lr0(states, transitions)

print("\n------------LL----------\n\n")

def convert_productions(productions):
    converted_productions = {}
    for key, value in productions.items():
        converted_productions[key] = [prod.split() for prod in value]
    return converted_productions

print(productions_dict)
converted_prod = convert_productions(productions_dict)
first = first_sets(converted_prod)
follow = follow_sets(converted_prod, first)

print("First sets:")
for non_terminal, first_set in first.items():
    print(f"{non_terminal}: {first_set}")

print("\nFollow sets:")
for non_terminal, follow_set in follow.items():
    print(f"{non_terminal}: {follow_set}")
