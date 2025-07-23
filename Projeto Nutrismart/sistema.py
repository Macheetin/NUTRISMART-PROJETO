# Importações necessárias para o código
from membros import Usuario
from alimentacao import Comida
from suportinho import Suporte

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
            Comida.cadastrar_alimento()
        elif escolha == "2":
            Comida.ver_alimentos()
        elif escolha == "3":
            Comida.ver_usuarios()
        elif escolha == "4":
            Comida.excluir_alimento()
        elif escolha == "5":
            Comida.submenu_suporte_administrador()
        elif escolha == "6":
            print("Saindo do menu administrador...")
            break
        else:
            print("❌ Opção inválida!")


# ----------------- Menu do Usuário Logado ----------------- #
def menu_usuario_logado(usuario):
    """Menu principal com as funcionalidades disponíveis para o usuário logado."""
    email_usuario = usuario.email
    comida = Comida(email_usuario)

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
            comida.registrar_refeicao()
        elif escolha == "2":
            comida.ver_refeicoes()
        elif escolha == "3":
            comida.ver_alimentos_recomendados()
        elif escolha == "4":
            comida.encerrar_dia()
        elif escolha == "5":
            comida.ranking_alimentos_mais_consumidos()
        elif escolha == "6":
            comida.submenu_lembretes()
        elif escolha == "7":
            Suporte.submenu_ajuda_suporte_usuario(email_usuario)
        elif escolha == "8":
            usuario.editar_meus_dados()
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
            Usuario.registrar()
        elif escolha == "2":
            usuario = Usuario.login()
            if usuario:
                menu_usuario_logado(usuario)
        elif escolha == "3":
            menu_administrador()
        elif escolha == "4":
            print("Saindo do programa...")
            break
        else:
            print("❌ Opção inválida!")
