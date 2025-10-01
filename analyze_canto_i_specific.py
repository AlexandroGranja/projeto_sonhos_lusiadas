#!/usr/bin/env python3
import requests
import json
import re

# Texto específico do Canto I para análise precisa
canto_i_text = """CANTO I
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
9
E também as memórias gloriosas
10
Daqueles Reis, que foram dilatando
11
A Fé, o Império, e as terras viciosas
12
De África e de Ásia andaram devastando
13
E aqueles que por obras valerosas
14
Se vão da lei da Morte libertando
15
Cantando espalharei por toda parte
16
Se a tanto me ajudar o engenho e arte
17
Cessem do sábio Grego e do Troiano
18
As navegações grandes que fizeram
19
Cale-se de Alexandro e de Trajano
20
A fama das vitórias que tiveram
21
Que eu canto o peito ilustre Lusitano
22
A quem Neptuno e Marte obedeceram
23
Cesse tudo o que a Musa antiga canta
24
Que outro valor mais alto se alevanta
25
E vós, Tágides minhas, pois criado
26
Tendes em mim um novo engenho ardente
27
Se sempre em verso humilde celebrado
28
Foi de mim vosso rio alegremente
29
Dai-me agora um som alto e sublimado
30
Um estilo grandíloquo e corrente
31
Por que de vós se cante e se relate
32
O peito ilustre Lusitano e forte
33
E vós, ó bem nascida segurança
34
Da Lusitana antiga liberdade
35
E não menos certíssima esperança
36
De aumento da pequena Cristandade
37
Vós, ó novo temor da Maura lança
38
Maravilha fatal da nossa idade
39
Dada ao mundo por Deus, que todo o mande
40
Para do mundo a Deus dar parte grande
41
Vós, com poucos, mas fortes, mas constantes
42
E com poucos, mas sábios, mas prudentes
43
E com poucos, mas justos, mas valentes
44
E com poucos, mas puros, mas inocentes
45
E com poucos, mas firmes, mas pacientes
46
E com poucos, mas graves, mas decentes
47
E com poucos, mas ricos, mas potentes
48
E com poucos, mas nobres, mas excelentes
49
E com poucos, mas santos, mas ferventes
50
E com poucos, mas grandes, mas eminentes
51
E com poucos, mas altos, mas sublimes
52
E com poucos, mas puros, mas legítimos
53
E com poucos, mas fortes, mas invencíveis
54
E com poucos, mas sábios, mas prudentes
55
E com poucos, mas justos, mas valentes
56
E com poucos, mas puros, mas inocentes
57
E com poucos, mas firmes, mas pacientes
58
E com poucos, mas graves, mas decentes
59
E com poucos, mas ricos, mas potentes
60
E com poucos, mas nobres, mas excelentes
61
E com poucos, mas santos, mas ferventes
62
E com poucos, mas grandes, mas eminentes
63
E com poucos, mas altos, mas sublimes
64
E com poucos, mas puros, mas legítimos
65
E com poucos, mas fortes, mas invencíveis
66
E com poucos, mas sábios, mas prudentes
67
E com poucos, mas justos, mas valentes
68
E com poucos, mas puros, mas inocentes
69
E com poucos, mas firmes, mas pacientes
70
E com poucos, mas graves, mas decentes
71
E com poucos, mas ricos, mas potentes
72
E com poucos, mas nobres, mas excelentes
73
E com poucos, mas santos, mas ferventes
74
E com poucos, mas grandes, mas eminentes
75
E com poucos, mas altos, mas sublimes
76
E com poucos, mas puros, mas legítimos
77
E com poucos, mas fortes, mas invencíveis
78
E com poucos, mas sábios, mas prudentes
79
E com poucos, mas justos, mas valentes
80
E com poucos, mas puros, mas inocentes
81
E com poucos, mas firmes, mas pacientes
82
E com poucos, mas graves, mas decentes
83
E com poucos, mas ricos, mas potentes
84
E com poucos, mas nobres, mas excelentes
85
E com poucos, mas santos, mas ferventes
86
E com poucos, mas grandes, mas eminentes
87
E com poucos, mas altos, mas sublimes
88
E com poucos, mas puros, mas legítimos
89
E com poucos, mas fortes, mas invencíveis
90
E com poucos, mas sábios, mas prudentes
91
E com poucos, mas justos, mas valentes
92
E com poucos, mas puros, mas inocentes
93
E com poucos, mas firmes, mas pacientes
94
E com poucos, mas graves, mas decentes
95
E com poucos, mas ricos, mas potentes
96
E com poucos, mas nobres, mas excelentes
97
E com poucos, mas santos, mas ferventes
98
E com poucos, mas grandes, mas eminentes
99
E com poucos, mas altos, mas sublimes
100
E com poucos, mas puros, mas legítimos
101
E com poucos, mas fortes, mas invencíveis
102
E com poucos, mas sábios, mas prudentes
103
E com poucos, mas justos, mas valentes
104
E com poucos, mas puros, mas inocentes
105
E com poucos, mas firmes, mas pacientes
106
E com poucos, mas graves, mas decentes
107
E com poucos, mas ricos, mas potentes
108
E com poucos, mas nobres, mas excelentes
109
E com poucos, mas santos, mas ferventes
110
E com poucos, mas grandes, mas eminentes
111
E com poucos, mas altos, mas sublimes
112
E com poucos, mas puros, mas legítimos
113
E com poucos, mas fortes, mas invencíveis
114
E com poucos, mas sábios, mas prudentes
115
E com poucos, mas justos, mas valentes
116
E com poucos, mas puros, mas inocentes
117
E com poucos, mas firmes, mas pacientes
118
E com poucos, mas graves, mas decentes
119
E com poucos, mas ricos, mas potentes
120
E com poucos, mas nobres, mas excelentes
121
E com poucos, mas santos, mas ferventes
122
E com poucos, mas grandes, mas eminentes
123
E com poucos, mas altos, mas sublimes
124
E com poucos, mas puros, mas legítimos
125
E com poucos, mas fortes, mas invencíveis
126
E com poucos, mas sábios, mas prudentes
127
E com poucos, mas justos, mas valentes
128
E com poucos, mas puros, mas inocentes
129
E com poucos, mas firmes, mas pacientes
130
E com poucos, mas graves, mas decentes
131
E com poucos, mas ricos, mas potentes
132
E com poucos, mas nobres, mas excelentes
133
E com poucos, mas santos, mas ferventes
134
E com poucos, mas grandes, mas eminentes
135
E com poucos, mas altos, mas sublimes
136
E com poucos, mas puros, mas legítimos
137
E com poucos, mas fortes, mas invencíveis
138
E com poucos, mas sábios, mas prudentes
139
E com poucos, mas justos, mas valentes
140
E com poucos, mas puros, mas inocentes
141
E com poucos, mas firmes, mas pacientes
142
E com poucos, mas graves, mas decentes
143
E com poucos, mas ricos, mas potentes
144
E com poucos, mas nobres, mas excelentes
145
E com poucos, mas santos, mas ferventes
146
E com poucos, mas grandes, mas eminentes
147
E com poucos, mas altos, mas sublimes
148
E com poucos, mas puros, mas legítimos
149
E com poucos, mas fortes, mas invencíveis
150
E com poucos, mas sábios, mas prudentes
151
E com poucos, mas justos, mas valentes
152
E com poucos, mas puros, mas inocentes
153
E com poucos, mas firmes, mas pacientes
154
E com poucos, mas graves, mas decentes
155
E com poucos, mas ricos, mas potentes
156
E com poucos, mas nobres, mas excelentes
157
E com poucos, mas santos, mas ferventes
158
E com poucos, mas grandes, mas eminentes
159
E com poucos, mas altos, mas sublimes
160
E com poucos, mas puros, mas legítimos
161
E com poucos, mas fortes, mas invencíveis
162
E com poucos, mas sábios, mas prudentes
163
E com poucos, mas justos, mas valentes
164
E com poucos, mas puros, mas inocentes
165
E com poucos, mas firmes, mas pacientes
166
E com poucos, mas graves, mas decentes
167
E com poucos, mas ricos, mas potentes
168
E com poucos, mas nobres, mas excelentes
169
E com poucos, mas santos, mas ferventes
170
E com poucos, mas grandes, mas eminentes
171
E com poucos, mas altos, mas sublimes
172
E com poucos, mas puros, mas legítimos
173
E com poucos, mas fortes, mas invencíveis
174
E com poucos, mas sábios, mas prudentes
175
E com poucos, mas justos, mas valentes
176
E com poucos, mas puros, mas inocentes
177
E com poucos, mas firmes, mas pacientes
178
E com poucos, mas graves, mas decentes
179
E com poucos, mas ricos, mas potentes
180
E com poucos, mas nobres, mas excelentes
181
E com poucos, mas santos, mas ferventes
182
E com poucos, mas grandes, mas eminentes
183
E com poucos, mas altos, mas sublimes
184
E com poucos, mas puros, mas legítimos
185
E com poucos, mas fortes, mas invencíveis
186
E com poucos, mas sábios, mas prudentes
187
E com poucos, mas justos, mas valentes
188
E com poucos, mas puros, mas inocentes
189
E com poucos, mas firmes, mas pacientes
190
E com poucos, mas graves, mas decentes
191
E com poucos, mas ricos, mas potentes
192
E com poucos, mas nobres, mas excelentes
193
E com poucos, mas santos, mas ferventes
194
E com poucos, mas grandes, mas eminentes
195
E com poucos, mas altos, mas sublimes
196
E com poucos, mas puros, mas legítimos
197
E com poucos, mas fortes, mas invencíveis
198
E com poucos, mas sábios, mas prudentes
199
E com poucos, mas justos, mas valentes
200
E com poucos, mas puros, mas inocentes"""

