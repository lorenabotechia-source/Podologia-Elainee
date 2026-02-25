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

# --- CREDENCIAIS DE ACESSO DIRETO (Evita erro de TOML) ---
conf = {
    "spreadsheet": "https://docs.google.com/spreadsheets/d/1s9dynrXK6N51AA5dI5THubj6aOme8PwLajdGh8os850/edit",
    "type": "service_account",
    "project_id": "podologia-elaine",
    "private_key_id": "cf7ca86dc0b09ca93106e8f6ae61d93b4580f734",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCdI2RErH1q1kxT\ni+XKjUoO3x0Xh8NC3r2YptQ8OhJpwJsgtm/Ee8KDbeweFw7B+C5jjeJplUJSNzgq\nFEBbSNqsR7tuMnmLIStslMoD6mie1M89CNpR/7+VHzKAxzEtxyCRkJb/WSqgdeuN\nd7c8KsV9SI7lwBBN/5rbiXw2Nkko7tAaEJjMg/bkA9e4D4+L0qgfMB/0givDhvLU\nYsH5oW4gYj+iUp753Chq6+WXFByHWZY2tlh267c6dIxIpM9bYaDamnbJaxyW/L3x\n/IVLFXQm7R+CsHGnVJVxzu3zBxLndy4hy37MfMuia3d7vjYr/ydMjIeR9QBTRFlc\nFFpx/YIdAgMBAAECggEABtMIDyXalu6fOl89NJKPejcQWvqnbUEIXn41G2rkn9K6\nKfqIvuTAQ6SQRS8R+GfGql/GfhItL8evWPLjAW1+XOfXz2cokvVDnuyU6J45uvDz\nd+tP5/dbPHOyMsuNap29eVtPlqyQ4FuFEyWO2XF8fP6b57hzcAYllVrSmfW5/NzV\nnv2Joyhzuf/KAFHidXiBqA2qfjEQ9Ct0IokaC/eD7FAEQEtRQUhl0kvlUdTlOfjB\nc/8q0URDI41cby9dYNtDtfqFLcqMoNKqa6vKA7T64tsnisP9I7i0JbGlJmMaXIJd\n41EZKSe189Vytkkmiw82CauI8yBlyAUVIYqSY0hg4QKBgQDPThRPPVL16U0wYoCt\n3SP2WWflURoVkOGml8C8OVE974GsYcIWE3AZZAqZN4hOy4vuU4+/YLmsVCVU74VN\nzkj0yrlRp+DYI/l2A/slswoBB/pm5IqOMkR8KeCtwJ4qwByJcNWRKIEEeGHULQOI\nsnGNaauXx+tDP2GjKBPhWn/jSQKBgQDCDJ+R8CS+62UAg2wOli9Egvp1eYzTL5ra\n1feLFCmzr/AxXVmC5EtveZEVmoMp67D/TLUx2GoYcakSa/m7kD2WmO8gUWWj5p53\nn7wbxGNKQ83BD87d44dgf84L9EoUGXkd5JcMQLt52ljGpMhPhJWdjHZi/A1KajVk\o6rsl/PUNQKBgQCQNyk51teX662fM2eBjI4wGxKEHV+gESJp2rhiOR2jkLMNURTM\ndslNYKNe45sX9dJrAgbGhGumzwMJi3eZISDv6vfxLnDk7GHnD+3v1BXpkbtJSUR6\nl8288wUy2wUtiGhR1QU97oeSrIyiJo6G0lzcm96bwKCSL82ky4TJCURewQKBgQCH\n1/xxVtLykKmhZV9lCsBGTwb07EWopf/bSMTFqTTUZMtaU4ZROm6QuGLX49YEp8m9\nv75tCZqkSBVbHxmxs3VaEu/8CN+FkPHIvpsaOS5lE/hbOizQavMfm/jrp3WggoCm\na5tOaZaU5EUXss3D1QZER8us2dSYDqgYLvd+L5XzLQKBgB7aGY65p3++/74/c19G\noDjT4OPSCne+d6VSn4EXme7v3udi6AB7r61cmf4yULniIxzg8cc6evdZTiJFZ3un\nRojnLcH1bL9wc7gz5rXi6qzutPYpwUUXoVDi6iNPmcZ1P1TsNDysV7LsDPED8A6Y\ka56NICABd5H2DbMqO6M8QRw\n-----END PRIVATE KEY-----\n",
    "client_email": "banco-de-dados-podologia-558@podologia-elaine.iam.gserviceaccount.com",
    "client_id": "108127276573949778048",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/banco-de-dados-podologia-558%40podologia-elaine.iam.gserviceaccount.com"
}

