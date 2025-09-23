import datetime
import os
import msvcrt

cpf_cadastrados = []
usuarios = {}
LIMITE_SAQUES_DIARIOS = 3
LIMITE_TRANSACOES_DIARIAS = 10
ID_AGENCIA = "0001"
opcoes = """
    [D] = Depositar
    [S] = Saque
    [C] = Criar conta corrente
    [U] = Cadastrar Usuário
    [E] = Extrato Bancário
    [0] = Sair
"""

def logica_cadastro():
    while True:
        nome = input("Insira o seu nome:\n").strip()
        if nome:
            break
        print("Nome não pode estar vazio! Tente novamente.")

    print("\nInforme agora a data de nascimento no formato (Dia/Mês/Ano)")
    while True:
        try:
            dia = int(input("Dia:\n"))
            mes = int(input("Mês:\n"))
            ano = int(input("Ano:\n"))
            data_nascimento = datetime.date(ano, mes, dia)
            print(f"Data de nascimento informada: {data_nascimento.strftime('%d/%m/%Y')}")
            break
        except ValueError:
            print("Data inválida!")

    while True:
        cpf = input("Insira o CPF (somente números, 11 dígitos):\n").strip()
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido! Digite um CPF correto.")
        elif cpf in cpf_cadastrados:
            print("CPF já cadastrado! Tente outro.")
        else:
            cpf_cadastrados.append(cpf)
            break

    print("Informe agora o endereço:")
    logradouro = input("Logradouro:\n")
    bairro = input("Bairro:\n")
    cidade = input("Cidade:\n")
    estado = input("Estado:\n")

    usuarios[cpf] = {
        "nome": nome,
        "data_nascimento": f"{dia}/{mes}/{ano}",
        "cpf": cpf,
        "endereco": {
            "logradouro": logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        },
        "contas": {"principal": None, "secundaria": None},
        "contas_transacoes": {"principal": [], "secundaria": []},
        "saques_realizados": 0,
        "transacoes_total": 0
    }

    print("Usuário cadastrado!")
    print("Pressione qualquer tecla para continuar...")
    msvcrt.getch()
    os.system("cls")


def logica_criar_conta_corrente(cpf):
    numero_conta = input("Informe o número da conta principal (5 a 8 dígitos):\n").strip()
    while len(numero_conta) < 5 or len(numero_conta) > 8:
        numero_conta = input("Número inválido! Informe novamente:\n").strip()
    usuarios[cpf]["contas"]["principal"] = numero_conta
    print(f"Conta principal {numero_conta} criada com sucesso!")

    criar_segunda = input("Deseja criar uma conta secundária? (SIM/NÃO):\n").strip().upper()
    if criar_segunda == "SIM":
        numero_segunda = input("Informe o número da conta secundária (5 a 8 dígitos):\n").strip()
        while len(numero_segunda) < 5 or len(numero_segunda) > 8:
            numero_segunda = input("Número inválido! Informe novamente:\n").strip()
        usuarios[cpf]["contas"]["secundaria"] = numero_segunda
        print(f"Conta secundária {numero_segunda} criada com sucesso!")


def logica_deposito():
    cpf = input("Informe o CPF do usuário:\n").strip()
    if cpf not in usuarios:
        print("CPF não cadastrado!")
        return

    tipo_conta = input("Deseja depositar na conta principal ou secundária? (principal/secundaria):\n").strip().lower()
    if tipo_conta not in ["principal", "secundaria"]:
        print("Conta inválida!")
        return

    if usuarios[cpf]["transacoes_total"] >= LIMITE_TRANSACOES_DIARIAS:
        print("Você excedeu o limite de transações diárias!")
        return

    try:
        valor = float(input("Informe o valor do depósito:\n"))
        if valor <= 0:
            print("Valor inválido para depósito!")
            return
    except ValueError:
        print("Valor inválido!")
        return

    data_hora = datetime.datetime.now()
    usuarios[cpf]["contas_transacoes"][tipo_conta].append((valor, data_hora))
    usuarios[cpf]["transacoes_total"] += 1
    print(f"Depósito de R${valor:.2f} realizado com sucesso em {data_hora}!")
    print("Pressione qualquer tecla para continuar...")
    msvcrt.getch()
    os.system("cls")


def logica_saque():
    cpf = input("Informe o CPF do usuário:\n").strip()
    if cpf not in usuarios:
        print("CPF não cadastrado!")
        return

    tipo_conta = input("Deseja sacar da conta principal ou secundária? (principal/secundaria):\n").strip().lower()
    if tipo_conta not in ["principal", "secundaria"]:
        print("Conta inválida!")
        return

    if usuarios[cpf]["transacoes_total"] >= LIMITE_TRANSACOES_DIARIAS:
        print("Você excedeu o limite de transações diárias!")
        return
    if usuarios[cpf]["saques_realizados"] >= LIMITE_SAQUES_DIARIOS:
        print("Limite de saques diários atingido!")
        return

    saldo = sum(valor for valor, _ in usuarios[cpf]["contas_transacoes"][tipo_conta])
    try:
        valor = float(input("Informe o valor do saque:\n"))
        if valor <= 0 or valor > saldo or valor > 500:
            print("Saque inválido! Valor maior que o saldo ou limite R$500.")
            return
    except ValueError:
        print("Valor inválido!")
        return

    data_hora = datetime.datetime.now()
    usuarios[cpf]["contas_transacoes"][tipo_conta].append((-valor, data_hora))
    usuarios[cpf]["saques_realizados"] += 1
    usuarios[cpf]["transacoes_total"] += 1
    print(f"Saque de R${valor:.2f} realizado com sucesso em {data_hora}!")
    print("Pressione qualquer tecla para continuar...")
    msvcrt.getch()
    os.system("cls")


def logica_extrato():
    cpf = input("Informe o CPF do usuário:\n").strip()
    if cpf not in usuarios:
        print("CPF não cadastrado!")
        return

    tipo_conta = input("Deseja ver extrato da conta principal ou secundária? (principal/secundaria):\n").strip().lower()
    if tipo_conta not in ["principal", "secundaria"]:
        print("Conta inválida!")
        return

    transacoes = usuarios[cpf]["contas_transacoes"][tipo_conta]
    saldo = sum(valor for valor, _ in transacoes)

    print("============================================")
    print(f"Extrato da conta {tipo_conta}")
    print("--------------------------------------------")
    if not transacoes:
        print("Nenhuma movimentação realizada.")
    else:
        for valor, data_hora in transacoes:
            tipo = "Depósito" if valor > 0 else "Saque"
            print(f"{tipo}: R${abs(valor):.2f} em {data_hora}")
    print("--------------------------------------------")
    print(f"Saldo atual: R${saldo:.2f}")
    print("Pressione qualquer tecla para continuar...")
    msvcrt.getch()
    os.system("cls")
    print("============================================")


while True:
    print(opcoes)
    escolha = input("Insira uma opção:\n").upper()
    if escolha == "D":
        logica_deposito()
        
    elif escolha == "U":
        logica_cadastro()
        
    elif escolha == "C":
        cpf = input("Informe o CPF do usuário para criar/associar conta:\n").strip()
        if cpf in usuarios:
            logica_criar_conta_corrente(cpf)
        else:
            print("CPF não cadastrado!")
            
    elif escolha == "S":
        logica_saque()
        
    elif escolha == "E":
        logica_extrato()
        
    elif escolha == "0":
        break
    else:
        print("Opção inválida!")
