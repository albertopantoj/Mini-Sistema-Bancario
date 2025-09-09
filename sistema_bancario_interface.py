import tkinter as tk
from tkinter import messagebox, simpledialog

conta_bancaria = []
saques_bancarios = []
LIMITE_SAQUES_DIARIOS = 3
saques_realizados = 0

# Funções do sistema
def logica_deposito():
    global conta_bancaria
    try:
        deposito = simpledialog.askfloat("Depósito", "Digite o valor a depositar:")
        if deposito is None:
            return  # usuário cancelou
        if deposito >= 1:
            conta_bancaria.append(deposito)
            messagebox.showinfo("Depósito", f"Depósito de R${deposito:.2f} realizado com sucesso!")
        else:
            messagebox.showwarning("Erro", "Valor inválido para depósito!")
    except Exception:
        messagebox.showerror("Erro", "Entrada inválida! Digite apenas números.")

def logica_saque():
    global saques_realizados, conta_bancaria, saques_bancarios
    try:
        saque = simpledialog.askfloat("Saque", "Digite o valor a sacar:")
        if saque is None:
            return
        saldo = sum(conta_bancaria)

        if saques_realizados >= LIMITE_SAQUES_DIARIOS:
            messagebox.showwarning("Erro", "Limite de saques diários atingido!")
        elif saque > 500:
            messagebox.showwarning("Erro", "Limite de saque é de R$500,00 por operação!")
        elif saque > saldo:
            messagebox.showwarning("Erro", "Saldo insuficiente!")
        elif saque <= 0:
            messagebox.showwarning("Erro", "Valor inválido!")
        else:
            conta_bancaria.append(-saque)
            saques_bancarios.append(saque)
            saques_realizados += 1
            messagebox.showinfo("Saque", f"Saque de R${saque:.2f} realizado com sucesso!")
    except Exception:
        messagebox.showerror("Erro", "Entrada inválida! Digite apenas números.")

def logica_extrato():
    saldo = sum(conta_bancaria)
    extrato = "📑 Extrato Bancário\n\n"
    if not conta_bancaria:
        extrato += "Nenhuma movimentação realizada."
    else:
        for mov in conta_bancaria:
            if mov > 0:
                extrato += f"Depósito: R${mov:.2f}\n"
            else:
                extrato += f"Saque:   R${abs(mov):.2f}\n"
    extrato += f"\n💵 Saldo atual: R${saldo:.2f}"
    messagebox.showinfo("Extrato", extrato)

# Interface gráfica
janela = tk.Tk()
janela.title("💳 Sistema Bancário")
janela.geometry("300x300")

tk.Label(janela, text="Sistema Bancário", font=("Arial", 16, "bold")).pack(pady=10)

btn_deposito = tk.Button(janela, text="💰 Depositar", width=20, command=logica_deposito)
btn_deposito.pack(pady=5)

btn_saque = tk.Button(janela, text="💸 Sacar", width=20, command=logica_saque)
btn_saque.pack(pady=5)

btn_extrato = tk.Button(janela, text="📑 Extrato", width=20, command=logica_extrato)
btn_extrato.pack(pady=5)

btn_sair = tk.Button(janela, text="❌ Sair", width=20, command=janela.destroy)
btn_sair.pack(pady=20)

janela.mainloop()
