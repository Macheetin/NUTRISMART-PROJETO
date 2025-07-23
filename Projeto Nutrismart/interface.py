import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, date
from database import cursor, conn
from alimentacao import Comida
from suportinho import Suporte

class InterfaceNutrismart:
    def __init__(self, root):
        """Inicializa a aplicação principal com configurações básicas"""
        self.root = root
        self.root.title("Nutrismart - Sistema Nutricional")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        self.usuario_atual = None
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configuração de cores e fontes
        self.cores = {
            'fundo': '#f0f0f0',
            'card': '#ffffff',
            'primaria': "#95a72e",
            'secundaria': "#ecc70e",
            'texto': '#212121',
            'destaque': '#ff8f00'
        }
        
        self.fontes = {
            'titulo': ('Arial', 18, 'bold'),
            'subtitulo': ('Arial', 14),
            'normal': ('Arial', 12),
            'pequena': ('Arial', 10)
        }
        
        self.configurar_estilos()
        self.criar_menu_principal()

    def configurar_estilos(self):
        """Configura os estilos visuais para todos os componentes"""
        self.style.configure('TFrame', background=self.cores['fundo'])
        self.style.configure('TLabel', background=self.cores['fundo'], foreground=self.cores['texto'])
        self.style.configure('TButton', font=self.fontes['normal'], padding=6)
        self.style.configure('Titulo.TLabel', font=self.fontes['titulo'], foreground=self.cores['primaria'])
        self.style.configure('Card.TFrame', background=self.cores['card'], relief=tk.RAISED, borderwidth=2)
        self.style.map('BotaoPrimario.TButton',
                    foreground=[('active', 'white'), ('!disabled', 'white')],
                    background=[('active', self.cores['secundaria']), ('!disabled', self.cores['primaria'])])
        
    def limpar_tela(self):
        """Remove todos os widgets da tela atual"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_menu_principal(self):
        """Cria o menu principal com opções baseadas no estado de login"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Cabeçalho
        cabecalho = ttk.Frame(frame_principal)
        cabecalho.pack(fill=tk.X, pady=10)
        ttk.Label(cabecalho, text="Nutrismart", style='Titulo.TLabel').pack(side=tk.LEFT)
        
        if self.usuario_atual:
            frame_usuario = ttk.Frame(cabecalho)
            frame_usuario.pack(side=tk.RIGHT)
            ttk.Label(frame_usuario, text=f"Bem-vindo, {self.usuario_atual}", font=self.fontes['pequena']).pack()
        
        # Grade de opções
        frame_grade = ttk.Frame(frame_principal)
        frame_grade.pack(expand=True, fill=tk.BOTH, pady=20)
        
        if not self.usuario_atual:
            opcoes = [
                ("Cadastrar Usuário", "Crie sua conta para começar", self.mostrar_tela_cadastro),
                ("Login", "Acesse sua conta existente", self.mostrar_tela_login),
                ("Acesso Admin", "Área restrita para administradores", self.mostrar_tela_admin)
            ]
        else:
            opcoes = [
                ("Registrar Refeição", "Adicione o que você consumiu", self.mostrar_tela_registro_refeicao),
                ("Histórico", "Veja seu histórico alimentar", self.mostrar_historico_refeicoes),
                ("Alimentos Recomendados", "Sugestões para sua dieta", self.mostrar_alimentos_recomendados),
                ("Encerrar Dia", "Resumo nutricional diário", self.mostrar_encerramento_dia),
                ("Ranking Alimentos", "Seus alimentos mais consumidos", self.mostrar_ranking_alimentos),
                ("Lembretes", "Alertas e recomendações", self.mostrar_lembretes),
                ("Suporte", "Fale com nosso time", self.mostrar_suporte),
                ("Editar Perfil", "Atualize seus dados", self.mostrar_edicao_perfil),
                ("Sair", "Encerre sua sessão", self.fazer_logout)
            ]
        
        for i, (titulo, descricao, comando) in enumerate(opcoes):
            linha, coluna = divmod(i, 3)
            
            card = ttk.Frame(frame_grade, style='Card.TFrame', width=300, height=150)
            card.grid(row=linha, column=coluna, padx=10, pady=10, sticky='nsew')
            card.grid_propagate(False)
            
            ttk.Label(card, text=titulo, style='Titulo.TLabel').pack(pady=10)
            ttk.Label(card, text=descricao, wraplength=280).pack(pady=5, padx=10)
            
            if comando:
                ttk.Button(card, text="Acessar", style='BotaoPrimario.TButton', 
                        command=comando).pack(pady=10, ipadx=20)
            
            frame_grade.grid_rowconfigure(linha, weight=1)
            frame_grade.grid_columnconfigure(coluna, weight=1)
        
        # Rodapé
        rodape = ttk.Frame(frame_principal)
        rodape.pack(fill=tk.X, pady=10)
        ttk.Button(rodape, text="Sair do Programa", command=self.root.quit).pack(side=tk.RIGHT)

    def mostrar_tela_registro_refeicao(self):
        """Exibe a tela para registro de novas refeições"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=30, pady=20)
        
        ttk.Label(frame_principal, text="Registrar Refeição", style='Titulo.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=10, fill=tk.X)
        
        # Campo Alimento
        ttk.Label(frame_form, text="Alimento:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entrada_alimento = ttk.Entry(frame_form)
        self.entrada_alimento.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Campo Quantidade
        ttk.Label(frame_form, text="Quantidade (gramas):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entrada_quantidade = ttk.Entry(frame_form)
        self.entrada_quantidade.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Registrar", style='BotaoPrimario.TButton',
                command=self.registrar_refeicao).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=10)

    def registrar_refeicao(self):
        """Processa o registro de uma nova refeição no banco de dados"""
        alimento = self.entrada_alimento.get().strip().lower()
        quantidade = self.entrada_quantidade.get().strip()
        
        if not alimento or not quantidade:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        try:
            quantidade = float(quantidade)
            if quantidade <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser maior que zero!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido para a quantidade!")
            return
        
        # Registra a refeição
        try:
            comida = Comida(self.usuario_atual)
            sucesso, mensagem = comida.registrar_refeicao(alimento, quantidade)
            
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.criar_menu_principal()
            else:
                messagebox.showerror("Erro", mensagem)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao registrar a refeição: {str(e)}")

    def mostrar_historico_refeicoes(self):
        """Exibe o histórico de refeições do usuário em formato de tabela"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Histórico de Refeições", style='Titulo.TLabel').pack(pady=10)
        
        frame_tabela = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_tabela.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Criar Treeview
        colunas = ("ID", "Alimento", "Quantidade (g)", "Calorias", "Data")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
        
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=120, anchor=tk.CENTER)
        
        tabela.column("Alimento", width=200, anchor=tk.W)
        tabela.column("Data", width=200)
        
        # Barra de rolagem
        scroll = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tabela.pack(expand=True, fill=tk.BOTH)
        
        # Carregar dados
        comida = Comida(self.usuario_atual)
        refeicoes = comida.ver_refeicoes()
        
        if refeicoes:
            for refeicao in refeicoes:
                tabela.insert("", tk.END, values=refeicao)
        else:
            ttk.Label(frame_principal, text="Nenhuma refeição registrada ainda.").pack()
        
        # Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Atualizar", command=self.mostrar_historico_refeicoes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=5)

    def mostrar_alimentos_recomendados(self):
        """Exibe alimentos recomendados baseados na dieta do usuário"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Alimentos Recomendados", style='Titulo.TLabel').pack(pady=10)
        
        frame_card = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_card.pack(pady=20, padx=50, fill=tk.X)
        
        # Obter recomendações
        comida = Comida(self.usuario_atual)
        
        # Obter dieta do usuário
        cursor.execute("SELECT dieta FROM usuarios WHERE email = ?", (self.usuario_atual,))
        resultado = cursor.fetchone()
        if not resultado:
            ttk.Label(frame_card, text="Usuário não encontrado.").pack()
            return
        
        dieta_usuario = resultado[0]
        
        # Mostrar dieta atual
        ttk.Label(frame_card, text=f"Dieta atual: {dieta_usuario}", font=self.fontes['subtitulo']).pack(pady=10)
        
        # Mostrar alimentos recomendados
        ttk.Label(frame_card, text="\nAlimentos recomendados:", font=self.fontes['subtitulo']).pack(pady=5, anchor=tk.W)
        
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
        
        if alimentos_recomendados:
            # Selecionar 4 aleatórios
            import random
            aleatorios = random.sample(alimentos_recomendados, k=min(4, len(alimentos_recomendados)))
            
            for alimento in aleatorios:
                ttk.Label(frame_card, text=f"- {alimento}").pack(anchor=tk.W, pady=2)
        else:
            ttk.Label(frame_card, text="Nenhuma recomendação disponível para esta dieta.").pack()
        
        ttk.Button(frame_principal, text="Voltar", command=self.criar_menu_principal).pack(pady=20)

    def mostrar_encerramento_dia(self):
        """Exibe um resumo nutricional do dia atual"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Resumo Diário", style='Titulo.TLabel').pack(pady=10)
        
        frame_card = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_card.pack(pady=20, padx=50, fill=tk.X)
        
        # Obter dados do usuário
        cursor.execute("SELECT dieta, peso, altura FROM usuarios WHERE email = ?", (self.usuario_atual,))
        resultado = cursor.fetchone()
        if not resultado:
            ttk.Label(frame_card, text="Usuário não encontrado.").pack()
            ttk.Button(frame_principal, text="Voltar", command=self.criar_menu_principal).pack(pady=20)
            return
        
        dieta_usuario, peso, altura = resultado
        
        # Obter refeições do dia
        hoje = date.today().strftime("%Y-%m-%d")
        cursor.execute('''
            SELECT r.alimento, r.quantidade_gramas, a.calorias
            FROM refeicoes r
            JOIN alimentos a ON r.alimento = a.nome
            WHERE r.email_usuario = ? AND date(r.data) = ?
        ''', (self.usuario_atual, hoje))
        refeicoes_hoje = cursor.fetchall()
        
        if not refeicoes_hoje:
            ttk.Label(frame_card, text="Nenhuma refeição registrada para hoje.").pack()
            ttk.Button(frame_principal, text="Voltar", command=self.criar_menu_principal).pack(pady=20)
            return
        
        # Calcular calorias totais
        calorias_totais = 0
        for alimento, quantidade, cal_100g in refeicoes_hoje:
            calorias_totais += (cal_100g * quantidade) / 100
        calorias_totais = round(calorias_totais, 2)
        
        # Calcular meta calórica
        metas = {
            "Low carb": 25 * peso,
            "Cetogênica": 27 * peso,
            "Hiperproteica": 30 * peso,
            "Bulking": 35 * peso
        }
        meta_calorias = metas.get(dieta_usuario, 30 * peso)
        
        # Exibir resultados
        ttk.Label(frame_card, text=f"Dieta: {dieta_usuario}").pack(anchor=tk.W, pady=5)
        ttk.Label(frame_card, text=f"Calorias consumidas hoje: {calorias_totais} kcal").pack(anchor=tk.W, pady=5)
        ttk.Label(frame_card, text=f"Meta calórica diária: {meta_calorias} kcal").pack(anchor=tk.W, pady=5)
        
        # Avaliação
        if calorias_totais < meta_calorias * 0.9:
            status = "⚠️ Você consumiu menos calorias que o recomendado para sua dieta hoje."
            cor = 'red'
        elif calorias_totais > meta_calorias * 1.1:
            status = "⚠️ Você consumiu mais calorias que o recomendado para sua dieta hoje."
            cor = 'red'
        else:
            status = "✅ Consumo calórico dentro da meta para hoje. Bom trabalho!"
            cor = 'green'
        
        ttk.Label(frame_card, text=status, foreground=cor).pack(anchor=tk.W, pady=10)
        
        ttk.Button(frame_principal, text="Voltar", command=self.criar_menu_principal).pack(pady=20)

    def mostrar_ranking_alimentos(self):
        """Exibe ranking dos alimentos mais consumidos pelo usuário"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Ranking de Alimentos", style='Titulo.TLabel').pack(pady=10)
        
        frame_tabela = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_tabela.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Criar Treeview
        tabela = ttk.Treeview(frame_tabela, columns=("Posição", "Alimento", "Quantidade"), show="headings", height=10)
        
        tabela.heading("Posição", text="Posição")
        tabela.heading("Alimento", text="Alimento")
        tabela.heading("Quantidade", text="Quantidade (g)")
        
        tabela.column("Posição", width=80, anchor=tk.CENTER)
        tabela.column("Alimento", width=200, anchor=tk.W)
        tabela.column("Quantidade", width=150, anchor=tk.CENTER)
        
        # Barra de rolagem
        scroll = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tabela.pack(expand=True, fill=tk.BOTH)
        
        # Carregar dados
        cursor.execute('''
            SELECT alimento, SUM(quantidade_gramas) as total_gramas
            FROM refeicoes
            WHERE email_usuario = ?
            GROUP BY alimento
            ORDER BY total_gramas DESC
            LIMIT 10
        ''', (self.usuario_atual,))
        ranking = cursor.fetchall()
        
        if ranking:
            for i, (alimento, total) in enumerate(ranking, 1):
                tabela.insert("", tk.END, values=(i, alimento.capitalize(), f"{total:.2f}"))
        else:
            ttk.Label(frame_principal, text="Nenhuma refeição registrada para gerar ranking.").pack()
        
        # Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Atualizar", command=self.mostrar_ranking_alimentos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=5)

    def mostrar_lembretes(self):
        """Exibe lembretes e alertas para o usuário"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Lembretes", style='Titulo.TLabel').pack(pady=10)
        
        frame_card = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_card.pack(pady=20, padx=50, fill=tk.X)
        
        # Obter registros do dia
        hoje = date.today()
        cursor.execute("SELECT * FROM refeicoes WHERE email_usuario = ? AND date(data) = ?", 
                      (self.usuario_atual, str(hoje)))
        registros = cursor.fetchall()
        
        if not registros:
            ttk.Label(frame_card, text="Você ainda não registrou refeições hoje!").pack(pady=10)
        else:
            ttk.Label(frame_card, text=f"Você registrou {len(registros)} refeições hoje").pack(pady=10)
        
        ttk.Label(frame_card, text="Lembrete: Beba pelo menos 2 litros de água ao longo do dia!").pack(pady=10)
        
        ttk.Button(frame_principal, text="Voltar", command=self.criar_menu_principal).pack(pady=20)

    def mostrar_suporte(self):
        """Exibe a interface de suporte para o usuário"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Ajuda e Suporte", style='Titulo.TLabel').pack(pady=10)
        
        notebook = ttk.Notebook(frame_principal)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Aba de contato
        frame_contato = ttk.Frame(notebook)
        notebook.add(frame_contato, text="Enviar Mensagem")
        
        ttk.Label(frame_contato, text="Digite sua mensagem:", font=self.fontes['subtitulo']).pack(pady=10, anchor=tk.W)
        
        self.texto_mensagem = scrolledtext.ScrolledText(frame_contato, width=80, height=10, wrap=tk.WORD)
        self.texto_mensagem.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        frame_botoes_contato = ttk.Frame(frame_contato)
        frame_botoes_contato.pack(pady=10)
        
        ttk.Button(frame_botoes_contato, text="Enviar", style='BotaoPrimario.TButton',
                command=self.enviar_mensagem_suporte).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_contato, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=5)
        
        # Aba de respostas
        frame_respostas = ttk.Frame(notebook)
        notebook.add(frame_respostas, text="Minhas Mensagens")
        
        self.tabela_mensagens = ttk.Treeview(frame_respostas, columns=("Data", "Mensagem", "Resposta"), show="headings", height=10)
        
        self.tabela_mensagens.heading("Data", text="Data")
        self.tabela_mensagens.heading("Mensagem", text="Mensagem")
        self.tabela_mensagens.heading("Resposta", text="Resposta")
        
        self.tabela_mensagens.column("Data", width=120)
        self.tabela_mensagens.column("Mensagem", width=300)
        self.tabela_mensagens.column("Resposta", width=300)
        
        scroll = ttk.Scrollbar(frame_respostas, orient=tk.VERTICAL, command=self.tabela_mensagens.yview)
        self.tabela_mensagens.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabela_mensagens.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.carregar_mensagens_suporte()
        
        ttk.Button(frame_principal, text="Voltar", command=self.criar_menu_principal).pack(pady=10)

    def enviar_mensagem_suporte(self):
        """Envia uma mensagem de suporte para o administrador"""
        mensagem = self.texto_mensagem.get("1.0", tk.END).strip()
        
        if not mensagem:
            messagebox.showerror("Erro", "Digite uma mensagem antes de enviar!")
            return
            
        try:
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("""
                INSERT INTO suporte (email, mensagem, data_hora) 
                VALUES (?, ?, ?)
            """, (self.usuario_atual, mensagem, data_hora))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")
            self.texto_mensagem.delete("1.0", tk.END)
            self.carregar_mensagens_suporte()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao enviar a mensagem: {str(e)}")

    def carregar_mensagens_suporte(self):
        """Carrega as mensagens de suporte do usuário"""
        for item in self.tabela_mensagens.get_children():
            self.tabela_mensagens.delete(item)
            
        cursor.execute("""
            SELECT data_hora, mensagem, resposta 
            FROM suporte 
            WHERE email = ?
            ORDER BY data_hora DESC
        """, (self.usuario_atual,))
        
        for linha in cursor.fetchall():
            self.tabela_mensagens.insert("", tk.END, values=linha)

    def mostrar_edicao_perfil(self):
        """Exibe a tela para edição dos dados do perfil"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Editar Perfil", style='Titulo.TLabel').pack(pady=10)
        
        # Obter dados atuais do usuário
        cursor.execute("SELECT peso, altura, dieta FROM usuarios WHERE email = ?", (self.usuario_atual,))
        resultado = cursor.fetchone()
        if not resultado:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            self.criar_menu_principal()
            return
        
        peso, altura, dieta = resultado
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        # Campo Peso
        ttk.Label(frame_form, text="Peso (kg):").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.entrada_peso = ttk.Entry(frame_form)
        self.entrada_peso.insert(0, str(peso))
        self.entrada_peso.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Campo Altura
        ttk.Label(frame_form, text="Altura (m):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.entrada_altura = ttk.Entry(frame_form)
        self.entrada_altura.insert(0, str(altura))
        self.entrada_altura.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Campo Dieta
        ttk.Label(frame_form, text="Dieta:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.combo_dieta = ttk.Combobox(frame_form, values=["Low carb", "Cetogênica", "Hiperproteica", "Bulking"])
        self.combo_dieta.set(dieta)
        self.combo_dieta.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)
        
        # Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Salvar", style='BotaoPrimario.TButton',
                command=self.salvar_edicao_perfil).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=10)

    def salvar_edicao_perfil(self):
        """Salva as alterações do perfil no banco de dados"""
        try:
            novo_peso = float(self.entrada_peso.get())
            nova_altura = float(self.entrada_altura.get())
            nova_dieta = self.combo_dieta.get()
            
            if novo_peso <= 0 or nova_altura <= 0:
                messagebox.showerror("Erro", "Peso e altura devem ser maiores que zero!")
                return
                
            novo_imc = novo_peso / (nova_altura ** 2)
            
            cursor.execute("""
                UPDATE usuarios 
                SET peso = ?, altura = ?, dieta = ?, imc = ?
                WHERE email = ?
            """, (novo_peso, nova_altura, nova_dieta, novo_imc, self.usuario_atual))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            self.criar_menu_principal()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite valores numéricos válidos!")

    def mostrar_tela_cadastro(self):
        """Exibe a tela de cadastro de novos usuários"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=50, pady=30)
        
        ttk.Label(frame_principal, text="Cadastro de Usuário", style='Titulo.TLabel').pack(pady=20)
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        campos = [
            ("E-mail:", "entry", "email"),
            ("Senha:", "entry", "senha", True),
            ("Peso (kg):", "entry", "peso"),
            ("Altura (m):", "entry", "altura"),
            ("Sexo (M/F):", "entry", "sexo")
        ]
        
        for i, (rotulo, tipo, nome, *opcoes) in enumerate(campos):
            ttk.Label(frame_form, text=rotulo).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            
            if tipo == "entry":
                entrada = ttk.Entry(frame_form, show="*" if opcoes and opcoes[0] else None)
                entrada.grid(row=i, column=1, padx=10, pady=10, sticky=tk.EW)
                setattr(self, f"cad_{nome}", entrada)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Cadastrar", style='BotaoPrimario.TButton',
                command=self.cadastrar_usuario).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=10)

    def cadastrar_usuario(self):
        """Processa o cadastro de um novo usuário"""
        email = self.cad_email.get().strip()
        senha = self.cad_senha.get().strip()
        peso = self.cad_peso.get().strip()
        altura = self.cad_altura.get().strip()
        sexo = self.cad_sexo.get().strip().upper()
        
        if not all([email, senha, peso, altura, sexo]):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        if sexo not in ['M', 'F']:
            messagebox.showerror("Erro", "Sexo deve ser M ou F!")
            return
            
        try:
            peso = float(peso)
            altura = float(altura)
            
            if peso <= 0 or altura <= 0:
                messagebox.showerror("Erro", "Peso e altura devem ser maiores que zero!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Peso e altura devem ser números válidos!")
            return
        
        # Verificar se email já existe
        cursor.execute("SELECT email FROM usuarios WHERE email = ?", (email,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "E-mail já cadastrado!")
            return
        
        # Selecionar dieta
        dieta = self.selecionar_dieta()
        if not dieta:
            return
        
        # Pergunta de segurança
        pergunta, resposta = self.selecionar_pergunta_seguranca()
        if not pergunta or not resposta:
            return
        
        # Calcular IMC
        imc = peso / (altura ** 2)
        
        # Inserir no banco
        try:
            cursor.execute("""
                INSERT INTO usuarios (email, senha, peso, altura, sexo, dieta, imc, pergunta_seguranca, resposta_seguranca)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (email, senha, peso, altura, sexo, dieta, imc, pergunta, resposta))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.criar_menu_principal()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível cadastrar: {str(e)}")

    def selecionar_dieta(self):
        """Abre uma janela para seleção da dieta"""
        janela = tk.Toplevel(self.root)
        janela.title("Selecionar Dieta")
        janela.geometry("400x300")
        
        ttk.Label(janela, text="Selecione sua dieta:", style='Titulo.TLabel').pack(pady=20)
        
        dieta_var = tk.StringVar()
        dietas = ["Low carb", "Cetogênica", "Hiperproteica", "Bulking"]
        
        for dieta in dietas:
            ttk.Radiobutton(janela, text=dieta, variable=dieta_var, value=dieta).pack(pady=5)
        
        def confirmar():
            if not dieta_var.get():
                messagebox.showerror("Erro", "Selecione uma dieta!")
                return
            janela.destroy()
        
        frame_botoes = ttk.Frame(janela)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Confirmar", style='BotaoPrimario.TButton',
                command=confirmar).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=10)
        
        self.root.wait_window(janela)
        return dieta_var.get()

    def selecionar_pergunta_seguranca(self):
        """Abre uma janela para seleção da pergunta de segurança"""
        janela = tk.Toplevel(self.root)
        janela.title("Pergunta de Segurança")
        janela.geometry("500x400")
        
        ttk.Label(janela, text="Selecione uma pergunta de segurança:", style='Titulo.TLabel').pack(pady=10)
        
        perguntas = [
            "Qual é o nome do seu primeiro animal de estimação?",
            "Qual é a sua comida favorita?",
            "Qual cidade você nasceu?"
        ]
        
        pergunta_var = tk.StringVar()
        for i, pergunta in enumerate(perguntas, 1):
            ttk.Radiobutton(janela, text=pergunta, variable=pergunta_var, value=pergunta).pack(pady=5, anchor=tk.W)
        
        ttk.Label(janela, text="Resposta:").pack(pady=10, anchor=tk.W)
        resposta_entry = ttk.Entry(janela)
        resposta_entry.pack(pady=5, fill=tk.X, padx=20)
        
        def confirmar():
            if not pergunta_var.get() or not resposta_entry.get().strip():
                messagebox.showerror("Erro", "Selecione uma pergunta e digite uma resposta!")
                return
            self.pergunta_selecionada = pergunta_var.get()
            self.resposta_selecionada = resposta_entry.get().strip().lower()
            janela.destroy()
        
        frame_botoes = ttk.Frame(janela)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Confirmar", style='BotaoPrimario.TButton',
                command=confirmar).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=10)
        
        self.root.wait_window(janela)
        return (self.pergunta_selecionada, self.resposta_selecionada) if hasattr(self, 'pergunta_selecionada') else (None, None)

    def mostrar_tela_login(self):
        """Exibe a tela de login"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        ttk.Label(frame_principal, text="Login", style='Titulo.TLabel').pack(pady=20)
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(frame_form, text="E-mail:").pack(pady=10)
        self.login_email = ttk.Entry(frame_form)
        self.login_email.pack(pady=10, padx=20, fill=tk.X)
        
        ttk.Label(frame_form, text="Senha:").pack(pady=10)
        self.login_senha = ttk.Entry(frame_form, show="*")
        self.login_senha.pack(pady=10, padx=20, fill=tk.X)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Entrar", style='BotaoPrimario.TButton',
                command=self.fazer_login).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Recuperar Senha",
                command=self.mostrar_recuperacao_senha).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=10)

    def fazer_login(self):
        """Autentica o usuário no sistema"""
        email = self.login_email.get().strip()
        senha = self.login_senha.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        cursor.execute("SELECT senha FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] == senha:
            self.usuario_atual = email
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.criar_menu_principal()
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos!")

    def mostrar_recuperacao_senha(self):
        """Exibe a tela de recuperação de senha"""
        janela = tk.Toplevel(self.root)
        janela.title("Recuperar Senha")
        janela.geometry("500x300")
        
        ttk.Label(janela, text="Recuperação de Senha", style='Titulo.TLabel').pack(pady=20)
        
        frame_form = ttk.Frame(janela, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(frame_form, text="E-mail cadastrado:").pack(pady=10)
        self.rec_email = ttk.Entry(frame_form)
        self.rec_email.pack(pady=10, padx=20, fill=tk.X)
        
        def recuperar():
            email = self.rec_email.get().strip()
            
            if not email:
                messagebox.showerror("Erro", "Digite seu e-mail!")
                return
                
            cursor.execute("""
                SELECT pergunta_seguranca, resposta_seguranca, senha 
                FROM usuarios 
                WHERE email = ?
            """, (email,))
            resultado = cursor.fetchone()
            
            if not resultado:
                messagebox.showerror("Erro", "E-mail não encontrado!")
                return
                
            pergunta, resposta, senha = resultado
            
            janela_pergunta = tk.Toplevel(janela)
            janela_pergunta.title("Pergunta de Segurança")
            janela_pergunta.geometry("500x300")
            
            ttk.Label(janela_pergunta, text=pergunta, style='Titulo.TLabel').pack(pady=20)
            
            ttk.Label(janela_pergunta, text="Resposta:").pack(pady=10)
            self.rec_resposta = ttk.Entry(janela_pergunta)
            self.rec_resposta.pack(pady=10, padx=20, fill=tk.X)
            
            def verificar():
                if self.rec_resposta.get().strip().lower() == resposta.lower():
                    messagebox.showinfo("Sua Senha", f"Sua senha é: {senha}")
                    janela_pergunta.destroy()
                    janela.destroy()
                else:
                    messagebox.showerror("Erro", "Resposta incorreta!")
            
            ttk.Button(janela_pergunta, text="Verificar", style='BotaoPrimario.TButton',
                    command=verificar).pack(pady=20)
        
        frame_botoes = ttk.Frame(janela)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Recuperar", style='BotaoPrimario.TButton',
                command=recuperar).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Cancelar", command=janela.destroy).pack(side=tk.LEFT, padx=10)

    def mostrar_tela_admin(self):
        """Exibe a tela de login administrativo"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=50, pady=50)
        
        ttk.Label(frame_principal, text="Acesso Administrador", style='Titulo.TLabel').pack(pady=20)
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(frame_form, text="Senha:").pack(pady=10)
        self.admin_senha = ttk.Entry(frame_form, show="*")
        self.admin_senha.pack(pady=10, padx=20, fill=tk.X)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Entrar", style='BotaoPrimario.TButton',
                command=self.verificar_admin).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.criar_menu_principal).pack(side=tk.LEFT, padx=10)

    def verificar_admin(self):
        """Verifica a senha de administrador"""
        if self.admin_senha.get() == "admin123":
            self.mostrar_menu_admin()
        else:
            messagebox.showerror("Erro", "Senha incorreta!")

    def mostrar_menu_admin(self):
        """Exibe o menu administrativo"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Menu Administrador", style='Titulo.TLabel').pack(pady=10)
        
        frame_grade = ttk.Frame(frame_principal)
        frame_grade.pack(expand=True, fill=tk.BOTH, pady=20)
        
        opcoes = [
            ("Cadastrar Alimento", "Adicione novos alimentos", self.mostrar_cadastro_alimento),
            ("Listar Alimentos", "Visualize todos os alimentos", self.mostrar_lista_alimentos_admin),
            ("Listar Usuários", "Veja todos os usuários", self.mostrar_lista_usuarios_admin),
            ("Excluir Alimento", "Remova alimentos", self.mostrar_exclusao_alimento),
            ("Gerenciar Suporte", "Responda mensagens", self.mostrar_suporte_admin),
            ("Voltar", "Retornar ao menu", self.criar_menu_principal)
        ]
        
        for i, (titulo, descricao, comando) in enumerate(opcoes):
            linha, coluna = divmod(i, 3)
            
            card = ttk.Frame(frame_grade, style='Card.TFrame', width=300, height=150)
            card.grid(row=linha, column=coluna, padx=10, pady=10, sticky='nsew')
            card.grid_propagate(False)
            
            ttk.Label(card, text=titulo, style='Titulo.TLabel').pack(pady=10)
            ttk.Label(card, text=descricao, wraplength=280).pack(pady=5, padx=10)
            
            if comando:
                ttk.Button(card, text="Acessar", style='BotaoPrimario.TButton', 
                        command=comando).pack(pady=10, ipadx=20)
            
            frame_grade.grid_rowconfigure(linha, weight=1)
            frame_grade.grid_columnconfigure(coluna, weight=1)

    def mostrar_cadastro_alimento(self):
        """Exibe a tela de cadastro de alimentos (admin)"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Cadastrar Alimento", style='Titulo.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(frame_form, text="Nome do Alimento:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.alimento_nome = ttk.Entry(frame_form)
        self.alimento_nome.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        ttk.Label(frame_form, text="Calorias (por 100g):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.alimento_calorias = ttk.Entry(frame_form)
        self.alimento_calorias.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Cadastrar", style='BotaoPrimario.TButton',
                command=self.cadastrar_alimento).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.mostrar_menu_admin).pack(side=tk.LEFT, padx=10)

    def cadastrar_alimento(self):
        """Processa o cadastro de um novo alimento (admin)"""
        nome = self.alimento_nome.get().strip().lower()
        calorias = self.alimento_calorias.get().strip()
        
        if not nome or not calorias:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        try:
            calorias = float(calorias)
            if calorias <= 0:
                messagebox.showerror("Erro", "Calorias devem ser maiores que zero!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor numérico válido para calorias!")
            return
        
        # Verificar se alimento já existe
        cursor.execute("SELECT nome FROM alimentos WHERE nome = ?", (nome,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Alimento já cadastrado!")
            return
        
        # Inserir no banco
        try:
            cursor.execute("INSERT INTO alimentos (nome, calorias) VALUES (?, ?)", (nome, calorias))
            conn.commit()
            messagebox.showinfo("Sucesso", "Alimento cadastrado com sucesso!")
            self.mostrar_menu_admin()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível cadastrar: {str(e)}")

    def mostrar_lista_alimentos_admin(self):
        """Exibe a lista de alimentos cadastrados (admin)"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Lista de Alimentos", style='Titulo.TLabel').pack(pady=10)
        
        frame_tabela = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_tabela.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        tabela = ttk.Treeview(frame_tabela, columns=("Alimento", "Calorias"), show="headings", height=15)
        
        tabela.heading("Alimento", text="Alimento")
        tabela.heading("Calorias", text="Calorias (por 100g)")
        
        tabela.column("Alimento", width=300, anchor=tk.W)
        tabela.column("Calorias", width=150, anchor=tk.CENTER)
        
        scroll = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tabela.pack(expand=True, fill=tk.BOTH)
        
        cursor.execute("SELECT nome, calorias FROM alimentos ORDER BY nome")
        for linha in cursor.fetchall():
            tabela.insert("", tk.END, values=linha)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Atualizar", command=self.mostrar_lista_alimentos_admin).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Voltar", command=self.mostrar_menu_admin).pack(side=tk.LEFT, padx=5)

    def mostrar_lista_usuarios_admin(self):
        """Exibe a lista de usuários cadastrados (admin)"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Lista de Usuários", style='Titulo.TLabel').pack(pady=10)
        
        frame_tabela = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_tabela.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        colunas = ("Email", "Peso", "Altura", "Sexo", "Dieta", "IMC")
        tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
        
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=120, anchor=tk.CENTER)
        
        tabela.column("Email", width=200, anchor=tk.W)
        tabela.column("Dieta", width=120)
        
        scroll = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela.yview)
        tabela.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tabela.pack(expand=True, fill=tk.BOTH)
        
        cursor.execute("SELECT email, peso, altura, sexo, dieta, imc FROM usuarios")
        for linha in cursor.fetchall():
            tabela.insert("", tk.END, values=linha)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Atualizar", command=self.mostrar_lista_usuarios_admin).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Voltar", command=self.mostrar_menu_admin).pack(side=tk.LEFT, padx=5)

    def mostrar_exclusao_alimento(self):
        """Exibe a tela de exclusão de alimentos (admin)"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Excluir Alimento", style='Titulo.TLabel').pack(pady=10)
        
        frame_form = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_form.pack(pady=20, padx=50, fill=tk.X)
        
        ttk.Label(frame_form, text="Nome do Alimento:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.excluir_alimento_nome = ttk.Entry(frame_form)
        self.excluir_alimento_nome.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Excluir", style='BotaoPrimario.TButton',
                command=self.excluir_alimento).pack(side=tk.LEFT, padx=10)
        ttk.Button(frame_botoes, text="Voltar", command=self.mostrar_menu_admin).pack(side=tk.LEFT, padx=10)

    def excluir_alimento(self):
        """Processa a exclusão de um alimento (admin)"""
        nome = self.excluir_alimento_nome.get().strip().lower()
        
        if not nome:
            messagebox.showerror("Erro", "Digite o nome do alimento!")
            return
            
        cursor.execute("SELECT nome FROM alimentos WHERE nome = ?", (nome,))
        if not cursor.fetchone():
            messagebox.showerror("Erro", "Alimento não encontrado!")
            return
            
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o alimento '{nome}'?"):
            try:
                cursor.execute("DELETE FROM alimentos WHERE nome = ?", (nome,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Alimento excluído com sucesso!")
                self.mostrar_menu_admin()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir: {str(e)}")

    def mostrar_suporte_admin(self):
        """Exibe a interface de suporte para administradores"""
        self.limpar_tela()
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        ttk.Label(frame_principal, text="Gerenciar Suporte", style='Titulo.TLabel').pack(pady=10)
        
        frame_tabela = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_tabela.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        colunas = ("ID", "Email", "Mensagem", "Resposta")
        self.tabela_suporte_admin = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
        
        for col in colunas:
            self.tabela_suporte_admin.heading(col, text=col)
            self.tabela_suporte_admin.column(col, width=150, anchor=tk.W)
        
        self.tabela_suporte_admin.column("ID", width=50)
        self.tabela_suporte_admin.column("Mensagem", width=300)
        
        scroll = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tabela_suporte_admin.yview)
        self.tabela_suporte_admin.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabela_suporte_admin.pack(expand=True, fill=tk.BOTH)
        
        frame_resposta = ttk.Frame(frame_principal, style='Card.TFrame')
        frame_resposta.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_resposta, text="Responder:").pack(pady=5, anchor=tk.W)
        self.texto_resposta_admin = scrolledtext.ScrolledText(frame_resposta, width=80, height=5, wrap=tk.WORD)
        self.texto_resposta_admin.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Enviar Resposta", style='BotaoPrimario.TButton',
                command=self.enviar_resposta_admin).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Atualizar", command=self.carregar_suporte_admin).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Voltar", command=self.mostrar_menu_admin).pack(side=tk.LEFT, padx=5)
        
        self.carregar_suporte_admin()
        self.tabela_suporte_admin.bind("<<TreeviewSelect>>", self.selecionar_mensagem_suporte)

    def carregar_suporte_admin(self):
        """Carrega as mensagens de suporte para o administrador"""
        for item in self.tabela_suporte_admin.get_children():
            self.tabela_suporte_admin.delete(item)
            
        cursor.execute("""
            SELECT id, email, mensagem, resposta 
            FROM suporte 
            ORDER BY data_hora DESC
        """)
        
        for linha in cursor.fetchall():
            self.tabela_suporte_admin.insert("", tk.END, values=linha)

    def selecionar_mensagem_suporte(self, event):
        """Seleciona uma mensagem de suporte para resposta"""
        selecionado = self.tabela_suporte_admin.focus()
        if selecionado:
            valores = self.tabela_suporte_admin.item(selecionado, "values")
            self.id_mensagem_selecionada = valores[0]
            self.texto_resposta_admin.delete("1.0", tk.END)
            if valores[3]:
                self.texto_resposta_admin.insert(tk.END, valores[3])

    def enviar_resposta_admin(self):
        """Envia uma resposta para uma mensagem de suporte"""
        if not hasattr(self, 'id_mensagem_selecionada'):
            messagebox.showerror("Erro", "Selecione uma mensagem para responder!")
            return
            
        resposta = self.texto_resposta_admin.get("1.0", tk.END).strip()
        
        if not resposta:
            messagebox.showerror("Erro", "Digite uma resposta!")
            return
            
        try:
            cursor.execute("""
                UPDATE suporte 
                SET resposta = ? 
                WHERE id = ?
            """, (resposta, self.id_mensagem_selecionada))
            conn.commit()
            messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
            self.carregar_suporte_admin()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível enviar a resposta: {str(e)}")

    def fazer_logout(self):
        """Realiza o logout do usuário atual"""
        self.usuario_atual = None
        self.criar_menu_principal()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceNutrismart(root)
    root.mainloop()