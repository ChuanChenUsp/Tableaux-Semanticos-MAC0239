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

    PREMISSA = Constant(True)
    for p in sequente[0]: 
        PREMISSA = And(PREMISSA, p)
    
    CONSEQUENCIA = sequente[1]

    # Sequente é válido se ele é fechado. 
    rules = []
    root = isClosed(False, PREMISSA>>CONSEQUENCIA, rules)

    if root: # Não é válido. Existe um contraexemplo root[1].
        print(f"Sequente não é válido. Contraexemplo:")
        contraexemplo = {}
        for var, val in root[0].items():
            print(var, ": ", val)
            contraexemplo[var] = 1 if val else 2
        return (False, contraexemplo)
        
    else: # Válido. Contraexemplo é vazio {}.
        print(f"Sequente é válido.")
        print(f"Regras aplicadas:")
        print(rules)
        return (True, {})
        
    
'''
F ((((A1 & A2) & ..) & An) >> B) -->
uma interpretação de F ((((A1 & A2) & ..) & An) >> B) é contraexemplo de A1, A2, .., An |- B.  
'''

def isClosed(Value: bool, P: Proposition, rules: list)-> list[dict]:
    """Decidir se um nó formado por P é ramo fechado ou não.
        Um nó é um ramo fechado se ele é saturado sem apresentar contradição ou se todos seus filhos fossem fechados.
        Um nó é um ramo aberto se existe uma contradição ou se um dos seus filhos é um ramo aberto.
        Um ramo é saturado quando não é possível aplicar mais regra de expansão.
    return: (True, {Uma interpretação de P}), se P consitui um ramo fechado;
                (False, {Contradição}), cc.
    """
    # Só retorna ramo aberto [{}] se o valor da constante bater com o Value esperado.
    if type(P) == Constant:
        return [{}] if P.value == Value else []

    if type(P) == Variable:
       return [{P.name: Value}]

    if type(P) == Not:
        rules.append("α¬")
        return isClosed(not Value, P.children[0], rules)
        
    # Usa o 'for c in P.children[1:]:' para combinar TODOS os filhos, sem deixar nenhum de fora.
    if type(P) == And or type(P) == Or:
        # Determina qual função de combinação será utilizada
        alpha = (type(P) == And) == Value

        if alpha:
            rules.append("α")
        else:
            rules.append("­β")

        if type(P) == And:
            rules[-1]+="∧"
        else:
            rules[-1]+="∨"

        # Processa o primeiro filho
        res = isClosed(Value, P.children[0], rules)
        # Processa os demais filhos
        for c in P.children[1:]:
            resultado_atual = isClosed(Value, c, rules)
            if alpha:
                res = mergeAlpha(res, resultado_atual)
            else:
                res = mergeBeta(res, resultado_atual)
        return res
# Mantém todos os ramos abertos na lista para o mergeAlpha testar todos contra as outras premissas.
    if type(P) == Implies:
        # P0 >> P1 equivale a (~P0) | P1
        ramo_esq = isClosed(not Value, P.children[0], rules)
        ramo_dir = isClosed(Value, P.children[1], rules)
        if not Value:  # Alfa: P0=True e P1=False
            rules.append("α→")
            return mergeAlpha(ramo_esq, ramo_dir)
        else:          # Beta: P0=False ou P1=True
            rules.append("β→")
            return mergeBeta(ramo_esq, ramo_dir)

    if type(P) == Iff:
        equiv = And(Implies(P.children[0], P.children[1]), Implies(P.children[1], P.children[0]))
        return isClosed(Value, equiv, rules)

    return []

    
def mergeAlpha(A: list[dict], B: list[dict]) -> list[dict]:
    return [a | b for a in A for b in B if all(a[x] == b[x] for x in a if x in b)]


def mergeBeta(A: list[dict], B: list[dict]) -> list[dict]:
    return A + B


def main():
    sequente = getInput()
    print(sequente)
    solve(sequente)

if __name__ == "__main__":
    main()


