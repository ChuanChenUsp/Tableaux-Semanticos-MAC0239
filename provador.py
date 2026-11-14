from code_base import *

def get_input() -> tuple[list[Proposition], Proposition]:
    """Ler uma sequente lógica da entrada e devolver as premissas e a consequência. 
    return: Uma tupla onde o primeiro elemento é a lista de premissas e o segundo elemento é a consequência.
    """

    print("Quantidade de premissas", end=": ", flush=True)
    n = input()
    while True:
        try:
            n = int(n)
            break
        except:
            print("Valor informado não é um inteiro, tente novamente...", flush=True)
            n = input()

    premissas = []
    for i in range(n):
        print(f"Premissa ", i+1, end=": ", flush=True)
        p = input().strip()
        while not is_formula(p):
            print(f"Sintaxe inválida, tente novamente...", flush=True)
            p = input().strip()
        premissas.append(p)

    print(f"Consequência", end = ": ", flush=True)
    consequencia = input().strip()
    while not is_formula(consequencia):
        print(f"Sintaxe inválida, tente novamente...", flush=True)
        consequencia = input().strip()
        print(f"Consequência: ", consequencia)

    return ([formula(p) for p in premissas], formula(consequencia))

def formula(s: str):
    """Receber um string e devolvê-lo como um objeto formula 
    """
    scope = {c: Variable(c) for c in s if c.isalpha()}
    return eval(s, {}, scope)

def is_formula(s: str) -> bool:
    """Receber um string s e verificar se ele é potencialmente uma formula
        • Fórmula: Uma fórmula é constituída por átomos, conectivos lógicos e parênteses.
        • Átomos: P, Q,... (representados por 1 letra, minúscula ou maiúscula)
        • Conectivos: ~(¬), & (∧), | (v), >> (→)
        • Exemplos de fórmulas: (p >> q), (((A | B) >> q) & (~s)), etc

    return: True, se s é potencialmente uma formula
            False, cc.
    """
    if not isinstance(s, str):
        return False
    try:
        formula(s)
        return True
    except:
        return False

def solver(inputs):
    pass

inputs = get_input()
print(inputs)
verdict = solver(inputs)


