#!/usr/bin/env python3
import re
import unicodedata

def normalize_text(text):
    lowered = text.lower()
    no_acc = unicodedata.normalize('NFKD', lowered)
    no_acc = ''.join(ch for ch in no_acc if not unicodedata.combining(ch))
    no_acc = re.sub(r'\s+', ' ', no_acc).strip()
    return no_acc

def build_sonho_pattern():
    return re.compile(r'\bsonh[oaos]*\b', re.IGNORECASE)

# Teste com texto pequeno que contém "sonho"
test_text = '''CANTO I
1
As armas e os barões assinalados
2
Que da ocidental praia Lusitana
3
Por mares nunca dantes navegados
4
Passaram ainda além da Taprobana
5
Em perigos e guerras esforçados
6
Mais do que prometia a força humana
7
E entre gente remota edificaram
8
Novo Reino, que tanto sublimaram

CANTO II
56
Sonhos que a alma enleva e o coração aflige
57
E que às vezes nos fazem despertar
58
Com lágrimas nos olhos, e às vezes
59
Nos fazem rir, e às vezes chorar
60
E que às vezes nos fazem sonhar
61
Com coisas que nunca hão de ser
62
E que às vezes nos fazem dormir
63
E que às vezes nos fazem acordar

CANTO VIII
47
Sonhos proféticos que o futuro mostram
48
E que às vezes nos fazem temer
49
E que às vezes nos fazem esperar
50
E que às vezes nos fazem crer
51
E que às vezes nos fazem duvidar'''

print("=== TESTE DE BUSCA POR SONHO* ===")
print(f"Texto original (primeiras 200 chars): {test_text[:200]}...")
print()

text_norm = normalize_text(test_text)
print(f"Texto normalizado (primeiras 200 chars): {text_norm[:200]}...")
print()

sonho_pattern = build_sonho_pattern()
print(f"Padrão regex: {sonho_pattern.pattern}")
print()

matches = sonho_pattern.findall(text_norm)
print(f"Matches encontrados: {matches}")
print(f"Total de matches: {len(matches)}")
print()

# Teste linha por linha
print("=== ANÁLISE LINHA POR LINHA ===")
lines = test_text.split('\n')
for i, line in enumerate(lines):
    line_norm = normalize_text(line)
    line_matches = sonho_pattern.findall(line_norm)
    if line_matches:
        print(f"Linha {i+1}: '{line.strip()}' -> {line_matches}")

print()
print("=== TESTE COM TERMOS ESPECÍFICOS ===")
test_terms = ['sonho', 'sonhos', 'sonhar', 'sonhando', 'sonhador']
for term in test_terms:
    pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
    count = len(pattern.findall(text_norm))
    print(f"'{term}': {count} ocorrências")
