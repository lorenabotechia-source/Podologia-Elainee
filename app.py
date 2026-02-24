import streamlit as st

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Ficha Podológica - Elaine Souza", layout="wide")

st.markdown("""
    <style>
    /* Fundo geral branco */
    .stApp { background-color: white; }
    
    /* Nomes dos campos (Labels) em PRETO */
    [data-testid="stWidgetLabel"] p {
        color: black !important;
        font-weight: bold !important;
        font-size: 1.1em !important;
    }

    /* CAIXA DE DIGITAÇÃO: Fundo Azul e Letra BRANCA */
    input, textarea {
        background-color: #1E3A8A !important; /* Azul Escuro */
        color: white !important; /* Letra Branca ao digitar */
        border-radius: 5px !important;
    }

    /* Cor do texto dentro da caixa enquanto digita */
    .stTextInput div div input, .stTextArea div div textarea {
        color: white !important;
    }

    /* Títulos em Azul */
    h1, h2, h3 { color: #1E3A8A !important; }

    /* Botão Verde */
    .stButton>button {
        background-color: #10B981 !important;
        color: white !important;
        font-weight: bold;
        width: 100%;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Ficha de Avaliação Podológica")
st.subheader("Profissional Responsável: Elaine Souza")
st.divider()

with st.form("ficha_podologia_v3"):
    
    st.markdown("### 📝 1. Identificação do Paciente")
    nome = st.text_input("Nome Completo:")
    data_nasc = st.text_input("Data de Nascimento:")
    endereco = st.text_input("Endereço Completo:")
    
    col_inf1, col_inf2 = st.columns(2)
    bairro = col_inf1.text_input("Bairro:")
    cidade = col_inf2.text_input("Cidade:")
    cep = col_inf1.text_input("CEP:")
    telefone = col_inf2.text_input("Telefone:")
    
    profissao = st.text_input("Profissão:")

    st.divider()

    st.markdown("### 👟 2. Hábitos e Estilo de Vida")
    st.write("**Trabalha:**")
    c_tr1, c_tr2, c_tr3, c_tr4, c_tr5 = st.columns(5)
    t_pe = c_tr1.checkbox("Em pé")
    t_sentado = c_tr2.checkbox("Sentado")
    t_andando = c_tr3.checkbox("Andando")
    t_destro = c_tr4.checkbox("Destro")
    t_canhoto = c_tr5.checkbox("Canhoto")

    esporte = st.text_input("Pratica algum esporte? Qual?")
    calcado = st.text_input("Qual o seu calçado preferido?")
    medicamentos = st.text_input("Usa medicamentos? Se sim, quais?")

    st.divider()

    st.markdown("### 🩹 3. Curativos e Avaliação")
    st.write("**Curativos:**")
    cur_cols = st.columns(5)
    cur1 = cur_cols[0].text_input("1º")
    cur2 = cur_cols[1].text_input("2º")
    cur3 = cur_cols[2].text_input("3º")
    cur4 = cur_cols[3].text_input("4º")
    cur5 = cur_cols[4].text_input("5º")

    st.write("")
    granuloma = st.text_input("Granuloma telangiectásico:")
    ortese = st.text_input("Órtese:")
    artelho = st.text_input("Artelho:")
    inicio_t = st.text_input("Início do tratamento:")
    final_t = st.text_input("Final do tratamento:")

    st.divider()

    st.markdown("### 🩺 4. Condições e Patologias")
    st.write("**Assinale as opções que se aplicam:**")
    
    doencas = [
        "Diabetes", "Hipertensão", "Cardíaco", "Anidrose", "Bromidrose", 
        "Pé Cavo", "Pé Plano", "Pé Equino Onicogrifose", "Halux Valgus D-E", 
        "Halux Varo D-E", "Calo Dorsal", "Calo de Milet", "Calo Subungueal", 
        "Calo Periungueal", "Calo Interdigital", "Onicofose", "Calo Duro", 
        "Calo Mole", "Calo Miliar", "Calo Vascular", "Calo Neuro Vascular", 
        "Calosidade", "Onicomicose"
    ]
    
    col_p1, col_p2, col_p3 = st.columns(3)
    for i, pato in enumerate(doencas):
        if i % 3 == 0: col_p1.checkbox(pato)
        elif i % 3 == 1: col_p2.checkbox(pato)
        else: col_p3.checkbox(pato)

    st.divider()
    
    st.markdown("### 🖋️ 5. Assinaturas")
    ass_paciente = st.text_input("Assinatura do Paciente (Nome):")
    st.text_input("Profissional Responsável:", value="Elaine Souza", disabled=True)

    # BOTÃO SALVAR
    botao_salvar = st.form_submit_button("SALVAR FICHA DE AVALIAÇÃO")

    if botao_salvar:
        st.success(f"Ficha de {nome} salva com sucesso!")
