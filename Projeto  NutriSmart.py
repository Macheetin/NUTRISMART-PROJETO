import sqlite3
import re
from datetime import datetime
import random

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
        imc REAL NOT NULL,
        pergunta_seguranca TEXT NOT NULL,
        resposta_seguranca TEXT NOT NULL
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS registro_refeicoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        refeicao TEXT NOT NULL,
        calorias INTEGER,
        data TEXT NOT NULL
    )
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS suporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    mensagem TEXT,
    resposta TEXT DEFAULT NULL
)
''')

conn.commit()

# ----------------- Funções Auxiliares ----------------- #

# Validar email
def validar_email(email):
    """Valida se o e-mail fornecido segue o padrão de e-mail."""
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

# Calculo de imc
def calcular_imc(peso, altura):
    """Calcula o IMC (Índice de Massa Corporal) com base no peso e altura."""
    return round(peso / (altura ** 2), 2)

# Escolha de dieta
def escolher_dieta():
    """Solicita ao usuário que escolha um tipo de dieta entre as opções disponíveis."""
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
    """Solicita informações ao usuário e registra um novo usuário no banco de dados."""
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

    print("\nEscolha uma pergunta de segurança:")
    perguntas = [
        "Qual é o nome do seu primeiro animal de estimação?",
        "Qual é a sua comida favorita?",
        "Qual cidade você nasceu?"
    ]
    for i, p in enumerate(perguntas, 1):
        print(f"{i}. {p}")
    while True:
        escolha = input("Digite o número da pergunta: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(perguntas):
            pergunta = perguntas[int(escolha) - 1]
            break
        else:
            print("❌ Escolha inválida!")

    resposta = input("Digite a resposta para a pergunta de segurança: ").strip().lower()

    cursor.execute('''
        INSERT INTO usuarios (email, senha, peso, altura, sexo, dieta, imc, pergunta_seguranca, resposta_seguranca)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (email, senha, peso, altura, sexo, dieta, imc, pergunta, resposta))
    conn.commit()
    print(f"✅ Usuário cadastrado com sucesso! Seu IMC é {imc}")

# ----------------- Login ----------------- #

def recuperar_senha():
    """Permite que o usuário recupere a senha por meio da pergunta de segurança cadastrada."""
    print("\n🔐 Recuperação de Senha")
    email = input("Digite seu e-mail cadastrado: ").strip()
    cursor.execute("SELECT pergunta_seguranca, resposta_seguranca, senha FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ E-mail não encontrado!")
        return

    pergunta, resposta_correta, senha = resultado
    print(f"Pergunta de segurança: {pergunta}")
    resposta_usuario = input("Sua resposta: ").strip().lower()
    if resposta_usuario == resposta_correta:
        print(f"✅ Sua senha é: {senha}")
    else:
        print("❌ Resposta incorreta!")

def login():
    """Realiza o login do usuário verificando o e-mail e a senha cadastrados."""
    print("\n=== Login ===")
    while True:
        email = input("E-mail: ").strip()
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        if not resultado:
            print("❌ E-mail não encontrado. Tente novamente.")
            return

        senha_digitada = input("Senha: ").strip()
        if senha_digitada != resultado[0]:
            print("❌ Senha incorreta.")
            escolha = input("Deseja recuperar sua senha? (s/n): ").strip().lower()
            if escolha == 's':
                print("\n🔐 Recuperação de Senha")
                cursor.execute("SELECT pergunta_seguranca, resposta_seguranca, senha FROM usuarios WHERE email = ?", (email,))
                resultado_rec = cursor.fetchone()
                pergunta, resposta_correta, senha_real = resultado_rec
                print(f"Pergunta de segurança: {pergunta}")
                resposta_usuario = input("Sua resposta: ").strip().lower()
                if resposta_usuario == resposta_correta:
                    print(f"✅ Sua senha é: {senha_real}")
                else:
                    print("❌ Resposta incorreta!")
            else:
                print("Tente novamente.")
            continue

        print("✅ Login realizado com sucesso!")
        return email
    
