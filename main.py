import streamlit as st
import pandas as pd

# Persoanlizar a pagina (uma vez)
st.set_page_config(
    page_title="Controle de Finanças 2025",
    page_icon="💰")

# Inserir texto na tela
# st.text("Teste de streamlit")

# Inserir texto usando markdown HARDCODE
# st.markdown('''
# # Boas vindas!

# ## Nosso APP financeiro tá funfando

# Espero que você curta nossa aplicação para gestão financeira
            
# ''')

# Inserir texto usando markdown REFERENCIADO

# Aqui criamos um objeto, mas isso poderia ser transformado em uma função declarada
with open("HOME.md", "r" , encoding="utf-8") as file:
    mkdown = file.read()

st.markdown(mkdown)

# A partir desse ponto sempre consultamos a documentação do Streamlit para entender os elementos que queremos adicionar em nossa aplicação

# File updloader - Leitura dos dados
file_upload = st.file_uploader(
    label="Faça o upload dos dados aqui" ,
    type=["csv"]
)

# Verifica se algum arquivo subiu
if file_upload:
    # Leitura dos dados e converter coluna de DATA
    df = pd.read_csv(file_upload, sep=",")
    df['Data'] = pd.to_datetime(df['Data'] , format="%d/%m/%Y").dt.date

    # UPDATE 1 : Podemos descarregar as paginas em EXPANDERS para reduzir a carga de informação na tela e evitar que o usuário
    # precise rolar a pagina eternamente para baixo
    
    exp_DadosBrutos = st.expander(label="01.Dados Brutos")

    # Exibição dos dados, formatados (consultando a documentação do st.dataframe)
    # UPDATE 1 : agora em vez de referenciar st.dataframe trocamos a referencia para o conteiner onde ele será exibido
    exp_DadosBrutos.dataframe(data=df, 
                             # Ocultar a coluna de INDEX
                             hide_index=True, 
                             # Configurar as colunas em DICIONARIOS com Chave = Nome do Campo e Valor = método COLUMNCONFIG
                             # IMPORTANTE : O dicionario pode ser declarado em separado e invocado no método
                             column_config={
                                "Valor":st.column_config.NumberColumn(label="Valor em R$",
                                                                    help="Valor do Saldo no dia",
                                                                    format="%.2f")
                             })

    # RESUMO POR INSTITUIÇÃO,
    # UPDATE 2 : Para evitar a rolagem dentro do EXPANDER podemos criar ABAS/TABS para exibir os dados
    exp_DadosPorInstituicao = st.expander(label="02.Resumo por Instituição")
        
    tab_dados , tab_historico , tab_distrib = exp_DadosPorInstituicao.tabs(["Dados", "Histórico" , "Saldo"])
    
    df_instituicao = pd.pivot_table(data=df,
                                    index="Data",
                                    columns="Instituição",
                                    values="Valor" ,
                                    aggfunc="sum")
    
    # Configurando os formatos das colunas
    columns_format = {
        "Data" : st.column_config.DateColumn("Data", format="localized") ,
        "Valor" : st.column_config.NumberColumn("Valor em R$" , format="DD.MM.YYYY")
    }
    
    # Exibindo o DataFrame com as colunas formatadas, e agora com índice criado no PIVOT_TABLE
    # UPDATE 1 : dentro do expander
    # UPDATE 2 : dentro do TAB em um laço WITH para facilitar a compreensão
    
    # Aba com os dados do Pivot   
    tab_dados.dataframe(data = df_instituicao , column_config=columns_format)
    
    # Aba com o gráfico de histórico
    tab_historico.subheader("A. Saldo Histórico", divider="gray")
    tab_historico.line_chart(data=df_instituicao)

    with tab_distrib:   # Aba com o gráfico de saldo atual usando WITH
        
        # UPDATE 3 : Inserir botão para o usuario selecionar o dia que quer ver o saldo
        # flt_data= st.date_input(label="Selecione uma data para ver o saldo" , 
        #                         min_value=df_instituicao.index.min() ,
        #                         max_value=df_instituicao.index.max())
        
        # if flt_data not in df_instituicao.index:
        #     st.warning(body="Escolha uma data válida!")
        # else:
        #     df_ultimosaldo = df_instituicao.sort_index().loc[flt_data]
        #     # Escrevemos apenas ST para não encaixar em nenhum outro conteiner
        #     st.bar_chart(df_ultimosaldo)

        # UPDATE 4 : Um seletor de datas tem muitas datas não válidas, ja que temos apenas dados
        # para cada dia 5 de cada mês, então vamos mudar o método de input para mostrar apenas
        # as datas válidas (pode ser feito tambem usando SELECT BOX)

        lst_datas = df_instituicao.index.to_list()
        flt_data = st.pills(label="Selecione a data para ver o saldo", 
                            options=lst_datas,
                            format_func=lambda x : x.strftime("%b-%y"))
        df_ultimosaldo = df_instituicao.sort_index().loc[flt_data]
        st.bar_chart(df_ultimosaldo)



