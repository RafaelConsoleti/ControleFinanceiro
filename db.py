import mysql.connector

def conectar():
    # Estabelece conexão com o banco de dados
    return mysql.connector.connect(
        host="localhost",
        user="root",      
        password="1234",    
        database="financas"
    )

def inserir_transacao(tipo, categoria, valor, descricao):
    """
    Insere uma nova transação no banco.
    """
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO transacoes (tipo, categoria, valor, descricao)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (tipo, categoria, valor, descricao))
    conn.commit()

    cursor.close()
    conn.close()

def listar_transacoes():
    """
    Retorna todas as transações do banco, ordenadas pela data mais recente.
    """
    conn = conectar()
    cursor = conn.cursor()

    sql = "SELECT id, tipo, categoria, valor, descricao, data FROM transacoes ORDER BY data DESC"
    cursor.execute(sql)

    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados

def deletar_transacao_por_id(transacao_id):
    """
    Deleta uma transação específica pelo ID.
    """
    conn = conectar()
    cursor = conn.cursor()

    sql = "DELETE FROM transacoes WHERE id = %s"
    cursor.execute(sql, (transacao_id,))
    conn.commit()

    cursor.close()
    conn.close()

    reordenar_ids()  # Reorganiza os IDs após a exclusão

def deletar_todas_transacoes():
    """
    Deleta todas as transações do banco.
    """
    conn = conectar()
    cursor = conn.cursor()

    sql = "DELETE FROM transacoes"
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    reordenar_ids()  # Reorganiza os IDs após exclusão em massa

def reordenar_ids():
    """
    Reorganiza os IDs para manter a sequência contínua após exclusões.
    """
    conn = conectar()
    cursor = conn.cursor()

    # Reinicia o contador
    cursor.execute("SET @contador = 0")

    # Atualiza os IDs sequencialmente
    cursor.execute("""
        UPDATE transacoes 
        SET id = (@contador := @contador + 1)
        ORDER BY data ASC
    """)

    # Atualiza o AUTO_INCREMENT para o próximo valor
    cursor.execute("SELECT MAX(id) FROM transacoes")
    max_id = cursor.fetchone()[0] or 0
    cursor.execute(f"ALTER TABLE transacoes AUTO_INCREMENT = {max_id + 1}")

    conn.commit()
    conn.close()