# ----------------- Funções do menu do usuário ----------------- #

# --- Refeição diária --- #

# Registrar refeições
def registrar_refeicao(email_usuario):
    """Registra uma refeição consumida, informando o alimento, quantidade e data."""
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

# Ver refeições registradas
def ver_refeicoes(email_usuario):
    """Exibe todas as refeições registradas por um usuário específico."""
    print("\n=== Refeições Registradas ===")
    cursor.execute("SELECT id, alimento, quantidade_gramas, data FROM refeicoes WHERE email_usuario = ?", (email_usuario,))
    refeicoes = cursor.fetchall()
    if refeicoes:
        for r in refeicoes:
            print(f"- ID: {r[0]} | Alimento: {r[1]} | Quantidade: {r[2]}g | Data: {r[3]}")
    else:
        print("❌ Nenhuma refeição registrada.")


#--- Alimentos Recomendados --- #

# Ver alimentos recomendados por dieta
def ver_alimentos_recomendados_usuario(email):
    """Mostra ao usuário alimentos recomendados com base na dieta selecionada."""
    cursor.execute("SELECT dieta FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ Usuário não encontrado.")
        return

    dieta_usuario = resultado[0]

    recomendacoes = {
        "Low carb": [
            "Ovos", "Abacate", "Peixes", "Nozes", "Couve-flor", "Espinafre", "Brócolis", "Azeite de oliva",
            "Amêndoas", "Queijo", "Cogumelos", "Carne bovina", "Salmão", "Aspargos", "Alface", "Cenoura",
            "Tomate", "Pepino", "Pimentão", "Berinjela", "Abobrinha", "Castanha-do-pará", "Aipo", "Azeitona",
            "Sementes de chia", "Sementes de linhaça", "Coco", "Framboesa", "Morango", "Repolho", "Alcachofra",
            "Cebola", "Alho", "Rúcula", "Manjericão", "Salsinha", "Endívia", "Alcaparras", "Pimenta", "Ervilha-torta",
            "Limão", "Laranja", "Carne de porco", "Frango", "Iogurte natural", "Ricota", "Chá verde", "Água com gás",
            "Vinagre de maçã", "Café"
        ],
        "Cetogênica": [
            "Bacon", "Queijo cheddar", "Carne de cordeiro", "Manteiga", "Nata", "Óleo de coco", "Salmão selvagem",
            "Ovos caipiras", "Espinafre", "Couve", "Brócolis", "Couve-flor", "Abacate", "Nozes", "Castanhas",
            "Sementes de abóbora", "Azeitonas", "Chá de hortelã", "Café sem açúcar", "Queijo parmesão",
            "Frango caipira", "Carne moída", "Camarão", "Atum", "Aspargos", "Abobrinha", "Cogumelos", "Alho",
            "Cebola", "Pimenta", "Ervas frescas", "Alface", "Rúcula", "Salsa", "Manjericão", "Nata fresca",
            "Creme de leite", "Óleo MCT", "Chá de camomila", "Queijo mozzarella", "Carne bovina", "Carne de porco",
            "Peixes gordurosos", "Sementes de chia", "Sementes de linhaça", "Abacate", "Limão", "Vinagre de maçã",
            "Água mineral"
        ],
        "Hiperproteica": [
            "Peito de frango", "Clara de ovo", "Carne magra", "Peixes", "Queijo cottage", "Iogurte grego",
            "Atum", "Carne bovina magra", "Salmão", "Ovos inteiros", "Tofu", "Tempeh", "Lentilhas", "Feijão",
            "Quinoa", "Amêndoas", "Nozes", "Sementes de abóbora", "Camarão", "Proteína isolada", "Leite desnatado",
            "Ricota", "Brócolis", "Couve-flor", "Espinafre", "Cenoura", "Abobrinha", "Alface", "Tomate",
            "Pepino", "Pimentão", "Azeite de oliva", "Chá verde", "Água"
        ],
        "Bulking": [
            "Arroz integral", "Batata doce", "Aveia", "Massas integrais", "Carne vermelha", "Peito de frango",
            "Ovos", "Salmão", "Atum", "Quinoa", "Feijão", "Grão-de-bico", "Lentilha", "Leite integral",
            "Iogurte natural", "Queijo", "Nozes", "Amêndoas", "Castanha-do-pará", "Abacate", "Banana",
            "Morangos", "Espinafre", "Brócolis", "Cenoura", "Abobrinha", "Tomate", "Pepino", "Pimentão",
            "Azeite de oliva", "Manteiga de amendoim", "Chá verde", "Água", "Mel", "Chocolate amargo",
            "Batata inglesa", "Milho", "Pão integral", "Sementes de chia", "Sementes de linhaça", "Ervilha"
        ]
    }

    alimentos_recomendados = recomendacoes.get(dieta_usuario, [])

    if not alimentos_recomendados:
        print("❌ Nenhum alimento recomendado encontrado para esta dieta.")
        return

    aleatorios = random.sample(alimentos_recomendados, k=4)

    print(f"\n🍽️ 4 Alimentos aleatórios recomendados para a dieta {dieta_usuario}:")
    for alimento in aleatorios:
        print(f"- {alimento}")

