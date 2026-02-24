import streamlit as st
import sqlite3

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Ficha Podológica - Elaine Souza", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Arial'; }
    label { font-weight: bold; color: #1E3A8A; font-size: 1.1em; }
    .stButton>button { background-color: #10B981; color: white; font-weight: bold; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('podologia.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pacientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.title("🏥 Ficha de Avaliação Podológica")
st.subheader("Profissional Responsável: Elaine Souza")
st.divider()

with st.form("ficha_detalhada"):
    # IDENTIFICAÇÃO
    st.markdown("### 📝 Dados de Identificação")
    nome = st.text_input("Nome completo do paciente:")
    data_nasc = st.text_input("Data de nascimento (caixa de texto):")
    endereco = st.text_input("Endereço completo (caixa de texto):")
    
    col_inf1, col_inf2 = st.columns(2)
    bairro = col_inf1.text_input("Bairro (caixa de texto):")
    cidade = col_inf2.text_input("Cidade (caixa de texto):")
    cep = col_inf1.text_input("CEP (caixa de texto):")
    telefone = col_inf2.text_input("Telefone (caixa de texto):")
    
    profissao = st.text_input("Profissão (caixa de texto):")

    st.divider()

    # HÁBITOS
    st.markdown("### 👟 Hábitos e Estilo de Vida")
    st.write("Trabalha: (assinale as opções)")
    col_tr1, col_tr2, col_tr3, col_tr4, col_tr5 = st.columns(5)
    t_pe = col_tr1.checkbox("Em pé")
    t_sentado = col_tr2.checkbox("Sentado")
    t_andando = col_tr3.checkbox("Andando")
    t_destro = col_tr4.checkbox("Destro")
    t_canhoto = col_tr5.checkbox("Canhoto")

    st.write("Pratica algum esporte?")
    col_esp1, col_esp2 = st.columns(2)
    esp_sim = col_esp1.checkbox("Sim (Esporte)")
    esp_nao = col_esp2.checkbox("Não (Esporte)")

    calcado = st.text_input("Calçado preferido?")
    
    st.write("Cirurgias anteriores no pé?")
    col_cir1, col_cir2 = st.columns(2)
    cir_sim = col_cir1.checkbox("Sim (Cirurgia)")
    cir_nao = col_cir2.checkbox("Não (Cirurgia)")

    medicamentos = st.text_input("Usa medicamentos? Se sim, qual? (caixa de texto):")

    st.divider()

    # CURATIVOS
    st.markdown("### 🩹 Curativos")
    col_cur1, col_cur2, col_cur3, col_cur4, col_cur5 = st.columns(5)
    cur1 = col_cur1.text_input("Curativo: 1º")
    cur2 = col_col2.text_input("Curativo: 2º") if 'col_col2' not in locals() else col_cur2.text_input("Curativo: 2º")
    cur3 = col_cur3.text_input("Curativo: 3º")
    cur4 = col_cur4.text_input("Curativo: 4º")
    cur5 = col_cur5.text_input("Curativo: 5º")

    st.divider()

    # AVALIAÇÃO TÉCNICA
    st.markdown("### 🔬 Avaliação Técnica")
    granuloma = st.text_input("Granuloma telangiectásico:")
    ortese = st.text_input("Órtese:")
    artelho = st.text_input("Artelho:")
    inicio_t = st.text_input("Início:")
    final_t = st.text_input("Final:")

    st.divider()

    # OPÇÕES DE SAÚDE E PATOLOGIAS
    st.markdown("### 🩺 Condições e Patologias (Assinale as opções)")
    lista_doencas = [
        "Diabetes", "Hipertensão", "Cardíaco", "Anidrose", "Bromidrose", 
        "Pé Cavo", "Pé Plano", "Pé Equino Onicogrifose", "Halux Valgus D-E", 
        "Halux Varo D-E", "Calo Dorsal", "Calo de Milet", "Calo Subungueal", 
        "Calo Periungueal", "Calo Interdigital", "Onicofose", "Calo Duro", 
        "Calo Mole", "Calo Miliar", "Calo Vascular", "Calo Neuro Vascular", 
        "Calosidade", "Onicomicose"
    ]
    
    col_pat1, col_pat2, col_pat3 = st.columns(3)
    for i, pat in enumerate(lista_doencas):
        if i % 3 == 0: col_pat1.checkbox(pat)
        elif i % 3 == 1: col_pat2.checkbox(pat)
        else: col_pat3.checkbox(pat)

    st.divider()
    st.text_input("Nome da Profissional:", value="Elaine Souza", disabled=True)
    
    if st.form_submit_button("SALVAR DADOS DA FICHA"):
        st.success(f"Ficha de {nome} salva com sucesso!")