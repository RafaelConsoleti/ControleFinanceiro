import mysql.connector 

def conectar():
   
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