# --- Encerrar o Dia --- #
from datetime import date

# Encerrar o dia e ganhar seu feedback em relação a sua meta
def encerrar_dia(email_usuario):
    """Calcula e exibe o total calórico consumido no dia e verifica se está dentro da meta."""
    print("\n📅 Encerramento do Dia")
    hoje = date.today().strftime("%Y-%m-%d")

    cursor.execute("SELECT dieta, peso, altura FROM usuarios WHERE email = ?", (email_usuario,))
    resultado = cursor.fetchone()
    if not resultado:
        print("❌ Usuário não encontrado.")
        return
    dieta_usuario, peso, altura = resultado

    cursor.execute('''
        SELECT r.alimento, r.quantidade_gramas, a.calorias
        FROM refeicoes r
        JOIN alimentos a ON r.alimento = a.nome
        WHERE r.email_usuario = ? AND date(r.data) = ?
    ''', (email_usuario, hoje))
    refeicoes_hoje = cursor.fetchall()

    if not refeicoes_hoje:
        print("❌ Nenhuma refeição registrada para hoje.")
        return

    calorias_totais = 0
    for alimento, quantidade, cal_100g in refeicoes_hoje:
        calorias_totais += (cal_100g * quantidade) / 100

    calorias_totais = round(calorias_totais, 2)

    metas = {
        "Low carb": 25 * peso,
        "Cetogênica": 27 * peso,
        "Hiperproteica": 30 * peso,
        "Bulking": 35 * peso
    }

    meta_calorias = metas.get(dieta_usuario, 30 * peso)

    print(f"\nDieta: {dieta_usuario}")
    print(f"Calorias consumidas hoje: {calorias_totais} kcal")
    print(f"Meta calórica diária aproximada: {meta_calorias} kcal")

    if calorias_totais < meta_calorias * 0.9:
        print("⚠️ Você consumiu menos calorias que o recomendado para sua dieta hoje.")
    elif calorias_totais > meta_calorias * 1.1:
        print("⚠️ Você consumiu mais calorias que o recomendado para sua dieta hoje.")
    else:
        print("✅ Consumo calórico dentro da meta para hoje. Bom trabalho!")

# --- Ranking de alimentos consumidos --- #

# Ver ranking de alimentos mais consumidos pelo usuário
def ranking_alimentos_mais_consumidos(email_usuario):
    """Exibe os alimentos mais consumidos por um usuário em ordem decrescente."""
    print("\n🏆 Ranking dos alimentos mais consumidos:")
    cursor.execute('''
        SELECT alimento, SUM(quantidade_gramas) as total_gramas
        FROM refeicoes
        WHERE email_usuario = ?
        GROUP BY alimento
        ORDER BY total_gramas DESC
        LIMIT 10
    ''', (email_usuario,))
    ranking = cursor.fetchall()

    if not ranking:
        print("❌ Nenhuma refeição registrada para gerar o ranking.")
        return

    for i, (alimento, total) in enumerate(ranking, 1):
        print(f"{i}. {alimento.capitalize()} - {total:.2f} g")

