# Importações necessárias para o código
from database import cursor, conn

class Suporte:
    @staticmethod
    def contatar_administrador(email_usuario, mensagem=None):
        """
        Permite que o usuário envie uma mensagem ao administrador do sistema.
        
        Parâmetros:
            email_usuario (str): E-mail do usuário que está enviando a mensagem
            mensagem (str, opcional): Mensagem pré-definida (usada para chamadas programáticas)
        """
        if mensagem is None:
            print("\n--- Contato com o Administrador ---")
            mensagem = input("Digite sua dúvida, sugestão ou mensagem: ")

        # Valida se a mensagem não está vazia
        if mensagem.strip() == "":
            print("❌ Mensagem vazia não pode ser enviada.")
            return

        # Insere a mensagem no banco de dados
        cursor.execute("INSERT INTO suporte (email, mensagem) VALUES (?, ?)", 
                        (email_usuario, mensagem))
        conn.commit()

        print("✅ Mensagem enviada com sucesso! O administrador responderá em breve.")

    @staticmethod
    def visualizar_respostas(email_usuario):
        """
        Exibe todas as mensagens enviadas pelo usuário e suas respectivas respostas.
        
        Parâmetros:
            email_usuario (str): E-mail do usuário para filtrar as mensagens
        """
        print("\n--- Respostas do Administrador ---")
        
        # Busca todas as interações do usuário com o suporte
        cursor.execute("SELECT mensagem, resposta FROM suporte WHERE email = ?", 
                        (email_usuario,))
        registros = cursor.fetchall()

        if not registros:
            print("📭 Você ainda não enviou nenhuma mensagem ao administrador.")
        else:
            # Exibe cada mensagem com seu status de resposta
            for i, (mensagem, resposta) in enumerate(registros, start=1):
                print(f"\n📨 Mensagem {i}: {mensagem}")
                if resposta:
                    print(f"🟢 Resposta: {resposta}")
                else:
                    print("🕐 Aguardando resposta do administrador. Por favor, aguarde pacientemente.")
        
        input("\nPressione Enter para voltar ao menu...")

    @staticmethod
    def submenu_ajuda_suporte_usuario(email_usuario):
        """
        Menu interativo para usuários com opções de suporte.
        
        Parâmetros:
            email_usuario (str): E-mail do usuário logado
        """
        while True:
            print("\n=== Ajuda e Suporte ===")
            print("1. Contatar o administrador")
            print("2. Visualizar respostas")
            print("3. Voltar ao menu anterior")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                Suporte.contatar_administrador(email_usuario)
            elif escolha == "2":
                Suporte.visualizar_respostas(email_usuario)
            elif escolha == "3":
                break
            else:
                print("❌ Opção inválida!")

    # --- Métodos do Administrador --- #
    @staticmethod
    def submenu_suporte_administrador():
        """Menu interativo para administradores gerenciarem solicitações de suporte."""
        while True:
            print("\n--- Suporte ---")
            print("1. Visualizar contatos de usuários")
            print("2. Responder usuário")
            print("3. Voltar ao menu anterior")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                Suporte.visualizar_contatos_usuarios()
            elif escolha == "2":
                Suporte.responder_usuario()
            elif escolha == "3":
                break
            else:
                print("❌ Opção inválida!")

    @staticmethod
    def visualizar_contatos_usuarios():
        """Exibe todas as mensagens de suporte recebidas dos usuários."""
        # Busca todas as interações de suporte registradas
        cursor.execute("SELECT id, email, mensagem, resposta FROM suporte")
        contatos = cursor.fetchall()

        if not contatos:
            print("\nNenhuma mensagem de usuários no momento.")
            return

        print("\n--- Mensagens dos usuários ---")
        # Exibe cada mensagem com informações completas
        for contato in contatos:
            id_suporte, email, mensagem, resposta = contato
            print(f"\nID: {id_suporte}")
            print(f"Usuário: {email}")
            print(f"Mensagem: {mensagem}")
            if resposta:
                print(f"Resposta: {resposta}")
            else:
                print("Resposta: (ainda não respondida)")

    @staticmethod
    def responder_usuario():
        """
        Permite ao administrador responder a uma mensagem específica.
        Primeiro exibe todas as mensagens e depois solicita o ID para resposta.
        """
        # Mostra todas as mensagens disponíveis
        Suporte.visualizar_contatos_usuarios()
        
        # Solicita o ID da mensagem a ser respondida
        id_resposta = input("\nDigite o ID da mensagem que deseja responder (ou '0' para cancelar): ")
        if id_resposta == '0':
            print("Operação cancelada.")
            return
        
        # Valida se o ID existe
        cursor.execute("SELECT id FROM suporte WHERE id = ?", (id_resposta,))
        if not cursor.fetchone():
            print("ID inválido.")
            return

        # Coleta e registra a resposta
        resposta = input("Digite a resposta para o usuário: ")
        cursor.execute("UPDATE suporte SET resposta = ? WHERE id = ?", 
                        (resposta, id_resposta))
        conn.commit()
        print("Resposta enviada com sucesso.")