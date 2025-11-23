import sqlite3
import os
from datetime import datetime

def db_path():
    return os.path.join(os.path.dirname(__file__), "produtos.db")

def conectar():
    caminho = db_path()
    conexao = sqlite3.connect(caminho)
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            categoria TEXT
        )
    ''')
    conexao.commit()
    conexao.close()

def salvar_produto(nome, quantidade, preco, categoria):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, quantidade, preco, categoria)
            VALUES (?, ?, ?, ?)
        ''', (nome, quantidade, preco, categoria))
        conexao.commit()
        return True
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return False
    finally:
        conexao.close()





def listar_produtos():
       try:
           conexao = conectar()
           cursor = conexao.cursor()
           cursor.execute("SELECT id, nome, quantidade, preco, categoria FROM produtos ORDER BY nome")
           produtos = cursor.fetchall()
           return produtos
       except Exception as e:
           print(f"Erro ao listar: {e}")
           return []
       finally:
           if 'conexao' in locals():
               conexao.close()
   

if __name__ == "__main__":
    criar_tabela()
    caminho = db_path()
    print("Tabela 'produtos' criada (ou já existia).")
    print("Arquivo produtos.db em:", caminho)
    if os.path.exists(caminho):
        info = os.stat(caminho)
        print("Tamanho (bytes):", info.st_size)
        print("Última modificação:", datetime.fromtimestamp(info.st_mtime))

def atualizar_produto(id_produto, nome, quantidade, preco, categoria):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('''
            UPDATE produtos 
            SET nome=?, quantidade=?, preco=?, categoria=? 
            WHERE id=?
        ''', (nome, quantidade, preco, categoria, id_produto))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao atualizar: {e}")
        return False
    finally:
        if 'conexao' in locals():
            conexao.close()

def deletar_produto(id_produto):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        return False
    finally:
        if 'conexao' in locals():
            conexao.close()