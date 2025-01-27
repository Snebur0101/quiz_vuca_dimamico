import streamlit as st
import sqlite3

# Conectar ao banco de dados SQLite (ele será criado se não existir)
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Criar a tabela de usuários (se não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    senha TEXT,
    tipo TEXT
)
''')

# Criar a tabela de perguntas (se não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS perguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pergunta TEXT,
    respostas TEXT,
    gabarito TEXT
)
''')

# Lista de usuários para inicializar a tabela (se estiver vazia)
usuarios = [
    {'nome': 'Marcos', 'senha': 'Torchic123', 'tipo': 'criador'},
    {'nome': 'Marcos123', 'senha': 'Torchic123', 'tipo': 'respondente'},
    {"nome": "Davi", "senha": "Davi123", "tipo": "respondente"},
    {"nome": "Felipe", "senha": "Felipe123", "tipo": "respondente"},
    {"nome": "Hiago", "senha": "Hiago123", "tipo": "respondente"},
    {"nome": "Ismael", "senha": "Ismael123", "tipo": "respondente"},
    {"nome": "Jônatas", "senha": "Jônatas123", "tipo": "respondente"},
    {"nome": "Levi", "senha": "Levi123", "tipo": "respondente"},
    {"nome": "Márcio", "senha": "Márcio123", "tipo": "respondente"},
    {"nome": "Pedro", "senha": "Pedro123", "tipo": "respondente"},
    {"nome": "Pedro2", "senha": "Pedro12345", "tipo": "criador"},
    {"nome": "Rubens", "senha": "Rubens123", "tipo": "respondente"},
    {"nome": "Tiago", "senha": "Tiago123", "tipo": "respondente"}
]

# Inserir usuários na tabela se ela estiver vazia
for usuario in usuarios:
    cursor.execute('''
    INSERT OR IGNORE INTO usuarios (nome, senha, tipo) 
    VALUES (?, ?, ?)
    ''', (usuario['nome'], usuario['senha'], usuario['tipo']))
conn.commit()

# Inicializando a sessão do Streamlit
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.tipo_usuario = None

st.sidebar.title("Escolha uma opção:")
opcao = st.sidebar.radio("Ação", ["Login"])

if opcao == "Login":
    if not st.session_state.logged_in:
        st.title("Login")

        nome_usuario = st.text_input('Digite o seu login')
        senha_usuario = st.text_input('Digite a sua senha', type='password')

        if st.button("Entrar"):
            cursor.execute('''
            SELECT * FROM usuarios WHERE nome = ? AND senha = ?
            ''', (nome_usuario, senha_usuario))
            usuario = cursor.fetchone()

            if usuario:
                st.session_state.logged_in = True
                st.session_state.tipo_usuario = usuario[2]
                st.success(f'Bem-vindo, {usuario[1]}!')
            else:
                st.error("Usuário não encontrado!")

    else:
        if st.session_state.tipo_usuario == 'criador':
            st.markdown('## Crie as perguntas do Quiz')
            pergunta = st.text_input('Digite a pergunta')
            respostas = st.text_input('Digite as opções de resposta (separe elas por ponto e vírgula)').split(';')
            gabarito = st.text_input('Resposta correta (precisa que a resposta esteja escrita por extenso)')

            if st.button('Salvar Resposta'):
                if pergunta and respostas and gabarito:
                    cursor.execute('''
                    INSERT INTO perguntas (pergunta, respostas, gabarito) 
                    VALUES (?, ?, ?)
                    ''', (pergunta, ';'.join(respostas), gabarito))
                    conn.commit()
                    st.success('Pergunta foi salva com sucesso!')
                else:
                    st.error('Preencha todos os campos antes de salvar!')

        elif st.session_state.tipo_usuario == 'respondente':
            st.markdown('Responda todas as perguntas abaixo:')

            cursor.execute('SELECT * FROM perguntas')
            perguntas = cursor.fetchall()

            if perguntas:
                for i, pergunta in enumerate(perguntas):
                    st.markdown(f'### Pergunta {i + 1}: {pergunta[1]}')
                    resposta = st.selectbox('Escolha uma opção', pergunta[2].split(';'), key=pergunta[0])

# Fechar a conexão com o banco ao final
conn.close()
