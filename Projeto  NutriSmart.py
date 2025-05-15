import sqlite3
import re
from datetime import datetime

# Conexão com banco SQLite
conn = sqlite3.connect('nutricao.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        email TEXT PRIMARY KEY,
        senha TEXT NOT NULL,
        peso REAL NOT NULL,
        altura REAL NOT NULL,
        sexo TEXT NOT NULL,
        dieta TEXT NOT NULL,
        imc REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS alimentos (
        nome TEXT PRIMARY KEY,
        calorias REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS refeicoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email_usuario TEXT,
        alimento TEXT,
        quantidade_gramas REAL,
        data TEXT,
        FOREIGN KEY (email_usuario) REFERENCES usuarios(email)
    )
''')

conn.commit()

# ----------------- Funções Auxiliares ----------------- #

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

def escolher_dieta():
    opcoes = ["Low carb", "Cetogênica", "Hiperproteica", "Bulking"]
    while True:
        print("\nEscolha sua dieta:")
        for i, dieta in enumerate(opcoes, 1):
            print(f"{i}. {dieta}")
        escolha = input("Digite o número da dieta: ")
        if escolha.isdigit() and 1 <= int(escolha) <= 4:
            return opcoes[int(escolha) - 1]
        else:
            print("❌ Opção inválida! Tente novamente.")

# ----------------- Cadastro ----------------- #

def registrar_usuario():
    print("\n=== Cadastro de Usuário ===")
    while True:
        email = input("E-mail: ").strip()
        if not validar_email(email):
            print("❌ E-mail inválido!")
            continue
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            print("❌ E-mail já está cadastrado!")
            continue
        break

    while True:
        senha = input("Senha: ").strip()
        if senha == "":
            print("❌ A senha não pode ser vazia!")
        else:
            break

    try:
        peso = float(input("Peso (kg): "))
        altura = float(input("Altura (m): "))
        if peso <= 0 or altura <= 0:
            print("❌ Peso e altura devem ser maiores que zero.")
            return
    except ValueError:
        print("❌ Digite apenas números válidos para peso e altura.")
        return

    sexo = input("Sexo (M/F): ").strip().upper()
    if sexo not in ['M', 'F']:
        print("❌ Sexo inválido! Use apenas 'M' ou 'F'.")
        return

    dieta = escolher_dieta()
    imc = calcular_imc(peso, altura)

    cursor.execute('''
        INSERT INTO usuarios (email, senha, peso, altura, sexo, dieta, imc)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (email, senha, peso, altura, sexo, dieta, imc))
    conn.commit()
    print(f"✅ Usuário cadastrado com sucesso! Seu IMC é {imc}")

# ----------------- Login ----------------- #

def login():
    print("\n=== Login ===")
    while True:
        email = input("E-mail: ").strip()
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        if not resultado:
            print("❌ E-mail não encontrado. Tente novamente.")
            continue

        senha_digitada = input("Senha: ").strip()
        if senha_digitada != resultado[0]:
            print("❌ Senha incorreta. Tente novamente.")
            continue

        print("✅ Login realizado com sucesso!")
        return email

# ----------------- Refeição ----------------- #

