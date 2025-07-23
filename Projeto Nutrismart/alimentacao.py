# Importações necessárias para o código
import random
from datetime import datetime, date
from database import cursor, conn  

class Comida:
    """Classe principal para gerenciar operações relacionadas a alimentos"""
    
    def __init__(self, email_usuario):
        """
        Inicializa a instância da classe Comida
        
        Args:
            email_usuario (str): Email do usuário que será associado às operações
        """
        self.email_usuario = email_usuario
    
    def registrar_refeicao(self, alimento, quantidade):
        """
        Registra uma refeição no banco de dados
        
        Args:
            alimento (str): Nome do alimento a ser registrado
            quantidade (float): Quantidade consumida em gramas
            
        Returns:
            tuple: (bool, str) Indicando sucesso/falha e mensagem correspondente
        """
        try:
            # Verifica se o alimento existe no banco de dados
            cursor.execute("SELECT calorias FROM alimentos WHERE nome = ?", (alimento,))
            resultado = cursor.fetchone()
            if not resultado:
                return False, "Alimento não cadastrado"
            
            # Calcula as calorias consumidas com base na quantidade (em gramas)
            calorias = (quantidade / 100) * resultado[0]
            
            # Insere a refeição no banco de dados com data/hora atual
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('''
                INSERT INTO refeicoes (email_usuario, alimento, quantidade_gramas, calorias, data)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.email_usuario, alimento, quantidade, calorias, data))
            conn.commit()
            return True, "Refeição registrada com sucesso"
            
        except Exception as e:
            # Trata erros durante o registro
            print(f"Erro ao registrar refeição: {e}")
            return False, f"Erro ao registrar: {str(e)}"

    def ver_refeicoes(self):
        """
        Retorna todas as refeições registradas pelo usuário
        
        Returns:
            list: Lista de tuplas com informações das refeições, ordenadas por data (mais recente primeiro)
        """
        cursor.execute('''
            SELECT id, alimento, quantidade_gramas, calorias, data 
            FROM refeicoes 
            WHERE email_usuario = ?
            ORDER BY data DESC
        ''', (self.email_usuario,))
        return cursor.fetchall()

    def ver_alimentos_recomendados(self):
        """
        Exibe 4 alimentos aleatórios recomendados com base na dieta do usuário
        
        Obtém a dieta do usuário do banco de dados e recomenda alimentos adequados
        """
        # Obtém a dieta do usuário do banco de dados
        cursor.execute("SELECT dieta FROM usuarios WHERE email = ?", (self.email_usuario,))
        resultado = cursor.fetchone()
        if not resultado:
            print("❌ Usuário não encontrado.")
            return

        dieta_usuario = resultado[0]

        # Dicionário com alimentos recomendados para cada tipo de dieta
        recomendacoes = {
            "Low carb": [
                "Ovos", "Abacate", "Peixes", "Nozes", "Couve-flor", "Espinafre", "Brócolis", "Azeite de oliva",
                "Amêndoas", "Queijo", "Cogumelos", "Carne bovina", "Salmão", "Aspargos", "Alface", "Cenoura",
                "Tomate", "Pepino", "Pimentão", "Berinjela", "Abobrinha", "Castanha-do-pará", "Aipo", "Azeitona",
                "Sementes de chia", "Sementes de linhaça", "Coco", "Framboesa", "Morango", "Repolho", "Alcachofra",
                "Cebola", "Algo", "Rúcula", "Manjericão", "Salsinha", "Endívia", "Alcaparras", "Pimenta", "Ervilha-torta",
                "Limão", "Laranja", "Carne de porco", "Frango", "Iogurte natural", "Ricota", "Chá verde", "Água com gás",
                "Vinagre de maçã", "Café"
            ],
            "Cetogênica": [
                "Bacon", "Queijo cheddar", "Carne de cordeiro", "Manteiga", "Nata", "Óleo de coco", "Salmão selvagem",
                "Ovos caipiras", "Espinafre", "Couve", "Brócolis", "Couve-flor", "Abacate", "Nozes", "Castanhas",
                "Sementes de abóbora", "Azeitonas", "Chá de hortelã", "Café sem açúcar", "Queijo parmesão",
                "Frango caipira", "Carne moída", "Camarão", "Atum", "Aspargos", "Abobrinha", "Cogumelos", "Algo",
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

        # Obtém a lista de alimentos recomendados para a dieta do usuário
        alimentos_recomendados = recomendacoes.get(dieta_usuario, [])

        if not alimentos_recomendados:
            print("❌ Nenhum alimento recomendado encontrado para esta dieta.")
            return

        # Seleciona 4 alimentos aleatórios da lista
        aleatorios = random.sample(alimentos_recomendados, k=4)

        # Exibe os alimentos recomendados
        print(f"\n🍽️ 4 Alimentos aleatórios recomendados para a dieta {dieta_usuario}:")
        for alimento in aleatorios:
            print(f"- {alimento}")

    def ranking_alimentos_mais_consumidos(self):
        """
        Exibe um ranking dos 10 alimentos mais consumidos pelo usuário (em gramas)
        
        Mostra os alimentos ordenados pela quantidade total consumida
        """
        print("\n🏆 Ranking dos alimentos mais consumidos:")
        cursor.execute('''
            SELECT alimento, SUM(quantidade_gramas) as total_gramas
            FROM refeicoes
            WHERE email_usuario = ?
            GROUP BY alimento
            ORDER BY total_gramas DESC
            LIMIT 10
        ''', (self.email_usuario,))
        ranking = cursor.fetchall()

        if not ranking:
            print("❌ Nenhuma refeição registrada para gerar o ranking.")
            return

        # Exibe o ranking formatado
        for i, (alimento, total) in enumerate(ranking, 1):
            print(f"{i}. {alimento.capitalize()} - {total:.2f} g")


class Adm_alimentar(Comida):
    """Classe para administração de alimentos (herda de Comida)"""
    
    @staticmethod
    def cadastrar_alimento():
        """
        Cadastra um novo alimento no banco de dados
        
        Solicita nome e calorias do alimento e insere no sistema
        """
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

        # Verifica se o alimento já existe
        cursor.execute("SELECT * FROM alimentos WHERE nome = ?", (nome,))
        if cursor.fetchone():
            print("❌ Alimento já cadastrado!")
            return

        # Insere o novo alimento
        cursor.execute("INSERT INTO alimentos (nome, calorias) VALUES (?, ?)", (nome, calorias))
        conn.commit()
        print(f"✅ Alimento '{nome}' cadastrado com sucesso.")

    @staticmethod
    def ver_alimentos():
        """
        Lista todos os alimentos cadastrados no sistema
        
        Exibe nome e calorias por 100g de cada alimento
        """
        print("\n=== Lista de alimentos cadastrados ===")
        cursor.execute("SELECT nome, calorias FROM alimentos")
        alimentos = cursor.fetchall()
        if alimentos:
            for a in alimentos:
                print(f"- {a[0]} | {a[1]} cal por 100g")
        else:
            print("❌ Nenhum alimento cadastrado.")

    @staticmethod
    def excluir_alimento():
        """
        Remove um alimento do banco de dados
        
        Solicita o nome do alimento a ser removido e confirma a operação
        """
        print("\n=== Excluir alimento ===")
        nome = input("Nome do alimento para excluir: ").strip().lower()
        cursor.execute("SELECT * FROM alimentos WHERE nome = ?", (nome,))
        if not cursor.fetchone():
            print("❌ Alimento não encontrado.")
            return
        cursor.execute("DELETE FROM alimentos WHERE nome = ?", (nome,))
        conn.commit()
        print(f"✅ Alimento '{nome}' excluído com sucesso.")


class Registros(Comida):
    """Classe para gerenciar registros diários e lembretes (herda de Comida)"""
    
    def pegar_registros_do_dia(self):
        """
        Obtém todos os registros alimentares do dia atual
        
        Returns:
            list: Lista de registros do dia atual
        """
        hoje = date.today()
        cursor.execute("SELECT * FROM registro_refeicoes WHERE email = ? AND data = ?", (self.email_usuario, str(hoje)))
        registros = cursor.fetchall()
        return registros

    def submenu_lembretes(self):
        """
        Exibe lembretes personalizados com base nos registros do dia
        
        Mostra alertas sobre consumo alimentar e hidratação
        """
        registros_diarios = self.pegar_registros_do_dia()

        print("\n--- Lembretes e Alertas ---")

        if not registros_diarios:
            print("Atenção! Você ainda não registrou nenhuma refeição hoje. Não esqueça de se alimentar!")
        else:
            print(f"Você já registrou {len(registros_diarios)} refeição(ões) hoje. Continue assim!")

        print("Lembrete: Beba pelo menos 2 litros de água ao longo do dia.")
        input("\nPressione Enter para voltar ao menu principal...")

    def encerrar_dia(self):
        """
        Calcula e exibe um resumo nutricional do dia
        
        Compara as calorias consumidas com a meta calórica baseada na dieta
        """
        print("\n📅 Encerramento do Dia")
        hoje = date.today().strftime("%Y-%m-%d")

        # Obtém dados do usuário (dieta, peso, altura)
        cursor.execute("SELECT dieta, peso, altura FROM usuarios WHERE email = ?", (self.email_usuario,))
        resultado = cursor.fetchone()
        if not resultado:
            print("❌ Usuário não encontrado.")
            return
        dieta_usuario, peso, altura = resultado

        # Obtém todas as refeições registradas hoje
        cursor.execute('''
            SELECT r.alimento, r.quantidade_gramas, a.calorias
            FROM refeicoes r
            JOIN alimentos a ON r.alimento = a.nome
            WHERE r.email_usuario = ? AND date(r.data) = ?
        ''', (self.email_usuario, hoje))
        refeicoes_hoje = cursor.fetchall()

        if not refeicoes_hoje:
            print("❌ Nenhuma refeição registrada para hoje.")
            return

        # Calcula o total de calorias consumidas
        calorias_totais = 0
        for alimento, quantidade, cal_100g in refeicoes_hoje:
            calorias_totais += (cal_100g * quantidade) / 100

        calorias_totais = round(calorias_totais, 2)

        # Define metas calóricas baseadas no tipo de dieta
        metas = {
            "Low carb": 25 * peso,
            "Cetogênica": 27 * peso,
            "Hiperproteica": 30 * peso,
            "Bulking": 35 * peso
        }

        meta_calorias = metas.get(dieta_usuario, 30 * peso)

        # Exibe o resumo e feedback
        print(f"\nDieta: {dieta_usuario}")
        print(f"Calorias consumidas hoje: {calorias_totais} kcal")
        print(f"Meta calórica diária aproximada: {meta_calorias} kcal")

        if calorias_totais < meta_calorias * 0.9:
            print("⚠️ Você consumiu menos calorias que o recomendado para sua dieta hoje.")
        elif calorias_totais > meta_calorias * 1.1:
            print("⚠️ Você consumiu mais calorias que o recomendado para sua dieta hoje.")
        else:
            print("✅ Consumo calórico dentro da meta para hoje. Bom trabalho!")