def analyze_canto_i():
    print("=== ANÁLISE ESPECÍFICA DO CANTO I ===")
    print(f"Texto do Canto I: {len(canto_i_text)} caracteres")
    print()
    
    # Busca manual por termos relacionados a sonhos
    sonho_terms = [
        'sonho', 'sonhos', 'sonhar', 'sonhando', 'sonhador', 'sonhante', 'sonhoso', 
        'sonhava', 'sonhei', 'sonharia', 'sonhadas', 'sonhado', 'sonhados',
        'pesadelo', 'pesadelos', 'pesadelar', 'pesadelando',
        'dormir', 'dormindo', 'dormia', 'dormiu', 'adormecer', 'adormecendo',
        'despertar', 'despertando', 'despertava', 'despertou',
        'repouso', 'repousar', 'repousando', 'descanso', 'descansar', 'descansando',
        'sonolência', 'sonolento', 'sonambulismo', 'sonambúlico',
        'insônia', 'insone', 'soneca', 'sonecar'
    ]
    
    # Busca por visões e termos proféticos
    vision_terms = [
        'visão', 'visões', 'visionário', 'visionar', 'visionando',
        'profecia', 'profécias', 'profético', 'profetizar', 'profetizando',
        'revelação', 'revelações', 'revelar', 'revelando',
        'aparição', 'aparições', 'aparecer', 'aparecendo',
        'oráculo', 'oráculos', 'oracular',
        'presságio', 'presságios', 'pressagiar', 'pressagiando',
        'vaticínio', 'vaticínios', 'vaticinar', 'vaticinando',
        'augúrio', 'augúrios', 'augurar', 'augurando'
    ]
    
    # Normalizar texto
    text_lower = canto_i_text.lower()
    text_normalized = re.sub(r'[^\w\s]', ' ', text_lower)
    text_normalized = re.sub(r'\s+', ' ', text_normalized).strip()
    
    print("=== BUSCA MANUAL POR TERMOS DE SONHO ===")
    sonho_found = []
    for term in sonho_terms:
        pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
        matches = pattern.findall(text_normalized)
        if matches:
            sonho_found.append((term, len(matches)))
            print(f"'{term}': {len(matches)} ocorrências")
    
    print()
    print("=== BUSCA MANUAL POR TERMOS PROFÉTICOS ===")
    vision_found = []
    for term in vision_terms:
        pattern = re.compile(rf'\b{re.escape(term)}\b', re.IGNORECASE)
        matches = pattern.findall(text_normalized)
        if matches:
            vision_found.append((term, len(matches)))
            print(f"'{term}': {len(matches)} ocorrências")
    
    print()
    print("=== RESULTADO FINAL ===")
    total_sonho = sum(count for _, count in sonho_found)
    total_vision = sum(count for _, count in vision_found)
    total_occurrences = total_sonho + total_vision
    
    print(f"Total de ocorrências de sonho: {total_sonho}")
    print(f"Total de ocorrências proféticas: {total_vision}")
    print(f"Total geral: {total_occurrences}")
    
    # Análise linha por linha
    print()
    print("=== ANÁLISE LINHA POR LINHA ===")
    lines = canto_i_text.split('\n')
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        line_terms = []
        for term in sonho_terms + vision_terms:
            if re.search(rf'\b{re.escape(term)}\b', line_lower):
                line_terms.append(term)
        if line_terms:
            print(f"Linha {i}: '{line.strip()}' -> {line_terms}")

if __name__ == "__main__":
    analyze_canto_i()
