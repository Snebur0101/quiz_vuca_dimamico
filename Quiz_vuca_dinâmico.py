import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

url = 'https://raw.githubusercontent.com/Snebur0101/quiz_vuca_dimamico/refs/heads/main/credenciais_quiz.json'

response = requests.get(url)

with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    tmp_file.write(response.content)
    tmp_file_path = tmp_file.name

if not firebase_admin._apps:
    cred = credentials.Certificate(tmp_file_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

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

            for usuario in usuarios:
                if usuario['nome'] == nome_usuario and usuario['senha'] == senha_usuario:
                    st.session_state.logged_in = True
                    st.session_state.tipo_usuario = usuario['tipo']
                    st.success(f'Bem-vindo,{usuario['nome']}!')
                    break
                else:
                    st.error("Usuário não encontrado!")

                tipo_usuario = usuario['tipo']
    else:
        if st.session_state.tipo_usuario == 'criador':
            st.markdown('## Crie as perguntas do Quiz')
            pergunta = st.text_input('Digite a pergunta')
            respostas = st.text_input('Digite as opções de resposta (separe elas por ponto e vírgula)').split(';')
            gabarito = st.text_input('Resposta correta (precisa que a resposta esteja escrita por extenso)')

            if st.button('Salvar Resposta'):
                if pergunta and respostas and gabarito:
                    data = {
                        'pergunta': pergunta,
                        'respostas': respostas,
                        'gabarito': gabarito
                    }
                    try:
                        db.collection('perguntas').add(data)
                        st.success('Pergunta foi salva com sucesso!')
                    except Exception as e:
                        st.error(f'Ocorreu um erro ao salvar a pergunta: {e}')
                else:
                    st.error('Preencha todos os campos antes de salvar!')

        elif st.session_state.tipo_usuario == 'respondente':
            st.markdown('Responda todas as perguntas abaixo:')

            pergunta_ref = db.collection('perguntas').stream()
            perguntas = [{'id': p.id, **p.to_dict()} for p in pergunta_ref]

            if perguntas:
                for i, pergunta in enumerate(perguntas):
                    st.markdown(f'### Pergunta {i + 1}: {pergunta["pergunta"]}')
                    resposta = st.selectbox('Escolha uma opção', pergunta['respostas'], key=pergunta['id'])
