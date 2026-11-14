from code_base import *

def get_input() -> tuple[list[Proposition], Proposition]:
    """Ler uma sequente lógica da entrada e devolver as premissas e a consequência. 
    return: Uma tupla onde o primeiro elemento é a lista de premissas e o segundo elemento é a consequência.
    """

    print("Quantidade de premissas", end=": ", flush=True)
    n = int(input())

    premissas = []
    for i in range(n):
        print(f"Premissa ", i+1, end=": ", flush=True)
        p = input().strip()
        while not is_formula(p):
            print(f"Sintaxe inválida, tente novamente...\n", flush=True)
            p = input().strip()
        premissas.append(p)
        # print(premissas[i])

    print(f"Consequência", end = ": ", flush=True)
    consequencia = input().strip()
    while not is_formula(consequencia):
        print(f"Sintaxe inválida, tente novamente...\n", flush=True)
        consequencia = input().strip()
    # print(consequencia)

    return ([formula(p) for p in premissas], formula(consequencia))

def formula(s: str):
    """Receber um string e devolvê-lo como um objeto formula 
    """
    scope = {c: Variable(c) for c in s if c.isalpha()}
    return eval(s, {}, scope)

def is_formula(s: str) -> bool:
    """Receber um string s e verificar se ele é potencialmente uma formula
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


