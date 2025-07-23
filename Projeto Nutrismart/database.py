import sqlite3
from datetime import datetime

# Conexão com banco SQLite
conn = sqlite3.connect('nutricao.db')
cursor = conn.cursor()

def criar_tabelas():
    """
    Cria as tabelas necessárias no banco de dados caso não existam.
    
    Cria as tabelas:
    - usuarios: Armazena informações dos usuários
    - alimentos: Armazena dados nutricionais dos alimentos
    - refeicoes: Registra as refeições dos usuários
    - registro_refeicoes: Tabela legada mantida para compatibilidade
    - suporte: Armazena mensagens de suporte
    
    A função não retorna valores, mas faz commit das alterações no banco.
    """
    # Tabela de usuários
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

    # Tabela de alimentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentos (
            nome TEXT PRIMARY KEY,
            calorias REAL NOT NULL,
            proteinas REAL DEFAULT 0,
            carboidratos REAL DEFAULT 0,
            gorduras REAL DEFAULT 0
        )
    ''')

    # Tabela de refeições (ATUALIZADA)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS refeicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_usuario TEXT NOT NULL,
            alimento TEXT NOT NULL,
            quantidade_gramas REAL NOT NULL,
            calorias REAL NOT NULL,  -- COLUNA ADICIONADA
            data TEXT NOT NULL,
            FOREIGN KEY (email_usuario) REFERENCES usuarios(email),
            FOREIGN KEY (alimento) REFERENCES alimentos(nome)
        )
    ''')

    # Tabela de registro de refeições (mantida para compatibilidade)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registro_refeicoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            refeicao TEXT NOT NULL,
            calorias INTEGER,
            data TEXT NOT NULL
        )
    ''')

    # Tabela de suporte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suporte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            mensagem TEXT NOT NULL,
            resposta TEXT,
            data_hora TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()

def migrar_dados():
    """
    Realiza migração de dados para a nova estrutura do banco.
    
    Adiciona a coluna 'calorias' na tabela refeicoes se não existir e
    calcula os valores com base nos alimentos registrados.
    
    Caso ocorra erro durante a migração, faz rollback das alterações.
    """
    try:
        # Adiciona coluna calorias se não existir
        cursor.execute("PRAGMA table_info(refeicoes)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        if 'calorias' not in colunas:
            cursor.execute('ALTER TABLE refeicoes ADD COLUMN calorias REAL NOT NULL DEFAULT 0')
            
            # Calcula calorias para registros existentes
            cursor.execute('''
                UPDATE refeicoes 
                SET calorias = (
                    SELECT (refeicoes.quantidade_gramas/100) * alimentos.calorias 
                    FROM alimentos 
                    WHERE alimentos.nome = refeicoes.alimento
                )
                WHERE EXISTS (
                    SELECT 1 FROM alimentos 
                    WHERE alimentos.nome = refeicoes.alimento
                )
            ''')
            conn.commit()
            print("Migração de dados concluída com sucesso!")
            
    except Exception as e:
        print(f"Erro durante migração: {e}")
        conn.rollback()

def mostrar_estrutura():
    """
    Exibe a estrutura atual do banco de dados.
    
    Mostra todas as tabelas existentes e suas colunas com tipos de dados.
    Útil para verificação e depuração.
    """
    print("\nESTRUTURA DO BANCO DE DADOS:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = cursor.fetchall()
    
    for tabela in tabelas:
        print(f"\nTabela: {tabela[0]}")
        cursor.execute(f"PRAGMA table_info({tabela[0]})")
        for coluna in cursor.fetchall():
            print(f"  {coluna[1]} ({coluna[2]})")

# Executa a criação das tabelas e migração
criar_tabelas()
migrar_dados()

# Mostra a estrutura ao executar 
if __name__ == "__main__":
    mostrar_estrutura()