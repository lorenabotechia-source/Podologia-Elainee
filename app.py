import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ficha Podológica - Elaine Souza", layout="wide")

# --- ESTILO VISUAL (Fundo branco, letras pretas e campos azuis) ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stWidgetLabel"] p { color: black !important; font-weight: bold !important; font-size: 1.1em !important; }
    input, textarea { background-color: #1E3A8A !important; color: white !important; border-radius: 5px !important; }
    .stTextInput div div input, .stTextArea div div textarea, .stDateInput div div input { color: white !important; }
    h1, h2, h3 { color: #1E3A8A !important; }
    .stButton>button { background-color: #10B981 !important; color: white !important; font-weight: bold; width: 100%; height: 3.5em; border-radius: 8px; }
    .stCheckbox label { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM A PLANILHA ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Ficha de Avaliação Podológica")
st.subheader("Profissional Responsável: Elaine Souza")
st.divider()

# Formulário Completo
with st.form("ficha_podologia", clear_on_submit=True):
    
    st.markdown("### 📝 1. Identificação")
    nome = st.text_input("Nome Completo do Paciente:")
    
    col_ident1, col_ident2 = st.columns(2)
    data_nasc = col_ident1.date_input("Data de Nascimento:", value=None, format="DD/MM/YYYY", min_value=date(1920, 1, 1))
    telefone = col_ident2.text_input("Telefone:")
    
    endereco = st.text_input("Endereço Completo:")
    
    col_loc1, col_loc2 = st.columns(2)
    bairro = col_loc1.text_input("Bairro:")
    cidade = col_loc2.text_input("Cidade:")
    
    profissao = st.text_input("Profissão:")

    st.divider()

    st.markdown("### 👟 2. Hábitos e Histórico")
    col_hab1, col_hab2, col_hab3 = st.columns(3)
    t_pe = col_hab1.checkbox("Trabalha em pé")
    t_sentado = col_hab2.checkbox("Trabalha sentado")
    t_andando = col_hab3.checkbox("Trabalha andando")
    
    col_hab4, col_hab5 = st.columns(2)
    t_destro = col_hab4.checkbox("Destro")
    t_canhoto = col_hab5.checkbox("Canhoto")

    esporte = st.text_input("Pratica esporte? Qual?")
    calcado = st.text_input("Tipo de calçado mais utilizado:")
    medicamentos = st.text_area("Usa medicamentos? (Quais?)")

    st.divider()

    st.markdown("### 🩹 3. Tratamento")
    col_trat1, col_trat2 = st.columns(2)
    data_inicio = col_trat1.date_input("Início do Tratamento:", format="DD/MM/YYYY")
    data_final = col_trat2.date_input("Previsão de Finalização:", format="DD/MM/YYYY")
    
    curativos = st.text_input("Curativos Utilizados:")

    st.divider()

    st.markdown("### 🩺 4. Condições e Patologias")
    lista_doencas = [
        "Diabetes", "Hipertensão", "Cardíaco", "Anidrose", "Bromidrose", 
        "Pé Cavo", "Pé Plano", "Pé Equino", "Onicogrifose", "Halux Valgus D-E", 
        "Halux Varo D-E", "Calo Dorsal", "Calo de Milet", "Calo Subungueal", 
        "Calo Periungueal", "Calo Interdigital", "Onicofose", "Calo Duro", 
        "Calo Mole", "Calo Miliar", "Calo Vascular", "Calo Neuro Vascular", 
        "Calosidade", "Onicomicose"
    ]
    
    col_p1, col_p2, col_p3 = st.columns(3)
    selecionados = []
    for i, pato in enumerate(lista_doencas):
        if i % 3 == 0: 
            if col_p1.checkbox(pato): selecionados.append(pato)
        elif i % 3 == 1: 
            if col_p2.checkbox(pato): selecionados.append(pato)
        else: 
            if col_p3.checkbox(pato): selecionados.append(pato)

    st.divider()
    obs_gerais = st.text_area("Observações Técnicas Gerais:")

    # BOTÃO SALVAR
    submit = st.form_submit_button("SALVAR FICHA NA PLANILHA")

    if submit:
        if nome:
            try:
                # 1. Tenta ler a planilha Sheet1 para não apagar o que já existe
                try:
                    df_antigo = conn.read(worksheet="Sheet1")
                except:
                    df_antigo = pd.DataFrame()

                # 2. Cria a nova linha com tudo
                novo_paciente = pd.DataFrame([{
                    "Nome": nome, "Nascimento": str(data_nasc), "Telefone": telefone,
                    "Endereco": endereco, "Bairro": bairro, "Cidade": cidade,
                    "Profissao": profissao, "Trabalho": f"{t_pe}/{t_sentado}/{t_andando}",
                    "Esporte": esporte, "Calcado": calcado, "Medicamentos": medicamentos,
                    "Inicio": str(data_inicio), "Final": str(data_final), 
                    "Curativos": curativos, "Patologias": ", ".join(selecionados), 
                    "Observacoes": obs_gerais, "Data_Registro": str(date.today())
                }])

                # 3. Junta o antigo com o novo
                df_final = pd.concat([df_antigo, novo_paciente], ignore_index=True)

                # 4. Envia de volta para o Google
                conn.update(worksheet="Sheet1", data=df_final)
                
                st.success(f"✅ Ficha de {nome} salva com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("⚠️ Por favor, digite ao menos o nome do paciente.")



