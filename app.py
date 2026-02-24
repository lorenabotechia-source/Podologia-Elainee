import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Ficha Podológica - Elaine Souza", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: white; }
    [data-testid="stWidgetLabel"] p { color: black !important; font-weight: bold !important; font-size: 1.1em !important; }
    input, textarea { background-color: #1E3A8A !important; color: white !important; border-radius: 5px !important; }
    .stTextInput div div input, .stTextArea div div textarea, .stDateInput div div input { color: white !important; }
    h1, h2, h3 { color: #1E3A8A !important; font-family: 'Arial'; }
    .stButton>button { background-color: #10B981 !important; color: white !important; font-weight: bold; width: 100%; height: 3.5em; border-radius: 10px; border: none; }
    /* Estilo para as caixas de seleção (checkboxes) */
    .stCheckbox label { color: black !important; font-weight: normal !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM O BANCO DE DADOS (GOOGLE SHEETS) ---
# O Streamlit usará as 'Secrets' para se conectar à planilha da sua sogra
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro na conexão com o Google Sheets. Verifique as configurações de Secrets.")

# --- INTERFACE ---
st.title("🏥 Sistema de Avaliação Podológica")
st.subheader("Profissional: Elaine Souza")
st.divider()

menu = ["Cadastrar Novo Paciente", "Consultar Histórico"]
escolha = st.sidebar.selectbox("O que deseja fazer?", menu)

if escolha == "Cadastrar Novo Paciente":
    # clear_on_submit=True limpa tudo automaticamente após salvar
    with st.form("ficha_podologia", clear_on_submit=True):
        
        st.markdown("### 📝 1. Identificação Pessoal")
        nome = st.text_input("Nome Completo do Paciente:")
        
        col_nasc, col_tel = st.columns(2)
        # CALENDÁRIO para nascimento
        data_nasc = col_nasc.date_input("Data de Nascimento:", value=None, format="DD/MM/YYYY", min_value=date(1920, 1, 1))
        telefone = col_tel.text_input("Telefone de Contato:")
        
        endereco = st.text_input("Endereço Residencial:")
        
        c1, c2, c3 = st.columns(3)
        bairro = c1.text_input("Bairro:")
        cidade = c2.text_input("Cidade:")
        profissao = c3.text_input("Profissão:")

        st.divider()

        st.markdown("### 🩹 2. Informações do Tratamento")
        col_data1, col_data2 = st.columns(2)
        # CALENDÁRIOS para o tratamento
        data_inicio = col_data1.date_input("Início do Tratamento:", format="DD/MM/YYYY")
        data_final = col_data2.date_input("Final do Tratamento (Previsão):", format="DD/MM/YYYY")
        
        curativos = st.text_input("Curativos Realizados:")
        calcado = st.text_input("Calçado Preferido/Mais utilizado:")
        medicamentos = st.text_area("Usa medicamentos? Se sim, quais?")

        st.divider()

        st.markdown("### 🩺 3. Avaliação Clínica (Patologias)")
        st.write("Assinale as opções que se aplicam ao paciente:")
        
        lista_doencas = [
            "Diabetes", "Hipertensão", "Cardíaco", "Anidrose", "Bromidrose", 
            "Pé Cavo", "Pé Plano", "Pé Equino Onicogrifose", "Halux Valgus D-E", 
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
        
        st.markdown("### 🖋️ 4. Finalização")
        obs_gerais = st.text_area("Observações Técnicas Gerais:")
        ass_paciente = st.text_input("Assinatura do Paciente (Nome):")
        st.text_input("Profissional Responsável:", value="Elaine Souza", disabled=True)

        # BOTÃO SALVAR
        botao_salvar = st.form_submit_button("SALVAR FICHA E LIMPAR TELA")

        if botao_salvar:
            if nome:
                # Preparar os dados para a planilha
                novos_dados = pd.DataFrame([{
                    "Nome": nome,
                    "Nascimento": str(data_nasc),
                    "Telefone": telefone,
                    "Endereco": endereco,
                    "Bairro": bairro,
                    "Cidade": cidade,
                    "Profissao": profissao,
                    "Inicio_Tratamento": str(data_inicio),
                    "Final_Tratamento": str(data_final),
                    "Curativos": curativos,
                    "Patologias": ", ".join(selecionados),
                    "Observacoes": obs_gerais,
                    "Assinatura_Paciente": ass_paciente,
                    "Data_Registro": str(date.today())
                }])

                # Tenta enviar para a Planilha Google
                try:
                    dados_existentes = conn.read(worksheet="Sheet1")
                    dados_atualizados = pd.concat([dados_existentes, novos_dados], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=dados_atualizados)
                    st.success(f"✅ Ficha de {nome} salva com segurança no Google Drive! Tela pronta para o próximo.")
                except:
                    # Se a planilha não estiver configurada, mostra sucesso local para teste
                    st.warning("Ficha processada. Configure o link da Planilha Google nas Secrets para salvar permanentemente.")
            else:
                st.error("⚠️ O campo NOME é obrigatório para salvar a ficha.")

elif escolha == "Consultar Histórico":
    st.markdown("### 🔍 Consulta de Pacientes Cadastrados")
    try:
        df = conn.read(worksheet="Sheet1")
        # Campo de busca
        busca = st.text_input("Pesquisar paciente pelo nome:")
        if busca:
            df = df[df['Nome'].str.contains(busca, case=False)]
        st.dataframe(df)
    except:
        st.error("Não foi possível carregar os dados. Verifique a conexão com a Planilha Google.")

