import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_drawable_canvas import st_canvas
import pandas as pd
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ficha Digital Elaine Souza", layout="wide")

# --- ESTILO VISUAL (Fundo branco, campos azuis, letras pretas) ---
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

st.title("🏥 Ficha de Avaliação Podológica Digital")
st.subheader("Profissional Responsável: Elaine Souza")
st.divider()

with st.form("ficha_completa_digital", clear_on_submit=True):
    
    st.markdown("### 📝 1. Identificação")
    nome = st.text_input("Nome Completo do Paciente:")
    
    col_id1, col_id2 = st.columns(2)
    data_nasc = col_id1.date_input("Data de Nascimento:", value=None, format="DD/MM/YYYY", min_value=date(1920, 1, 1))
    telefone = col_id2.text_input("Telefone:")
    
    endereco = st.text_input("Endereço Completo:")
    
    col_loc1, col_loc2, col_loc3 = st.columns(3)
    bairro = col_loc1.text_input("Bairro:")
    cidade = col_loc2.text_input("Cidade:")
    cep = col_loc3.text_input("CEP:")
    
    profissao = st.text_input("Profissão:")

    st.divider()

    st.markdown("### 👟 2. Hábitos e Histórico")
    col_hab1, col_hab2, col_hab3, col_hab4, col_hab5 = st.columns(5)
    t_pe = col_hab1.checkbox("Em pé")
    t_sentado = col_hab2.checkbox("Sentado")
    t_andando = col_hab3.checkbox("Andando")
    t_destro = col_hab4.checkbox("Destro")
    t_canhoto = col_hab5.checkbox("Canhoto")

    esporte = st.text_input("Pratica algum esporte? Qual?")
    calcado = st.text_input("Calçado mais utilizado (nº e tipo):")
    medicamentos = st.text_area("Usa medicamentos? Se sim, quais?")

    st.divider()

    st.markdown("### 🩹 3. Avaliação e Tratamento")
    col_trat1, col_trat2 = st.columns(2)
    data_inicio = col_trat1.date_input("Início do Tratamento:", format="DD/MM/YYYY")
    data_final = col_trat2.date_input("Previsão de Finalização:", format="DD/MM/YYYY")
    
    col_cur1, col_cur2, col_cur3 = st.columns(3)
    cur1 = col_cur1.text_input("Curativo 1")
    cur2 = col_cur2.text_input("Curativo 2")
    cur3 = col_cur3.text_input("Curativo 3")

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

    st.divider()
    # --- ÁREAS DE ASSINATURA DIGITAL ---
    st.markdown("### 🖋️ Assinaturas Digitais (Assine com o dedo ou caneta)")
    
    col_canvas1, col_canvas2 = st.columns(2)
    
    with col_canvas1:
        st.write("Assinatura do Paciente:")
        canvas_paciente = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=2,
            stroke_color="black",
            background_color="white",
            height=150,
            key="canvas_p",
        )
        
    with col_canvas2:
        st.write("Assinatura Elaine Souza:")
        canvas_elaine = st_canvas(
            fill_color="rgba(255, 255, 255, 0)",
            stroke_width=2,
            stroke_color="blue",
            background_color="white",
            height=150,
            key="canvas_e",
        )

    st.divider()

    # BOTÃO SALVAR
    submit = st.form_submit_button("SALVAR FICHA DIGITAL E LIMPAR TELA")

    if submit:
        if nome:
            try:
                # 1. Tenta ler a planilha existente
                try:
                    df_antigo = conn.read(worksheet="Sheet1")
                except:
                    df_antigo = pd.DataFrame()

                # 2. Organiza todos os dados para a planilha
                novos_dados = pd.DataFrame([{
                    "Nome": nome, 
                    "Nascimento": str(data_nasc), 
                    "Telefone": telefone,
                    "Endereco": endereco, 
                    "Bairro": bairro, 
                    "Cidade": cidade,
                    "CEP": cep,
                    "Profissao": profissao, 
                    "Habitos": f"Pé:{t_pe}/Sent:{t_sentado}/And:{t_andando}/Lado:{'D' if t_destro else 'C'}",
                    "Esporte": esporte, 
                    "Calcado": calcado, 
                    "Medicamentos": medicamentos,
                    "Inicio": str(data_inicio), 
                    "Final": str(data_final), 
                    "Curativos": f"{cur1}, {cur2}, {cur3}", 
                    "Patologias": ", ".join(selecionados), 
                    "Observacoes": obs_gerais, 
                    "Status_Assinatura": "Assinado Digitalmente",
                    "Data_Registro": str(date.today())
                }])

                # 3. Junta e envia para o Google Sheets
                df_final = pd.concat([df_antigo, novos_dados], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_final)
                
                st.success(f"✅ Sucesso! A ficha de {nome} foi salva e digitalizada.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("⚠️ O campo Nome é obrigatório para salvar a ficha.")




