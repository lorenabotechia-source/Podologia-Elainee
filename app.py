import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Ficha Podológica - Elaine Souza", layout="wide")

# --- ESTILO VISUAL (Cores, Letras Pretas fora e Brancas dentro) ---
st.markdown("""
    <style>
    .stApp { background-color: white; }
    
    /* Letras dos nomes dos campos em PRETO */
    [data-testid="stWidgetLabel"] p { 
        color: black !important; 
        font-weight: bold !important; 
        font-size: 1.1em !important; 
    }
    
    /* Caixas de digitação: Fundo AZUL e Letra BRANCA */
    input, textarea { 
        background-color: #1E3A8A !important; 
        color: white !important; 
        border-radius: 5px !important; 
    }
    
    /* Forçar letra branca ao digitar */
    .stTextInput div div input, .stTextArea div div textarea, .stDateInput div div input { 
        color: white !important; 
    }
    
    /* Títulos em Azul */
    h1, h2, h3 { color: #1E3A8A !important; }
    
    /* Botão SALVAR em Verde */
    .stButton>button { 
        background-color: #10B981 !important; 
        color: white !important; 
        font-weight: bold; 
        width: 100%; 
        height: 3.5em; 
        border-radius: 8px;
    }
    
    /* Letras das caixinhas de marcar (Checkboxes) em preto */
    .stCheckbox label { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM O GOOGLE DRIVE ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🏥 Ficha de Avaliação Podológica")
st.subheader("Profissional Responsável: Elaine Souza")
st.divider()

# Menu lateral para navegação
menu = ["Cadastrar Paciente", "Consultar Histórico"]
escolha = st.sidebar.selectbox("Selecione uma opção:", menu)

if escolha == "Cadastrar Paciente":
    # clear_on_submit=True limpa a tela após salvar
    with st.form("ficha_completa", clear_on_submit=True):
        
        st.markdown("### 📝 1. Identificação")
        nome = st.text_input("Nome Completo do Paciente:")
        # CALENDÁRIO para Data de Nascimento
        data_nasc = st.date_input("Data de Nascimento:", value=None, format="DD/MM/YYYY", min_value=date(1920, 1, 1))
        
        col_end1, col_end2 = st.columns(2)
        endereco = col_end1.text_input("Endereço Completo:")
        bairro = col_end2.text_input("Bairro:")
        
        col_cid1, col_cid2, col_cid3 = st.columns(3)
        cidade = col_cid1.text_input("Cidade:")
        cep = col_cid2.text_input("CEP:")
        telefone = col_cid3.text_input("Telefone:")
        
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
        calcado = st.text_input("Calçado mais utilizado:")
        medicamentos = st.text_area("Usa medicamentos? Se sim, quais?")

        st.divider()

        st.markdown("### 🩹 3. Avaliação e Tratamento")
        col_data1, col_data2 = st.columns(2)
        # CALENDÁRIOS para o tratamento
        data_inicio = col_data1.date_input("Início do Tratamento:", format="DD/MM/YYYY")
        data_final = col_data2.date_input("Previsão de Finalização:", format="DD/MM/YYYY")
        
        col_cur1, col_cur2, col_cur3 = st.columns(3)
        cur1 = col_cur1.text_input("Curativo 1")
        cur2 = col_cur2.text_input("Curativo 2")
        cur3 = col_cur3.text_input("Curativo 3")

        st.divider()

        st.markdown("### 🩺 4. Condições e Patologias")
        st.write("Assinale as opções que o paciente apresenta:")
        
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
        
        st.markdown("### 🖋️ 5. Observações e Assinatura")
        obs_gerais = st.text_area("Observações Técnicas Gerais:")
        ass_paciente = st.text_input("Nome para Assinatura do Paciente:")
        st.text_input("Profissional Responsável:", value="Elaine Souza", disabled=True)

        # BOTÃO SALVAR
        if st.form_submit_button("SALVAR FICHA E LIMPAR TELA"):
            if nome:
                try:
                    # Lê os dados que já existem na planilha
                    dados_existentes = conn.read()
                    
                    # Cria a nova linha para salvar
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
                        "Curativos": f"{cur1}, {cur2}, {cur3}",
                        "Patologias": ", ".join(selecionados),
                        "Observacoes": obs_gerais,
                        "Data_Registro": str(date.today())
                    }])
                    
                    # Adiciona e atualiza no Google Drive
                    df_final = pd.concat([dados_existentes, novos_dados], ignore_index=True)
                    conn.update(data=df_final)
                    
                    st.success(f"✅ Sucesso! A ficha de {nome} foi salva no Google Drive e a tela foi limpa.")
                except Exception as e:
                    st.error("Erro ao conectar com a planilha. Verifique se ela está configurada como 'Editor' nas Secrets.")
            else:
                st.error("⚠️ O campo NOME é obrigatório!")

elif escolha == "Consultar Histórico":
    st.markdown("### 🔍 Consulta de Pacientes")
    try:
        df = conn.read()
        st.dataframe(df)
    except:
        st.error("Ainda não existem dados para exibir.")


