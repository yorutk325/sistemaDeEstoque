import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import banco_dados  
id_editando = None



   

def salvar_produto():
    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    preco_str = entry_preco.get().strip()
    categoria = entry_categoria.get().strip()


    if not nome or not quantidade_str or not preco_str or not categoria:
        messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
        return
    

    
    try:
        quantidade = int(quantidade_str)
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
    except ValueError:
        messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo.")
        return
    

    try:
        preco = float(preco_str)
        if preco < 0:
            raise ValueError("Preço não pode ser negativo.")
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser um número decimal positivo (ex: 10.50).")
        return
    

    sucesso = banco_dados.salvar_produto(nome, quantidade, preco, categoria)
    if sucesso:
        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_categoria.delete(0, tk.END)
    else:
        messagebox.showerror("Erro", "Erro ao salvar produto. Verifique o console para detalhes.")

        global id_editando
    if id_editando is not None:
       sucesso = banco_dados.atualizar_produto(id_editando, nome, quantidade, preco, categoria)
       if sucesso:
           messagebox.showinfo("Sucesso", "Produto atualizado!")
           id_editando = None
  
    else:
       sucesso = banco_dados.salvar_produto(nome, quantidade, preco, categoria)

def listar_produtos():
    produtos = banco_dados.listar_produtos()
    
    janela_lista = tk.Toplevel(janela)
    janela_lista.title("Lista de Produtos")
    janela_lista.geometry("800x500")
    
    titulo_lista = tk.Label(janela_lista, text="Estoque Atual", font=("Arial", 14, "bold"))
    titulo_lista.pack(pady=10)
    
    if not produtos:
        msg_vazia = tk.Label(janela_lista, text="Nenhum produto cadastrado ainda.", font=("Arial", 12))
        msg_vazia.pack(pady=20)
        return
    
    frame_tabela = tk.Frame(janela_lista)
    frame_tabela.pack(pady=10, padx=10, fill="both", expand=True)
    
    colunas = ("ID", "Nome", "Quantidade", "Preço", "Categoria")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
    
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço", text="Preço (R$)")
    tree.heading("Categoria", text="Categoria")
    
    tree.column("ID", width=50)
    tree.column("Nome", width=200)
    tree.column("Quantidade", width=100)
    tree.column("Preço", width=100)
    tree.column("Categoria", width=150)
    
    for prod in produtos:
        tree.insert("", tk.END, values=(prod[0], prod[1], prod[2], f"R$ {prod[3]:.2f}", prod[4] or "N/A"))
    
    scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    frame_botoes = tk.Frame(janela_lista)
    frame_botoes.pack(pady=10)
    
    def editar_selecionado():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para editar.")
            return
        item = tree.item(selecionado)
        valores = item['values']

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])
        entry_quantidade.delete(0, tk.END)
        entry_quantidade.insert(0, valores[2])
        entry_preco.delete(0, tk.END)
        entry_preco.insert(0, valores[3].replace("R$ ", ""))
        entry_categoria.delete(0, tk.END)
        entry_categoria.insert(0, valores[4] if valores[4] != "N/A" else "")
        global id_editando
        id_editando = valores[0]
        messagebox.showinfo("Editar", "Dados carregados no formulário. Altere e salve.")
        janela_lista.destroy()
    
    def deletar_selecionado():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para deletar.")
            return
        if messagebox.askyesno("Confirmar", "Tem certeza que quer deletar este produto?"):
            item = tree.item(selecionado)
            id_prod = item['values'][0]
            if banco_dados.deletar_produto(id_prod):
                messagebox.showinfo("Sucesso", "Produto deletado!")
                janela_lista.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao deletar.")
    
    btn_editar = tk.Button(frame_botoes, text="Editar Selecionado", command=editar_selecionado, 
                           bg="#FF9800", fg="white", padx=10)
    btn_editar.pack(side=tk.LEFT, padx=5)
    
    btn_deletar = tk.Button(frame_botoes, text="Deletar Selecionado", command=deletar_selecionado, 
                            bg="#f44336", fg="white", padx=10)
    btn_deletar.pack(side=tk.LEFT, padx=5)
    
    btn_fechar = tk.Button(frame_botoes, text="Fechar", command=janela_lista.destroy, 
                           bg="#9E9E9E", fg="white", padx=10)
    btn_fechar.pack(side=tk.LEFT, padx=5)

banco_dados.criar_tabela()

janela = tk.Tk()
janela.title("Cadastro de Produtos - Estoque")
janela.geometry("600x400")


titulo = tk.Label(janela, text="Cadastro de Produtos", font=("Arial", 16, "bold"))
titulo.pack(pady=10)


frame_form = tk.Frame(janela)
frame_form.pack(pady=20, padx=20, fill="x")


tk.Label(frame_form, text="Nome do Produto:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nome = tk.Entry(frame_form, width=40)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Quantidade:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_quantidade = tk.Entry(frame_form, width=40)
entry_quantidade.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Preço (R$):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_preco = tk.Entry(frame_form, width=40)
entry_preco.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_form, text="Categoria:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_categoria = tk.Entry(frame_form, width=40)
entry_categoria.grid(row=3, column=1, padx=10, pady=5)


btn_salvar = tk.Button(janela, text="Salvar Produto", command=salvar_produto, 
                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                       padx=20, pady=10)
btn_salvar.pack(pady=20)

btn_listar = tk.Button(janela, text="Listar Produtos", command=listar_produtos, 
                       bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                       padx=20, pady=10)
btn_listar.pack(pady=5)


janela.mainloop()