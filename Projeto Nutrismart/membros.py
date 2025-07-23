# Importações necessárias para o código
import re  
from database import cursor, conn  

class Usuario:
    """Classe que representa um usuário do sistema de saúde e nutrição."""
    
    def __init__(self, email):
        """Inicializa um usuário com seu e-mail.
        
        Args:
            email (str): Endereço de e-mail do usuário.
        """
        self.email = email

    @staticmethod
    def validar_email(email):
        """Valida se um e-mail tem formato válido usando regex.
        
        Args:
            email (str): Endereço de e-mail a ser validado.
            
        Returns:
            bool: True se o e-mail for válido, False caso contrário.
        """
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Padrão básico para e-mails
        return re.match(padrao, email) is not None

    @staticmethod
    def calcular_imc(peso, altura):
        """Calcula o IMC (Índice de Massa Corporal) com base no peso e altura.
        
        Args:
            peso (float): Peso do usuário em quilogramas.
            altura (float): Altura do usuário em metros.
            
        Returns:
            float: Valor do IMC.
        """
        return round(peso / (altura ** 2), 2)  # Arredonda para 2 casas decimais

    @staticmethod
    def escolher_dieta():
        """Permite ao usuário escolher uma dieta entre as opções disponíveis.
        
        Returns:
            str: Nome da dieta selecionada.
        """
        opcoes = ["Low carb", "Cetogênica", "Hiperproteica", "Bulking"]
        while True:
            print("\nEscolha sua dieta:")
            for i, dieta in enumerate(opcoes, 1):
                print(f"{i}. {dieta}")
            escolha = input("Digite o número da dieta: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
                return opcoes[int(escolha) - 1]
            else:
                print("❌ Opção inválida! Tente novamente.")

    @staticmethod
    def registrar():
        """Registra um novo usuário no sistema, coletando e validando todos os dados necessários."""
        print("\n=== Cadastro de Usuário ===")
        # Validação do e-mail
        while True:
            email = input("E-mail: ").strip()
            if not Usuario.validar_email(email):
                print("❌ E-mail inválido!")
                continue
            # Verifica se e-mail já existe
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            if cursor.fetchone():
                print("❌ E-mail já está cadastrado!")
                continue
            break

        # Validação da senha (não pode ser vazia)
        while True:
            senha = input("Senha: ").strip()
            if senha == "":
                print("❌ A senha não pode ser vazia!")
            else:
                break

        # Validação de peso e altura (devem ser números positivos)
        try:
            peso = float(input("Peso (kg): "))
            altura = float(input("Altura (m): "))
            if peso <= 0 or altura <= 0:
                print("❌ Peso e altura devem ser maiores que zero.")
                return
        except ValueError:
            print("❌ Digite apenas números válidos para peso e altura.")
            return

        # Validação do sexo (apenas M ou F)
        sexo = input("Sexo (M/F): ").strip().upper()
        if sexo not in ['M', 'F']:
            print("❌ Sexo inválido! Use apenas 'M' ou 'F'.")
            return

        # Seleção de dieta e cálculo do IMC
        dieta = Usuario.escolher_dieta()
        imc = Usuario.calcular_imc(peso, altura)

        # Configuração de pergunta de segurança para recuperação
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

        # Insere todos os dados no banco de dados
        cursor.execute('''
            INSERT INTO usuarios (email, senha, peso, altura, sexo, dieta, imc, pergunta_seguranca, resposta_seguranca)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, senha, peso, altura, sexo, dieta, imc, pergunta, resposta))
        conn.commit()
        print(f"✅ Usuário cadastrado com sucesso! Seu IMC é {imc}")

    @staticmethod
    def recuperar_senha():
        """Permite ao usuário recuperar sua senha respondendo à pergunta de segurança."""
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

    @staticmethod
    def login():
        """Realiza o login do usuário no sistema.
        
        Returns:
            Usuario: Instância do usuário se o login for bem-sucedido, None caso contrário.
        """
        print("\n=== Login ===")
        while True:
            email = input("E-mail: ").strip()
            cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
            resultado = cursor.fetchone()
            if not resultado:
                print("❌ E-mail não encontrado. Tente novamente.")
                return None

            senha_digitada = input("Senha: ").strip()
            if senha_digitada != resultado[0]:
                print("❌ Senha incorreta.")
                escolha = input("Deseja recuperar sua senha? (s/n): ").strip().lower()
                if escolha == 's':
                    Usuario.recuperar_senha()
                else:
                    print("Tente novamente.")
                continue

            print("✅ Login realizado com sucesso!")
            return Usuario(email)  # Retorna uma instância do usuário

    def editar_meus_dados(self):
        """Permite ao usuário editar seus dados pessoais (peso, altura, dieta) e recalcula o IMC."""
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

        nova_dieta = Usuario.escolher_dieta()
        novo_imc = Usuario.calcular_imc(novo_peso, nova_altura)

        # Atualiza os dados no banco de dados
        cursor.execute('''
            UPDATE usuarios
            SET peso = ?, altura = ?, dieta = ?, imc = ?
            WHERE email = ?
        ''', (novo_peso, nova_altura, nova_dieta, novo_imc, self.email))
        conn.commit()

        print("✅ Dados atualizados com sucesso!")
        print(f"📊 Novo IMC: {novo_imc}")


class Adm(Usuario):
    """Classe que representa um administrador do sistema, com funcionalidades adicionais."""
    
    @staticmethod
    def ver_usuarios():
        """Exibe todos os usuários cadastrados no sistema com seus dados principais."""
        print("\n=== Usuários Cadastrados ===")
        cursor.execute("SELECT email, peso, altura, sexo, dieta, imc FROM usuarios")
        usuarios = cursor.fetchall()
        if usuarios:
            for u in usuarios:
                print(f"- Email: {u[0]} | Peso: {u[1]} kg | Altura: {u[2]} m | Sexo: {u[3]} | Dieta: {u[4]} | IMC: {u[5]}")
        else:
            print("❌ Nenhum usuário cadastrado.")