conta_bancaria = []
saques_bancarios = []
LIMITE_SAQUES_DIARIOS = 3
saques_realizados = 0
opcoes = """
    [D] = Depositar
    [S] = Saque
    [E] = Extrato Bancário
    
    [0] = Sair
""".upper()

print(opcoes)

def logica_deposito():
    print("==========================================")
    deposito = float(input("Deposite um valor:\n"))
    print("==========================================")
    if deposito >= 1:
        print(f"O valor depositado foi:\nR${deposito:.2f}")
        conta_bancaria.append(deposito)
    else:
        print("Valor inválido para depósito!")



def logica_saque():
    global saques_realizados
    print("============================================")
    saque = float(input("Informe o valor que deseja sacar:\n"))
    print("============================================")
    
    saldo = sum(conta_bancaria)
    
    if saques_realizados >= LIMITE_SAQUES_DIARIOS:
        print("Limite de saques diários atingido!")
        
    elif saque > 500:
        print("Limite de saque é de R$500!")
        
    elif saque > saldo:
        print("Saldo insuficiente!")
        
    elif saque <= 0:
        print("Valor inválido!")
    
    else:
        saques_bancarios.append(saque)
        conta_bancaria.append(-saque) #desconta o valor da conta
        saques_realizados += 1
        print(f"Saque de R${saque:.2f} realizado com sucesso!")
        



def logica_extrato():
    saldo = sum(conta_bancaria)
    print("============================================")
    print("Extrato Bancário")
    print("--------------------------------------------")
    
    if not conta_bancaria:
        print("Nenhuma movimentação realizada.")
    else:
        for mov in conta_bancaria:
            if mov > 0:
                print(f"Depósito: R${mov:.2f}")
            else:
                print(f"Saque: R${abs(mov):.2f}")
    
    
    print("--------------------------------------------")
    print(f"Saldo atual: R${saldo:.2f}")
    print("============================================")
             
while True:
    try:
        escolha = input("Insira uma opção:\n")

        if escolha == "D":
            logica_deposito()

        elif escolha == "S":
            logica_saque()

        elif escolha == "E":
            logica_extrato()
        
        elif escolha == "0":
            break
        
        else:
            print("Opção inválida!")
    except ValueError:
        print("Insira algo válido!!")
