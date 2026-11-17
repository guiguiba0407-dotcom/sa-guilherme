

import os
import sqlite3
import time
import keyboard


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def conectar():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            quantidade INTEGER NOT NULL DEFAULT 0,
            preco REAL NOT NULL DEFAULT 0.0
        )
    """)
    conn.commit()
    return conn


def obter_todos_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, preco FROM produtos ORDER BY id")
    produtos = cursor.fetchall()
    conn.close()
    return produtos


def cadastrar_produto(nome, quantidade, preco):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
            (nome, quantidade, preco),
        )
        conn.commit()
        print(f"\n[OK] Produto '{nome}' cadastrado!")
    except sqlite3.IntegrityError:
        print(f"\n[ERRO] O produto '{nome}' já existe.")
    finally:
        conn.close()


def listar_produtos():
    produtos = obter_todos_produtos()
    print("\n--- ESTOQUE ATUAL ---")
    if not produtos:
        print("Nenhum produto cadastrado.")
        print("-" * 68)
    else:
        print(
            f"{'ID':<4} | {'PRODUTO':<25} | {'QTD':<6} | {'PREÇO':<10} | {'TOTAL':<12}"
        )
        print("-" * 68)
        soma_geral = 0.0
        for p in produtos:
            total_item = p[2] * p[3]
            soma_geral += total_item
            print(
                f"{p[0]:<4} | {p[1]:<25} | {p[2]:<6} | R$ {p[3]:<7.2f} | R$ {total_item:<9.2f}"
            )
        print("-" * 68)
        print(f"{'VALOR TOTAL DE TODO O ESTOQUE SOMADO:':<52} R$ {soma_geral:.2f}")
        print("-" * 68)


def movimentar_estoque(produto_id, delta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        print("\n[ERRO] Produto não encontrado.")
    else:
        nova_qtd = produto[1] + delta
        if nova_qtd < 0:
            print(f"\n[ERRO] Estoque insuficiente. Disponível: {produto[1]}.")
        else:
            cursor.execute(
                "UPDATE produtos SET quantidade = ? WHERE id = ?",
                (nova_qtd, produto_id),
            )
            conn.commit()
            print(f"\n[OK] '{produto[0]}' atualizado para {nova_qtd} unidades.")
    conn.close()


def excluir_produto(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    if cursor.rowcount > 0:
        conn.commit()
        print("\n[OK] Produto excluído!")
    else:
        print("\n[ERRO] Produto não encontrado.")
    conn.close()


def selecionar_produto_horizontal(titulo_acao):
    produtos = obter_todos_produtos()
    if not produtos:
        limpar_tela()
        print(f"--- {titulo_acao} ---")
        print("\nNenhum produto cadastrado no estoque.")
        return None

    indice = 0

    while True:
        limpar_tela()
        print(f"=== {titulo_acao} ===")
        print("Use [A] Esquerda | [D] Direita | [ENTER] Selecionar | [ESC] Voltar\n")

        linha_numeros = ""
        linha_cursor = ""

        for i, prod in enumerate(produtos):
            num_str = str(prod[0])
            largura = max(len(num_str), 3)

            linha_numeros += num_str.center(largura) + "  "
            if i == indice:
                linha_cursor += "º".center(largura) + "  "
            else:
                linha_cursor += " ".center(largura) + "  "

        print("Documentos / Itens:")
        print(linha_numeros)
        print(linha_cursor)

        selecionado = produtos[indice]
        valor_total_item = selecionado[2] * selecionado[3]

        print("-" * 50)
        print(f"Item selecionado : [{selecionado[0]}] {selecionado[1]}")
        print(f"Estoque atual    : {selecionado[2]} unidades")
        print(f"Preço unitário   : R$ {selecionado[3]:.2f}")
        print(f"Total deste item : R$ {valor_total_item:.2f}")
        print("-" * 50)

        while True:
            evento = keyboard.read_event(suppress=True)
            if evento.event_type == keyboard.KEY_DOWN:
                tecla = evento.name.lower()
                break

        time.sleep(0.12)

        if tecla in ["a", "left"]:
            if indice > 0:
                indice -= 1
        elif tecla in ["d", "right"]:
            if indice < len(produtos) - 1:
                indice += 1
        elif tecla == "enter":
            return selecionado
        elif tecla == "esc":
            return None


def pausar():
    print("\nPressione ESPAÇO ou ENTER para voltar ao menu...")
    while True:
        evento = keyboard.read_event(suppress=True)
        if evento.event_type == keyboard.KEY_DOWN and evento.name in [
            "space",
            "enter",
        ]:
            break


def menu():
    while True:
        limpar_tela()
        print("=== CONTROLE DE ESTOQUE (ATALHOS RÁPIDOS) ===")
        print("[1] Cadastrar Produto")
        print("[2] Listar Estoque")
        print("[3] Entrada de Estoque (+)")
        print("[4] Saída de Estoque (-)")
        print("[5] Excluir Produto")
        print("[ESC] Sair")
        print("\nAguardando tecla...")

        while True:
            evento = keyboard.read_event(suppress=True)
            if evento.event_type == keyboard.KEY_DOWN:
                tecla = evento.name.lower()
                break

        time.sleep(0.15)

        if tecla == "1":
            limpar_tela()
            print("--- NOVO PRODUTO ---")
            nome = input("Nome do produto: ").strip()
            try:
                qtd = int(input("Quantidade inicial: "))
                preco = float(input("Preço unitário: ").replace(",", "."))
                cadastrar_produto(nome, qtd, preco)
            except ValueError:
                print("\n[ERRO] Digite números válidos.")
            pausar()

        elif tecla == "2":
            limpar_tela()
            listar_produtos()
            pausar()

        elif tecla == "3":
            produto = selecionar_produto_horizontal("ENTRADA DE ESTOQUE (+)")
            if produto:
                try:
                    qtd = int(input(f"\nQuantidade a ADICIONAR em '{produto[1]}': "))
                    if qtd > 0:
                        movimentar_estoque(produto[0], qtd)
                    else:
                        print("\n[ERRO] A quantidade deve ser maior que zero.")
                except ValueError:
                    print("\n[ERRO] Digite apenas números inteiros.")
            pausar()

        elif tecla == "4":
            produto = selecionar_produto_horizontal("SAÍDA DE ESTOQUE (-)")
            if produto:
                try:
                    qtd = int(input(f"\nQuantidade a REMOVER de '{produto[1]}': "))
                    if qtd > 0:
                        movimentar_estoque(produto[0], -qtd)
                    else:
                        print("\n[ERRO] A quantidade deve ser maior que zero.")
                except ValueError:
                    print("\n[ERRO] Digite apenas números inteiros.")
            pausar()

        elif tecla == "5":
            limpar_tela()
            listar_produtos()
            try:
                pid = int(input("ID do produto para excluir: "))
                excluir_produto(pid)
            except ValueError:
                print("\n[ERRO] ID inválido.")
            pausar()

        elif tecla == "esc":
            limpar_tela()
            print("Encerrando sistema...")
            break


if __name__ == "__main__":
    menu()