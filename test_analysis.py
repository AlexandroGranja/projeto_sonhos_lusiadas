#!/usr/bin/env python3
"""
Teste da análise de termos
"""

# Dicionário expandido de termos relacionados
EXPANDED_TERMS = {
    'onírico': [
        'sonho', 'sonhar', 'sonhador', 'sonhante', 'sonhoso',
        'pesadelo', 'pesadelar', 'pesadelante', 'pesadeloso',
        'dormir', 'adormecer', 'despertar', 'desperto',
        'sonolência', 'sonolento', 'sonolentamente',
        'sonambulismo', 'sonambúlico', 'sonambular',
        'insônia', 'insone', 'insoniamente', 'insoniar',
        'soneca', 'sonecar', 'sonecante',
        'repouso', 'repousar', 'repousante',
        'descanso', 'descansar', 'descansante'
    ],
    'profético': [
        'visão', 'visionário', 'visionar', 'visionante',
        'profecia', 'profético', 'profetizar', 'profetizante',
        'revelação', 'revelar', 'revelador', 'revelante',
        'aparição', 'aparecer', 'aparecimento', 'aparente',
        'oráculo', 'oracular', 'oracularmente',
        'vaticínio', 'vaticinar', 'vaticinador', 'vaticinante',
        'presságio', 'pressagiar', 'pressagiador',
        'augúrio', 'augurar', 'augurador',
        'predição', 'predizer', 'preditor'
    ],
    'alegórico': [
        'sombra', 'sombreado', 'sombreadamente', 'sombreador',
        'fantasia', 'fantasioso', 'fantasiosamente', 'fantasiar',
        'ilusão', 'ilusório', 'ilusoriamente', 'ilusionar',
        'metáfora', 'metafórico', 'metafóricamente',
        'símbolo', 'simbólico', 'simbolicamente', 'simbolizar',
        'alegoria', 'alegórico', 'alegoricamente', 'alegorizar',
        'emblema', 'emblemático', 'emblematicamente',
        'figura', 'figurado', 'figuradamente', 'figurar',
        'representação', 'representar', 'representante'
    ],
    'divino': [
        'glória', 'glorioso', 'gloriosamente', 'glorificar',
        'divino', 'divinamente', 'divindade', 'divinizar',
        'celestial', 'celestialmente', 'celestialidade',
        'sobrenatural', 'sobrenaturalmente', 'sobrenaturalidade',
        'milagre', 'milagroso', 'milagrosamente', 'milagrar',
        'sagrado', 'sagradamente', 'sacralidade', 'sacralizar',
        'santo', 'santamente', 'santidade', 'santificar',
        'bendito', 'benditamente', 'bendizer',
        'abençoado', 'abençoar', 'abençoador',
        'miraculoso', 'miraculosamente'
    ]
}

def count_expanded_terms(text):
    """Conta termos expandidos no texto."""
    results = {}
    text_lower = text.lower()
    
    for category, terms in EXPANDED_TERMS.items():
        results[category] = {}
        total_count = 0
        
        for term in terms:
            count = text_lower.count(term.lower())
            if count > 0:
                results[category][term] = count
                total_count += count
        
        results[category]['total'] = total_count
    
    return results

# Teste com texto que contém "sonho"
test_text = "O sonho divino da glória portuguesa revelou-se em visões proféticas. O sonho de Dom Manuel foi uma visão sagrada."

print("=== TESTE DE ANÁLISE ===")
print(f"Texto: {test_text}")
print()

results = count_expanded_terms(test_text)

print("=== RESULTADOS ===")
for category, terms in results.items():
    print(f"\n{category.upper()}:")
    for term, count in terms.items():
        if term != 'total' and count > 0:
            print(f"  {term}: {count}")
    print(f"  Total: {terms['total']}")

print(f"\n=== RESUMO ===")
total_dream_terms = sum(cat['total'] for cat in results.values())
print(f"Total de termos encontrados: {total_dream_terms}")
print(f"Palavras no texto: {len(test_text.split())}")
print(f"Cobertura: {(total_dream_terms / len(test_text.split())) * 100:.1f}%")
