from code_base import *

def getInput() -> tuple[list[Proposition], Proposition]:
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
        while not isFormula(p):
            print(f"Sintaxe inválida, tente novamente...", flush=True)
            p = input().strip()
        premissas.append(p)

    print(f"Consequência", end = ": ", flush=True)
    consequencia = input().strip()
    while not isFormula(consequencia):
        print(f"Sintaxe inválida, tente novamente...", flush=True)
        consequencia = input().strip()
        print(f"Consequência: ", consequencia)

    return ([formula(p) for p in premissas], formula(consequencia))

def formula(s: str):
    """Receber um string e devolvê-lo como um objeto formula 
    """
    scope = {c: Variable(c) for c in s if c.isalpha()}
    return eval(s, {}, scope)

def isFormula(s: str) -> bool:
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

def solver(sequente: tuple[list[Proposition], Proposition]) -> tuple[bool, dict]:
    """Receber um sequente lógico e verificar se ele é válido.
    return: (True, dict = {Variable: 3}), se o sequente é válido;
            (False, dict = {Variable: 1/2/3}), cc.
            dict é um contraexemplo para05 False.
            
    """
    P={}
    # Para testar validade, suponha premissas verdadeiras e consequência falsa 
    # valor 1 representa True
    # valor 2 representa False
    # valor 3 representa conflito
    for p in sequente[0]:
        P[p] |= 1
    P[sequente[1]] |= 2

    # Sequente é válido se encontrarmos qualquer
    return isClosed(P)

def isClosed(P: dict[Proposition, int])-> tuple[bool, dict]:
    """Decidir se um nó formado por P é ramo fechado ou não.
        Um nó é um ramo fechado se ele é saturado sem apresentar contradição ou se todos seus filhos fossem fechados.
        Um nó é um ramo aberto se existe uma contradição ou se um dos seus filhos é um ramo aberto.
        Um ramo é saturado quando não é possível aplicar mais regra de expansão.
    return: (True, {}), se P consitui um ramo fechado;
                (False, um contraexemplo), cc.
    """

    #P é ramo aberto
    for p in P.keys():
        if P[p] == 3:
            return (False, )

    
    # caso base: P saturado
    
def isAlpha(p: tuple[bool, Proposition]) -> bool:
    pass
def isBeta(p: tuple[bool, Proposition]) -> bool:
    pass


sequente = getInput()
print(sequente)
verdict, counter = solver(sequente)