#---- Lembretes e Alertas--- #

# Função pra consultar se o usuário ja registrou alimentação no dia
def pegar_registros_do_dia(email_usuario):
    """Retorna os registros de refeições feitas pelo usuário no dia atual."""
    from datetime import datetime
    hoje = datetime.now().date()
    cursor.execute("SELECT * FROM registro_refeicoes WHERE email = ? AND data = ?", (email_usuario, str(hoje)))
    registros = cursor.fetchall()
    return registros

# Registro diario pra lembretes
def submenu_lembretes(email_usuario):
    """Exibe lembretes ao usuário sobre alimentação e hidratação do dia."""
    registros_diarios = pegar_registros_do_dia(email_usuario)
    
    print("\n--- Lembretes e Alertas ---")
    
    # Avisar se já comeu algo no dia
    if not registros_diarios:
        print("Atenção! Você ainda não registrou nenhuma refeição hoje. Não esqueça de se alimentar!")
    else:
        print(f"Você já registrou {len(registros_diarios)} refeição(ões) hoje. Continue assim!")
    
    # Lembrete para beber água
    print("Lembrete: Beba pelo menos 2 litros de água ao longo do dia.")
    
    input("\nPressione Enter para voltar ao menu principal...")

# --- Contato com administrador --- #

# Enviar mensagem para o administrador
def contatar_administrador(email_usuario):
    """Permite que o usuário envie uma mensagem ao administrador do sistema."""
    print("\n--- Contato com o Administrador ---")
    mensagem = input("Digite sua dúvida, sugestão ou mensagem: ")

    if mensagem.strip() == "":
        print("❌ Mensagem vazia não pode ser enviada.")
        return

    cursor.execute("INSERT INTO suporte (email, mensagem) VALUES (?, ?)", (email_usuario, mensagem))
    conn.commit()

    print("✅ Mensagem enviada com sucesso! O administrador responderá em breve.")

    # Ver resposta do administrador
def visualizar_respostas(email_usuario):
    """Exibe respostas enviadas pelo administrador ao usuário."""
    print("\n--- Respostas do Administrador ---")
    
    cursor.execute("SELECT mensagem, resposta FROM suporte WHERE email = ?", (email_usuario,))
    registros = cursor.fetchall()

    if not registros:
        print("📭 Você ainda não enviou nenhuma mensagem ao administrador.")
    else:
        for i, (mensagem, resposta) in enumerate(registros, start=1):
            print(f"\n📨 Mensagem {i}: {mensagem}")
            if resposta:
                print(f"🟢 Resposta: {resposta}")
            else:
                print("🕐 Aguardando resposta do administrador. Por favor, aguarde pacientemente.")
    
    input("\nPressione Enter para voltar ao menu...")

# Menu de suporte do usuario
def submenu_ajuda_suporte_usuario(email_usuario):
    """Menu que oferece opções de suporte ao usuário como enviar dúvidas ou ver respostas."""
    while True:
        print("\n=== Ajuda e Suporte ===")
        print("1. Contatar o administrador")
        print("2. Visualizar respostas")
        print("3. Voltar ao menu anterior")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            contatar_administrador(email_usuario)
        elif escolha == "2":
            visualizar_respostas(email_usuario)
        elif escolha == "3":
            break
        else:
            print("❌ Opção inválida!")

# --- Editar meus dados --- #
def editar_meus_dados(email_usuario):
    """Permite ao usuário atualizar peso, altura, dieta e recalcular IMC."""
    print("\n=== Editar Meus Dados ===")

    try:
        novo_peso = float(input("Novo peso (kg): "))
        nova_altura = float(input("Nova altura (m): "))
        if novo_peso <= 0 or nova_altura <= 0:
            print("❌ Peso e altura devem ser maiores que zero.")
            return
    except ValueError:
        print("❌ Digite valores numéricos válidos para peso e altura.")
        return

    nova_dieta = escolher_dieta()
    novo_imc = calcular_imc(novo_peso, nova_altura)

    cursor.execute('''
        UPDATE usuarios
        SET peso = ?, altura = ?, dieta = ?, imc = ?
        WHERE email = ?
    ''', (novo_peso, nova_altura, nova_dieta, novo_imc, email_usuario))
    conn.commit()

    print("✅ Dados atualizados com sucesso!")
    print(f"📊 Novo IMC: {novo_imc}")