conn = st.connection("gsheets", type=GSheetsConnection, **conf)

st.title("🏥 Ficha de Avaliação Podológica Digital")
st.subheader("Profissional Responsável: Elaine Souza")
st.divider()

# --- FORMULÁRIO COMPLETO ---
with st.form("ficha_digital_completa", clear_on_submit=True):
    
    st.markdown("### 📝 1. Identificação")
    nome = st.text_input("Nome Completo do Paciente:")
    
    col_id1, col_id2 = st.columns(2)
    data_nasc = col_id1.date_input("Data de Nascimento (Calendário):", value=None, format="DD/MM/YYYY", min_value=date(1920, 1, 1))
    telefone = col_id2.text_input("Telefone:")
    
    endereco = st.text_input("Endereço Completo:")
    col_l1, col_l2, col_l3 = st.columns(3)
    bairro = col_l1.text_input("Bairro:")
    cidade = col_l2.text_input("Cidade:")
    cep = col_l3.text_input("CEP:")
    
    profissao = st.text_input("Profissão:")

    st.divider()
    st.markdown("### 👟 2. Hábitos e Histórico")
    col_hab1, col_hab2, col_hab3, col_hab4, col_hab5 = st.columns(5)
    t_pe = col_hab1.checkbox("Em pé")
    t_sentado = col_hab2.checkbox("Sentado")
    t_andando = col_hab3.checkbox("Andando")
    t_destro = col_hab4.checkbox("Destro")
    t_canhoto = col_hab5.checkbox("Canhoto")

    esporte = st.text_input("Pratica esporte? Qual?")
    calcado = st.text_input("Calçado (nº e tipo):")
    medicamentos = st.text_area("Usa medicamentos? (Quais?)")

    st.divider()
    st.markdown("### 🩹 3. Avaliação e Tratamento")
    col_t1, col_t2 = st.columns(2)
    dt_inicio = col_t1.date_input("Início do Tratamento:", format="DD/MM/YYYY")
    dt_final = col_t2.date_input("Previsão de Alta:", format="DD/MM/YYYY")
    
    col_c1, col_c2, col_c3 = st.columns(3)
    cur1 = col_c1.text_input("Curativo 1")
    cur2 = col_c2.text_input("Curativo 2")
    cur3 = col_c3.text_input("Curativo 3")

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
    for i, d in enumerate(lista_doencas):
        if i % 3 == 0: 
            if col_p1.checkbox(d): selecionados.append(d)
        elif i % 3 == 1: 
            if col_p2.checkbox(d): selecionados.append(d)
        else: 
            if col_p3.checkbox(d): selecionados.append(d)

    st.divider()
    obs = st.text_area("Observações Técnicas Gerais:")

    st.markdown("### 🖋️ Assinaturas Digitais (Assine com o dedo)")
    col_ass1, col_ass2 = st.columns(2)
    with col_ass1:
        st.write("Assinatura do Paciente:")
        st_canvas(fill_color="white", stroke_width=2, stroke_color="black", background_color="white", height=120, key="can_p")
    with col_ass2:
        st.write("Assinatura Elaine Souza:")
        st_canvas(fill_color="white", stroke_width=2, stroke_color="blue", background_color="white", height=120, key="can_e")

    if st.form_submit_button("SALVAR FICHA DIGITAL"):
        if nome:
            try:
                nova_linha = pd.DataFrame([{
                    "Nome": nome, "Nascimento": str(data_nasc), "Telefone": telefone, "CEP": cep,
                    "Curativos": f"{cur1}, {cur2}, {cur3}", "Patologias": ", ".join(selecionados),
                    "Obs": obs, "Data": str(date.today()), "Assinatura": "Digital"
                }])
                df_antigo = conn.read(worksheet="Sheet1")
                df_final = pd.concat([df_antigo, nova_linha], ignore_index=True)
                conn.update(worksheet="Sheet1", data=df_final)
                st.success(f"✅ Ficha de {nome} salva!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.warning("Nome obrigatório!")



