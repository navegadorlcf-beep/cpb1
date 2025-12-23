
import streamlit as st
import random
import time
import sqlite3

# ==============================
# Corrige a aleatoriedade do Streamlit
# ==============================
random.seed(time.time_ns())   # seed forte, evita repetição
# ==============================


# Função para criar o banco de dados e a tabela
def criar_banco():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Função para inserir um usuário no banco de dados
def cadastrar_usuario(nome):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

# Função para excluir toda a lista de usuários com validação de senha
def excluir_todos_usuarios_com_senha(senha):
    if validar_senha(senha):
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
        conn.close()
        return True
    return False

# Função para obter a lista de nomes cadastrados
def obter_nomes_cadastrados():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios")
    nomes = cursor.fetchall()
    conn.close()
    return [nome[0] for nome in nomes]

# Função para validar a senha
def validar_senha(senha):
    return senha == "1289"

# Configuração inicial da página
st.set_page_config(page_title="Sorteio de Nomes", layout="centered")

# Título do app
st.title("🎉 rifas das lojas cpb.! ")
st.write("Bem-vindos aos nossos sorteios!")
st.markdown("**Para validar sua participação faça o seu pagamento pix neste email:**<br>📧 `lojascpb@gmail.com`", unsafe_allow_html=True)

# Criar banco
criar_banco()

# Cadastro de nomes
st.subheader("Cadastre o seu nome")
nome_input = st.text_input("Digite seu nome:")

if st.button("Cadastrar"):
    if nome_input.strip():
        cadastrar_usuario(nome_input)
        st.success(f"Usuário {nome_input} cadastrado com sucesso!")
        st.rerun()
    else:
        st.error("Por favor, insira um nome válido.")

# Exibir nomes cadastrados
st.subheader("Nomes Cadastrados:")
nomes_cadastrados = obter_nomes_cadastrados()

if nomes_cadastrados:
    st.table({"Nomes Cadastrados": nomes_cadastrados})

    st.subheader("Excluir Todos os Nomes")
    senha_exclusao = st.text_input("Senha para excluir tudo:", type="password")

    if st.button("Excluir Todos"):
        if excluir_todos_usuarios_com_senha(senha_exclusao):
            st.success("Todos os nomes foram excluídos!")
            st.rerun()
        else:
            st.error("Senha incorreta.")
else:
    st.write("Nenhum nome cadastrado ainda.")

# Senha para sorteio
senha_input = st.text_input("Digite a senha do sorteio:", type="password")

if validar_senha(senha_input):

    st.subheader("Sorteio")

    if nomes_cadastrados:

        if st.button("Sortear"):

            st.subheader("Sorteio iniciado...")
            countdown_placeholder = st.empty()

            # Contagem regressiva
            for i in range(10, 0, -1):
                countdown_placeholder.write(f"⏳ Sorteando em {i} segundos...")
                time.sleep(1)

            countdown_placeholder.empty()

            # ===================================
            #  SORTEIO REALMENTE ALEATÓRIO
            # ===================================
            indice = random.randrange(len(nomes_cadastrados))
            nome_sorteado = nomes_cadastrados[indice]
            # ===================================

            st.success(f"🎉 PARABÉNS! O ganhador(a) é: **{nome_sorteado}** 🎉")
            st.balloons()

    else:
        st.warning("Nenhum nome cadastrado.")
else:
    st.warning("Digite a senha correta para sortear.")

# Rodapé
st.markdown("---")
st.caption("Participe ❤ e ganhe você também!")