def registrar_refeicao(email_usuario):
    print("\n🍽️ Registro de Refeição Diária")
    alimento = input("Nome do alimento: ").strip().lower()

    cursor.execute("SELECT calorias FROM alimentos WHERE nome = ?", (alimento,))
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ Alimento desconhecido! Peça ao administrador para cadastrá-lo.")
        return

    try:
        quantidade = float(input("Quantidade consumida (em gramas): "))
        if quantidade <= 0:
            print("❌ Quantidade deve ser maior que zero.")
            return
    except ValueError:
        print("❌ Digite apenas números válidos.")
        return

    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO refeicoes (email_usuario, alimento, quantidade_gramas, data)
        VALUES (?, ?, ?, ?)
    ''', (email_usuario, alimento, quantidade, data))
    conn.commit()
    print("✅ Refeição registrada com sucesso!")

def ver_refeicoes(email_usuario):
    print("\n=== Refeições Registradas ===")
    cursor.execute("SELECT id, alimento, quantidade_gramas, data FROM refeicoes WHERE email_usuario = ?", (email_usuario,))
    refeicoes = cursor.fetchall()
    if refeicoes:
        for r in refeicoes:
            print(f"- ID: {r[0]} | Alimento: {r[1]} | Quantidade: {r[2]}g | Data: {r[3]}")
    else:
        print("❌ Nenhuma refeição registrada.")

# ----------------- Usuário Logado ----------------- #

def menu_usuario_logado(email):
    while True:
        print(f"\n🔐 Bem-vindo, {email}")
        print("1. Ver meus dados")
        print("2. Registrar refeição")
        print("3. Ver refeições")
        print("4. Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cursor.execute("SELECT peso, altura, sexo, dieta, imc FROM usuarios WHERE email = ?", (email,))
            dados = cursor.fetchone()
            print(f"\n📄 Seus dados:")
            print(f"Peso: {dados[0]} kg | Altura: {dados[1]} m")
            print(f"Sexo: {dados[2]} | Dieta: {dados[3]} | IMC: {dados[4]}")
        elif escolha == "2":
            registrar_refeicao(email)
        elif escolha == "3":
            ver_refeicoes(email)
        elif escolha == "4":
            print("🔒 Logout realizado.")
            break
        else:
            print("❌ Opção inválida!")

# ----------------- Administrador ----------------- #

def registrar_alimento():
    print("\n=== Cadastro de Alimento ===")
    nome = input("Nome do alimento: ").strip().lower()
    cursor.execute("SELECT * FROM alimentos WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("⚠️ Alimento já cadastrado.")
        return
    try:
        calorias = float(input("Calorias por 100g: "))
        if calorias <= 0:
            print("❌ Valor inválido.")
            return
    except ValueError:
        print("❌ Valor inválido.")
        return
    cursor.execute("INSERT INTO alimentos (nome, calorias) VALUES (?, ?)", (nome, calorias))
    conn.commit()
    print("✅ Alimento cadastrado!")

def ver_alimentos():
    print("\n📋 Alimentos cadastrados:")
    cursor.execute("SELECT nome, calorias FROM alimentos")
    alimentos = cursor.fetchall()
    if alimentos:
        for a in alimentos:
            print(f"- {a[0].capitalize()} | {a[1]} kcal")
    else:
        print("⚠️ Nenhum alimento cadastrado.")

def excluir_alimento():
    print("\n🗑️ Excluir Alimento do Cadastro")
    nome = input("Digite o nome do alimento que deseja excluir: ").strip().lower()
    
    cursor.execute("SELECT * FROM alimentos WHERE nome = ?", (nome,))
    if not cursor.fetchone():
        print("❌ Alimento não encontrado.")
        return

    confirmacao = input(f"Tem certeza que deseja excluir o alimento '{nome}'? (s/n): ").strip().lower()
    if confirmacao == "s":
        cursor.execute("DELETE FROM alimentos WHERE nome = ?", (nome,))
        conn.commit()
        print("✅ Alimento excluído com sucesso!")
    else:
        print("❌ Exclusão cancelada.")

def menu_administrador():
    senha = input("Senha do administrador: ")
    if senha != "admin123":
        print("❌ Senha incorreta!")
        return

    while True:
        print("\n🔧 Menu do Administrador")
        print("1. Inserir alimento")
        print("2. Ver alimentos")
        print("3. Ver usuários")
        print("4. Excluir alimento")
        print("5. Sair")
        escolha = input("Escolha: ")

        if escolha == "1":
            registrar_alimento()
        elif escolha == "2":
            ver_alimentos()
        elif escolha == "3":
            cursor.execute("SELECT email, dieta, imc FROM usuarios")
            for u in cursor.fetchall():
                print(f"- {u[0]} | Dieta: {u[1]} | IMC: {u[2]}")
        elif escolha == "4":
            excluir_alimento()
        elif escolha == "5":
            print("🚪 Saindo do modo administrador.")
            break
        else:
            print("❌ Opção inválida!")

# ----------------- Menu Principal ----------------- #

def menu_principal():
    while True:
        print("\n===== MENU =====")
        print("1. Sou Usuário")
        print("2. Sou Administrador")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            while True:
                print("\n--- Menu do Usuário ---")
                print("1. Registrar novo usuário")
                print("2. Fazer login")
                print("3. Voltar")
                escolha = input("Escolha uma opção: ")
                if escolha == "1":
                    registrar_usuario()
                elif escolha == "2":
                    email = login()
                    if email:
                        menu_usuario_logado(email)
                elif escolha == "3":
                    break
                else:
                    print("❌ Opção inválida.")
        elif opcao == "2":
            menu_administrador()
        elif opcao == "3":
            print("👋 Saindo do sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida!")

# Executar sistema
menu_principal()
conn.close()
