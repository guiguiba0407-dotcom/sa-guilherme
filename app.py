import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "sa-guilherme-estoque-key-segura"
DB_PATH = "estoque.db"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    """)
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


# Decorador que exige login para acessar o estoque
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar o controle de estoque.", "erro")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# --- ROTAS DE AUTENTICAÇÃO ---

@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip().lower()
        senha = request.form.get("senha", "")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        conta = cursor.fetchone()
        conn.close()

        if conta and check_password_hash(conta["senha_hash"], senha):
            session["usuario_id"] = conta["id"]
            session["usuario_nome"] = conta["nome"]
            flash(f"Bem-vindo(a), {conta['nome']}!", "ok")
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha incorretos.", "erro")

    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if "usuario_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        usuario = request.form.get("usuario", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")

        if not nome or not usuario or not senha:
            flash("Preencha todos os campos.", "erro")
            return redirect(url_for("registro"))

        if len(senha) < 4:
            flash("A senha deve ter pelo menos 4 caracteres.", "erro")
            return redirect(url_for("registro"))

        if senha != confirmar:
            flash("As senhas não coincidem.", "erro")
            return redirect(url_for("registro"))

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nome, usuario, senha_hash) VALUES (?, ?, ?)",
                (nome, usuario, generate_password_hash(senha)),
            )
            conn.commit()
            conn.close()
            flash("Conta criada com sucesso! Agora faça seu login.", "ok")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash(f"O nome de usuário '{usuario}' já está em uso.", "erro")

    return render_template("registro.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "ok")
    return redirect(url_for("login"))


# --- ROTAS DO ESTOQUE (PROTEGIDAS) ---

@app.route("/")
@login_obrigatorio
def index():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, quantidade, preco FROM produtos ORDER BY id")
    produtos = cursor.fetchall()
    conn.close()

    soma_geral = sum(p["quantidade"] * p["preco"] for p in produtos)
    total_itens = sum(p["quantidade"] for p in produtos)

    return render_template(
        "index.html",
        produtos=produtos,
        soma_geral=soma_geral,
        total_itens=total_itens,
        usuario_nome=session.get("usuario_nome"),
    )


@app.route("/cadastrar", methods=["POST"])
@login_obrigatorio
def cadastrar():
    nome = request.form.get("nome", "").strip()
    try:
        quantidade = int(request.form.get("quantidade", 0))
        preco = float(request.form.get("preco", "0").replace(",", "."))

        if not nome:
            flash("O nome do produto não pode ficar vazio.", "erro")
            return redirect(url_for("index"))

        if quantidade < 0 or preco < 0:
            flash("Quantidade e preço não podem ser negativos.", "erro")
            return redirect(url_for("index"))

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
            (nome, quantidade, preco),
        )
        conn.commit()
        conn.close()
        flash(f"Produto '{nome}' cadastrado com sucesso!", "ok")
    except sqlite3.IntegrityError:
        flash(f"O produto '{nome}' já existe no estoque.", "erro")
    except ValueError:
        flash("Digite números válidos para quantidade e preço.", "erro")

    return redirect(url_for("index"))


@app.route("/movimentar/<int:produto_id>", methods=["POST"])
@login_obrigatorio
def movimentar(produto_id):
    acao = request.form.get("acao")
    try:
        qtd = int(request.form.get("qtd", 0))
        if qtd <= 0:
            flash("A quantidade deve ser maior que zero.", "erro")
            return redirect(url_for("index"))

        delta = qtd if acao == "entrada" else -qtd

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, quantidade FROM produtos WHERE id = ?", (produto_id,))
        produto = cursor.fetchone()

        if not produto:
            flash("Produto não encontrado.", "erro")
        else:
            nova_qtd = produto["quantidade"] + delta
            if nova_qtd < 0:
                flash(
                    f"Estoque insuficiente para '{produto['nome']}'. Disponível: {produto['quantidade']}.",
                    "erro",
                )
            else:
                cursor.execute(
                    "UPDATE produtos SET quantidade = ? WHERE id = ?",
                    (nova_qtd, produto_id),
                )
                conn.commit()
                flash(f"'{produto['nome']}' atualizado para {nova_qtd} unidades.", "ok")
        conn.close()
    except ValueError:
        flash("Digite apenas números inteiros.", "erro")

    return redirect(url_for("index"))


@app.route("/excluir/<int:produto_id>", methods=["POST"])
@login_obrigatorio
def excluir(produto_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
    flash("Produto excluído do estoque.", "ok")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)