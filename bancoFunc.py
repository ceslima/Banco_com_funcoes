# :: Sistema Bancário v3.1 - Com Exclusão Segura de Contas

# Módulos nativos do Python
import os
import platform
import time
from datetime import datetime
import uuid
import random
import json
import getpass

# --- Constantes do Sistema ---
LIMITE_SAQUES_DIARIOS = 3
LIMITE_VALOR_POR_SAQUE = 500.00
NOME_ARQUIVO_DADOS = "banco_dados.json"
ADMIN_USER = "ceslima"
ADMIN_PASS = "12345"

# --- Funções Utilitárias (limpar_tela, pausar_e_limpar) ---
def limpar_tela():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def pausar_e_limpar():
    input("\nPressione Enter para continuar...")
    limpar_tela()

# --- Funções de Gerenciamento de Dados (Persistência) ---
def carregar_dados():
    try:
        with open(NOME_ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_dados(dados):
    with open(NOME_ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# --- Funções de Cadastro e Administração ---

# ... (função cadastrar_nova_conta inalterada) ...
def cadastrar_nova_conta(dados_banco):
    limpar_tela()
    print("--- Cadastro de Nova Conta ---")
    nome = input("Digite o nome completo do titular: ").strip()
    senha = getpass.getpass("Crie uma senha de acesso: ")
    if not nome or not senha:
        print("\nERRO: Nome e senha não podem ser vazios.")
        return dados_banco
    nova_conta = {
        "id_conta": str(uuid.uuid4()),
        "numero_conta": str(random.randint(10000, 99999)),
        "nome": nome, "senha": senha, "saldo": 0.0, "extrato": [],
        "numero_saques_hoje": 0, "data_cadastro": datetime.now().isoformat()
    }
    dados_banco.append(nova_conta)
    print("\n--- Conta Criada com Sucesso! ---")
    print(f"Titular: {nome}")
    print(f"Anote o seu Número da Conta para acesso: {nova_conta['numero_conta']}")
    return dados_banco

def listar_contas(dados_banco):
    limpar_tela()
    print("--- Lista de Contas Cadastradas ---")
    if not dados_banco:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in dados_banco:
            print(f"Titular: {conta['nome']} | Conta Nº: {conta['numero_conta']} | Saldo: R$ {conta['saldo']:.2f}")
    pausar_e_limpar()

# --- NOVA FUNÇÃO: Deletar conta ---
def deletar_conta(dados_banco):
    """
    Busca uma conta pelo número e a remove após verificação de saldo e confirmação.
    """
    limpar_tela()
    print("--- Exclusão de Conta ---")
    num_conta_alvo = input("Digite o número da conta que deseja deletar: ")

    conta_encontrada = None
    indice_conta = -1

    for i, conta in enumerate(dados_banco):
        if conta['numero_conta'] == num_conta_alvo:
            conta_encontrada = conta
            indice_conta = i
            break
    
    if not conta_encontrada:
        print("\nERRO: Conta não encontrada.")
        pausar_e_limpar()
        return dados_banco

    # 1. Verificar se o saldo é maior que zero
    if conta_encontrada['saldo'] > 0:
        print("\nERRO: Não é possível deletar a conta.")
        print(f"A conta de {conta_encontrada['nome']} possui um saldo de R$ {conta_encontrada['saldo']:.2f}.")
        print("É necessário que o titular realize o saque do valor total antes da exclusão.")
        pausar_e_limpar()
        return dados_banco

    # 2. Se o saldo for zero, pedir confirmação
    print("\n--- Confirmação de Exclusão ---")
    print(f"Titular:         {conta_encontrada['nome']}")
    print(f"Número da Conta: {conta_encontrada['numero_conta']}")
    print(f"Saldo:           R$ {conta_encontrada['saldo']:.2f}")
    
    confirmacao = input("\nDeseja realmente deletar a conta? (sim/não): ").lower()

    # 3. Deletar se confirmado
    if confirmacao == 'sim':
        dados_banco.pop(indice_conta)
        print("\nConta deletada com sucesso.")
    else:
        print("\nOperação de exclusão cancelada.")
    
    pausar_e_limpar()
    return dados_banco


# ... (Funções do usuário: depositar, sacar, exibir_extrato inalteradas) ...
def depositar(usuario):
    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        if valor > 0:
            usuario['saldo'] += valor
            transacao = {"tipo": "Depósito", "valor": valor, "data": datetime.now().isoformat()}
            usuario['extrato'].append(transacao)
            print("\nDepósito realizado com sucesso!")
        else: print("\nERRO: O valor deve ser positivo.")
    except ValueError: print("\nERRO: Valor inválido.")
    pausar_e_limpar()
    return usuario

def sacar(usuario):
    try:
        valor = float(input("Informe o valor do saque: R$ "))
        excedeu_saldo = valor > usuario['saldo']
        excedeu_limite_saque = valor > LIMITE_VALOR_POR_SAQUE
        excedeu_num_saques = usuario['numero_saques_hoje'] >= LIMITE_SAQUES_DIARIOS
        if excedeu_saldo: print("\nERRO: Saldo insuficiente.")
        elif excedeu_limite_saque: print(f"\nERRO: Limite por saque é de R$ {LIMITE_VALOR_POR_SAQUE:.2f}.")
        elif excedeu_num_saques: print("\nERRO: Limite de saques diários atingido.")
        elif valor <= 0: print("\nERRO: O valor deve ser positivo.")
        else:
            usuario['saldo'] -= valor
            usuario['numero_saques_hoje'] += 1
            transacao = {"tipo": "Saque", "valor": valor, "data": datetime.now().isoformat()}
            usuario['extrato'].append(transacao)
            print("\nSaque realizado com sucesso!")
    except ValueError: print("\nERRO: Valor inválido.")
    pausar_e_limpar()
    return usuario

def exibir_extrato(usuario):
    print(f"\n--- Extrato da Conta {usuario['numero_conta']} ---")
    if not usuario['extrato']: print("Não foram realizadas movimentações.")
    else:
        for t in usuario['extrato']:
            data = datetime.fromisoformat(t['data']).strftime("%d/%m/%Y %H:%M:%S")
            print(f"{data} - {t['tipo']:<10} R$ {t['valor']:.2f}")
    print("-" * 40)
    print(f"Saldo Atual: R$ {usuario['saldo']:.2f}")
    print("-" * 40)
    pausar_e_limpar()

# --- Menus e Fluxo Principal (com menu admin atualizado) ---
def menu_usuario(usuario, dados_banco):
    # (código inalterado)
    while True:
        limpar_tela()
        print(f"Olá, {usuario['nome'].split()[0]}! | Conta: {usuario['numero_conta']} | Saldo: R$ {usuario['saldo']:.2f}")
        opcao = input("\n[d] Depositar\n[s] Sacar\n[e] Extrato\n[q] Sair (Logout)\n=> ").lower()
        if opcao == 'd': usuario = depositar(usuario)
        elif opcao == 's': usuario = sacar(usuario)
        elif opcao == 'e': exibir_extrato(usuario)
        elif opcao == 'q':
            for i, conta in enumerate(dados_banco):
                if conta['id_conta'] == usuario['id_conta']:
                    dados_banco[i] = usuario; break
            print("Saindo da sua conta..."); time.sleep(1)
            return dados_banco
        else: print("Opção inválida.")

def menu_administrador(dados_banco):
    """Exibe o menu de funções do administrador, agora com a opção de deletar."""
    while True:
        limpar_tela()
        print("--- Painel do Administrador ---")
        opcao = input("\n[c] Criar Nova Conta\n[l] Listar Contas\n[d] Deletar Conta\n[q] Sair (Logout)\n=> ").lower()

        if opcao == 'c': dados_banco = cadastrar_nova_conta(dados_banco)
        elif opcao == 'l': listar_contas(dados_banco)
        elif opcao == 'd': dados_banco = deletar_conta(dados_banco) # Nova opção
        elif opcao == 'q':
            print("Saindo do painel de administrador...")
            time.sleep(1)
            return dados_banco
        else:
            print("Opção inválida.")

# ... (funções realizar_login e main inalteradas) ...
def realizar_login(dados_banco):
    print("--- Bem-vindo ao Banco  ---")
    login = input("Digite o usuário (ou nº da conta): ")
    senha = getpass.getpass("Digite a senha: ")
    if login == ADMIN_USER and senha == ADMIN_PASS: return "admin"
    for usuario in dados_banco:
        if usuario['numero_conta'] == login and usuario['senha'] == senha:
            return usuario
    return None

def main():
    dados_banco = carregar_dados()
    while True:
        limpar_tela()
        ator = realizar_login(dados_banco)
        if ator == "admin": dados_banco = menu_administrador(dados_banco)
        elif isinstance(ator, dict): dados_banco = menu_usuario(ator, dados_banco)
        else: print("\nUsuário ou senha inválidos."); time.sleep(2)
        salvar_dados(dados_banco)

if __name__ == "__main__":
    main()
  