# ----------------- Funções do Administrador ----------------- #

# Cadastrar alimentos no banco de dados
def cadastrar_alimento():
    """Adiciona um novo alimento ao banco de dados com suas calorias."""
    print("\n=== Inserir novo alimento ===")
    nome = input("Nome do alimento: ").strip().lower()
    try:
        calorias = float(input("Calorias por 100g: "))
        if calorias <= 0:
            print("❌ Calorias devem ser maior que zero.")
            return
    except ValueError:
        print("❌ Digite um número válido para calorias.")
        return

    cursor.execute("SELECT * FROM alimentos WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("❌ Alimento já cadastrado!")
        return

    cursor.execute("INSERT INTO alimentos (nome, calorias) VALUES (?, ?)", (nome, calorias))
    conn.commit()
    print(f"✅ Alimento '{nome}' cadastrado com sucesso.")

# Ver alimentos cadastrados no banco de dados
def ver_alimentos():
    """Lista todos os alimentos cadastrados e suas respectivas calorias."""
    print("\n=== Lista de alimentos cadastrados ===")
    cursor.execute("SELECT nome, calorias FROM alimentos")
    alimentos = cursor.fetchall()
    if alimentos:
        for a in alimentos:
            print(f"- {a[0]} | {a[1]} cal por 100g")
    else:
        print("❌ Nenhum alimento cadastrado.")

# Excluir alimento do banco de dados
def excluir_alimento():
    """Exclui um alimento específico do banco de dados conforme nome informado."""
    print("\n=== Excluir alimento ===")
    nome = input("Nome do alimento para excluir: ").strip().lower()
    cursor.execute("SELECT * FROM alimentos WHERE nome = ?", (nome,))
    if not cursor.fetchone():
        print("❌ Alimento não encontrado.")
        return
    cursor.execute("DELETE FROM alimentos WHERE nome = ?", (nome,))
    conn.commit()
    print(f"✅ Alimento '{nome}' excluído com sucesso.")


# Ver usuarios cadastrados no banco de dados
def ver_usuarios():
    """Exibe todos os usuários cadastrados com dados como peso, altura e dieta."""
    print("\n=== Usuários Cadastrados ===")
    cursor.execute("SELECT email, peso, altura, sexo, dieta, imc FROM usuarios")
    usuarios = cursor.fetchall()
    if usuarios:
        for u in usuarios:
            print(f"- Email: {u[0]} | Peso: {u[1]} kg | Altura: {u[2]} m | Sexo: {u[3]} | Dieta: {u[4]} | IMC: {u[5]}")
    else:
        print("❌ Nenhum usuário cadastrado.")

# Submenu de suporte
def submenu_suporte_administrador():
    """Menu de suporte para o administrador visualizar mensagens e responder usuários."""
    while True:
        print("\n--- Suporte ---")
        print("1. Visualizar contatos de usuários")
        print("2. Responder usuário")
        print("3. Voltar ao menu anterior")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            visualizar_contatos_usuarios()
        elif escolha == "2":
            responder_usuario()
        elif escolha == "3":
            break
        else:
            print("❌ Opção inválida!")
def visualizar_contatos_usuarios():
    """Mostra todas as mensagens recebidas dos usuários e o status das respostas."""
    cursor.execute("SELECT id, email, mensagem, resposta FROM suporte")
    contatos = cursor.fetchall()

    if not contatos:
        print("\nNenhuma mensagem de usuários no momento.")
        return

    print("\n--- Mensagens dos usuários ---")
    for contato in contatos:
        id_suporte, email, mensagem, resposta = contato
        print(f"\nID: {id_suporte}")
        print(f"Usuário: {email}")
        print(f"Mensagem: {mensagem}")
        if resposta:
            print(f"Resposta: {resposta}")
        else:
            print("Resposta: (ainda não respondida)")

def responder_usuario():
    """Permite ao administrador responder uma mensagem específica de um usuário."""
    visualizar_contatos_usuarios()
    id_resposta = input("\nDigite o ID da mensagem que deseja responder (ou '0' para cancelar): ")
    if id_resposta == '0':
        print("Operação cancelada.")
        return
    
    cursor.execute("SELECT id FROM suporte WHERE id = ?", (id_resposta,))
    if not cursor.fetchone():
        print("ID inválido.")
        return

    resposta = input("Digite a resposta para o usuário: ")
    cursor.execute("UPDATE suporte SET resposta = ? WHERE id = ?", (resposta, id_resposta))
    conn.commit()
    print("Resposta enviada com sucesso.")

# ----------------- Menu do Administrador ----------------- #
def menu_administrador():
    """Menu com funcionalidades exclusivas para o administrador do sistema."""
    senha_admin = "admin123"  # senha fixa para admin
    tentativa = input("Digite a senha do administrador: ")
    if tentativa != senha_admin:
        print("❌ Senha incorreta! Acesso negado.")
        return

    while True:
        print("\n=== Menu do Administrador ===")
        print("1. Inserir alimento")
        print("2. Ver alimentos")
        print("3. Ver usuários")
        print("4. Excluir alimento")
        print("5. Suporte")  
        print("6. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            cadastrar_alimento()
        elif escolha == "2":
            ver_alimentos()
        elif escolha == "3":
            ver_usuarios()
        elif escolha == "4":
            excluir_alimento()
        elif escolha == "5":
            submenu_suporte_administrador() 
        elif escolha == "6":
            print("Saindo do menu administrador...")
            break
        else:
            print("❌ Opção inválida!")

# ----------------- Menu do Usuário Logado ----------------- #

def menu_usuario_logado(email_usuario):
    """menu principal com as funcionalidades disponíveis para o usuário logado."""
    while True:
        print(f"\n=== Bem-vindo {email_usuario} ===")
        print("1. Registrar refeição")
        print("2. Ver refeições")
        print("3. Ver alimentos recomendados")
        print("4. Encerrar o dia")
        print("5. Ranking de alimentos consumidos")
        print("6. Lembretes e alertas")
        print("7. Ajuda e suporte")
        print("8. Editar meus dados")
        print("9. Logout")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            registrar_refeicao(email_usuario)
        elif escolha == "2":
            ver_refeicoes(email_usuario)
        elif escolha == "3":
            ver_alimentos_recomendados_usuario(email_usuario)
        elif escolha == "4":
            encerrar_dia(email_usuario)
        elif escolha == "5":
            ranking_alimentos_mais_consumidos(email_usuario)
        elif escolha == "6":
            submenu_lembretes( email_usuario)
        elif escolha == "7":
            submenu_ajuda_suporte_usuario(email_usuario)
        elif escolha == "8":
            editar_meus_dados(email_usuario)
        elif escolha == "9":
            print("Logout realizado.")
            break
        else:
            print("❌ Opção inválida!")

# ----------------- Menu Principal ----------------- #

def menu_principal():
    """Menu inicial do sistema com opções de cadastro, login ou acesso do administrador."""
    while True:
        print("\n--- Menu Nutrismart ---")
        print("1. Cadastrar usuário")
        print("2. Login")
        print("3. Administrador")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            registrar_usuario()
        elif escolha == "2":
            email = login()
            if email:
                menu_usuario_logado(email)
        elif escolha == "3":
            senha_admin = input("Digite a senha do administrador: ")
            if senha_admin == "admin123":  # senha fixa para administrador
                menu_administrador()
            else:
                print("❌ Senha de administrador incorreta.")
        elif escolha == "4":
            print("Saindo do programa...")
            break
        else:
            print("❌ Opção inválida!")

# ----------------- Execução ----------------- #

if __name__ == "__main__":
    menu_principal()
    conn.close()
