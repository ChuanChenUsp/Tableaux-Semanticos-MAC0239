"""
test.py - Script de testes do provador de tableaux semânticos (provador.py)
MAC0239 - EP Cálculo Proposicional

Uso:
    python test.py

O script executa duas baterias de testes:
  1. Sintaxe (isFormula)
  2. Sequentes clássicos (válidos e inválidos), com resultado esperado e
     verificação independente de cada contraexemplo

Termina com código de saída 0 se tudo passou e 1 caso contrário.
"""

import sys
from contextlib import redirect_stdout
from io import StringIO
from itertools import product

from provador import formula, isFormula, solve


# ----------------------------------------------------------------------
# Funções auxiliares
# ----------------------------------------------------------------------

def formatar(premissas, conclusao):
    """Formata um sequente como 'A1, A2 |- B'."""
    return f"{', '.join(premissas) if premissas else '(vazio)'} |- {conclusao}"


def resolver(premissas_str, conclusao_str):
    """Converte as strings em fórmulas e chama solve() sem poluir a saída.

    Devolve (premissas, conclusao, valido, contraexemplo).
    """
    premissas = [formula(p) for p in premissas_str]
    conclusao = formula(conclusao_str)
    with redirect_stdout(StringIO()):  # solve() imprime; aqui silenciamos
        valido, contra = solve((premissas, conclusao))
    return premissas, conclusao, valido, contra


def contraexemplo_ok(premissas, conclusao, contra):
    """Confere se 'contra' é mesmo um contraexemplo.

    solve() devolve {variável: 1 (True) ou 2 (False)}. O ramo aberto pode
    ser parcial (variáveis que não aparecem ficam livres), então
    testamos TODAS as completações possíveis das variáveis livres:
    em todas elas as premissas devem ser verdadeiras e a conclusão falsa.
    """
    todas = set(conclusao.variables())
    for p in premissas:
        todas |= p.variables()
    livres = sorted(todas - set(contra))

    base = {nome: (val == 1) for nome, val in contra.items()}
    for valores in product([True, False], repeat=len(livres)):
        v = dict(base)
        v.update(zip(livres, valores))
        if not all(p.evaluate(**v) for p in premissas):
            return False
        if conclusao.evaluate(**v):
            return False
    return True


# ----------------------------------------------------------------------
# Casos de teste
# ----------------------------------------------------------------------

# Sintaxe: (string, esperado)
CASOS_SINTAXE = [
    ("p", True),
    ("~p", True),
    ("(p >> q)", True),
    ("(((a | b) >> q) & (~s))", True),
    ("~~p", True),
    ("A & B", True),
    ("", False),
    ("p >>", False),
    ("(p", False),
    ("p & & q", False),
    ("p q", False),
    ("pq", False),
    ("p >> )", False),
]

# Sequentes: (nome, premissas, conclusão, é_válido)
CASOS_SEQUENTES = [
    # --- válidos ---
    ("Modus ponens",                ["p", "p >> q"], "q", True),
    ("Modus tollens",               ["p >> q", "~q"], "~p", True),
    ("Silogismo disjuntivo",        ["p | q", "~p"], "q", True),
    ("Silogismo hipotético",        ["p >> q", "q >> r"], "p >> r", True),
    ("Dilema construtivo",          ["p >> q", "r >> s", "p | r"], "q | s", True),
    ("Contraposição",               ["p >> q"], "~q >> ~p", True),
    ("De Morgan (conjunção)",       ["~(p & q)"], "~p | ~q", True),
    ("De Morgan (disjunção)",       ["~(p | q)"], "~p & ~q", True),
    ("Exportação",                  ["(p & q) >> r"], "p >> (q >> r)", True),
    ("Dupla negação",               ["~~p"], "p", True),
    ("Introdução da conjunção",     ["p", "q"], "p & q", True),
    ("Explosão (premissas contraditórias)", ["p", "~p"], "q", True),
    ("Átomos maiúsculos",           ["A", "A >> B"], "B", True),
    ("Terceiro excluído (sem premissas)", [], "p | ~p", True),
    ("Lei de Peirce (sem premissas)", [], "((p >> q) >> p) >> p", True),
    ("Distributividade",            ["p & (q | r)"], "(p & q) | (p & r)", True),
    # --- inválidos ---
    ("Non sequitur",                ["p"], "q", False),
    ("Afirmação do consequente",    ["p >> q", "q"], "p", False),
    ("Negação do antecedente",      ["p >> q", "~p"], "~q", False),
    ("Falácia do meio excluído",    ["p | q", "p"], "~q", False),
    ("Sem premissas, átomo",        [], "p", False),
    ("Disjunção vs conjunção",      ["p | q"], "p & q", False),
    ("Recíproca",                   ["p >> q"], "q >> p", False),
    ("Contradição como conclusão",  ["p"], "p & ~p", False),
]


# ----------------------------------------------------------------------
# Execução
# ----------------------------------------------------------------------

falhas = 0


def verificar(condicao, mensagem):
    """Imprime PASS/FAIL e conta as falhas."""
    global falhas
    if condicao:
        print(f"  [PASS] {mensagem}")
    else:
        print(f"  [FAIL] {mensagem}")
        falhas += 1


def teste_sintaxe():
    print("=== 1. Sintaxe (isFormula) ===")
    for s, esperado in CASOS_SINTAXE:
        verificar(isFormula(s) == esperado, f"isFormula({s!r}) == {esperado}")


def teste_sequentes():
    print("\n=== 2. Sequentes clássicos ===")
    for nome, prem, concl, esperado in CASOS_SEQUENTES:
        premissas, conclusao, valido, contra = resolver(prem, concl)
        desc = f"{nome}: {formatar(prem, concl)}  -> esperado {'válido' if esperado else 'inválido'}"
        verificar(valido == esperado, desc)

        # Para inválidos, confere o contraexemplo
        if not valido:
            verificar(contraexemplo_ok(premissas, conclusao, contra),
                      f"   contraexemplo {contra} é realmente um contraexemplo")
        else:
            verificar(contra == {}, "   sequente válido devolve contraexemplo vazio")


if __name__ == "__main__":
    teste_sintaxe()
    teste_sequentes()

    print("\n" + "=" * 40)
    if falhas == 0:
        print("Todos os testes passaram.")
    else:
        print(f"{falhas} verificação(ões) falharam.")
    sys.exit(1 if falhas else 0)