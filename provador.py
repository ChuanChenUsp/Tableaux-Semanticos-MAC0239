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

def solve(sequente: tuple[list[Proposition], Proposition]) -> tuple[bool, dict]:
    """Receber um sequente lógico e verificar se ele é válido.
    return: (True, dict = {Variable: 3}), se o sequente é válido;
            (False, dict = {Variable: 1/2/3}), cc.
            dict é um contraexemplo para False.
            
    """
    # Para testar validade, suponha premissas verdadeiras e consequência falsa 
    # valor 1 representa True
    # valor 2 representa False
    # valor 3 representa conflito

    PREMISSA = True
    for i in range(len(sequente[0])):
        PREMISSA = (PREMISSA&sequente[0][i])
    
    CONSEQUENCIA = sequente[1]

    # Sequente é válido se ele é fechado. 
    root = isClosed(False, PREMISSA>>CONSEQUENCIA)
    if root[0]: # Não é válido. Existe um contraexemplo root[1].
        print(f"Sequente não é válido. Contraexemplo:")
        for atom in root[1].keys():
            print(atom, ": ", root[1][atom])
    else: # Válido. Contraexemplo é vazio {}.
        print(f"Sequente é válido.")
        
    
'''
F ((((A1 & A2) & ..) & An) >> B) -->
uma interpretação de F ((((A1 & A2) & ..) & An) >> B) é contraexemplo de A1, A2, .., An |- B.  
'''

def isClosed(Value: bool, P: Proposition)-> tuple[bool, dict]:
    """Decidir se um nó formado por P é ramo fechado ou não.
        Um nó é um ramo fechado se ele é saturado sem apresentar contradição ou se todos seus filhos fossem fechados.
        Um nó é um ramo aberto se existe uma contradição ou se um dos seus filhos é um ramo aberto.
        Um ramo é saturado quando não é possível aplicar mais regra de expansão.
    return: (True, {Uma interpretação de P}), se P consitui um ramo fechado;
                (False, {Contradição}), cc.
    """

    if type(P) == Constant:
        return (True, {})
    if type(P) == Not:
        self = P.children[0]
    elif type(P) != Variable:
        l = P.children[0]
        r = P.children[1]

    if type(P) == Variable:
        return (True, {P.name: Value})
    elif type(P) == And:
        if Value:
            return mergeAlpha(isClosed(True, l), isClosed(True, r))
        else:
            return mergeBeta(isClosed(False, l), isClosed(False, r))
    elif type(P) == Or:
        if Value:
            return mergeBeta(isClosed(True, l), isClosed(True, r))
        else:
            return mergeAlpha(isClosed(False, l), isClosed(False, r))
    elif type(P) == Implies:
        if Value:
            return mergeBeta(isClosed(False, l), isClosed(True, r))
        else:
            return mergeAlpha(isClosed(True, l), isClosed(False, r))
    elif type(P) == Not:
        return isClosed(not Value, self)

    
def mergeAlpha(a: tuple[bool, dict], b: tuple[bool, dict]) -> tuple[bool, dict]:
    if not a[0] or not b[0]:
        return (False, {})
    for atom in a[1].keys():
        if atom in b[1].keys():
            if a[1][atom]^b[1][atom]:
                return (False, {})
    return (True, a[1]|b[1])
def mergeBeta(a: tuple[bool, dict], b: tuple[bool, dict]) -> tuple[bool, dict]:
    if a[0]:
        return a
    if b[1]:
        return b
    return (False, {})


sequente = getInput()
print(sequente)
solve(sequente)


