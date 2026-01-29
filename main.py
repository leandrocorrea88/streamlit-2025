import streamlit as st
import pandas as pd

# Funções do Projeto

def calc_general_stats(data:pd.DataFrame):
    '''Calcular as estatisticas de Patrimonio'''
    
    # Garantir a ordem das datas
    data.sort_index()

    # Criar um LAG de Patrimonio ...
    data['lag_1'] = data['Patrimonio'].shift(1)

    # (A) ... para pegar o valor do periodo anterior e calcular a diferença ABSOLUTA ...
    data['Cresc. Patrimonio R$ Mes'] = data['Patrimonio'] - data['lag_1']

    # (B) ... ou RELATIVA
    data['Cresc. Patrimonio % Mes'] = (data['Patrimonio'] / data['lag_1']) - 1

    # (C) Calcular a Media movel considerando os ultimos X meses
    data['Cresc. R$ MM.06'] = data['Cresc. Patrimonio R$ Mes'].rolling(6).mean()
    data['Cresc. R$ MM.12'] = data['Cresc. Patrimonio R$ Mes'].rolling(12).mean()
    data['Cresc. R$ MM.24'] = data['Cresc. Patrimonio R$ Mes'].rolling(24).mean()

    # (D) Calcular evolução ABSOLUTA do patrimonio em janelas móveis 
    # ex.: Mes 6 - Mes 1 , Mes 7 - Mes 2, ...
    data['Evolução R$ MM.06'] = data['Patrimonio'].rolling(6).apply( lambda x : x[-1] - x[0])
    data['Evolução R$ MM.12'] = data['Patrimonio'].rolling(12).apply( lambda x : x[-1] - x[0])
    data['Evolução R$ MM.24'] = data['Patrimonio'].rolling(24).apply( lambda x : x[-1] - x[0])

    # (E) Calcular evolução RELATIVA do patrimonio em janelas móveis 
    # ex.: Mes 6 - Mes 1 , Mes 7 - Mes 2, ...
    data['Evolução % MM.06'] = data['Patrimonio'].rolling(6).apply( lambda x : (x[-1] / x[0])-1)
    data['Evolução % MM.12'] = data['Patrimonio'].rolling(12).apply( lambda x : (x[-1] / x[0])-1)
    data['Evolução % MM.24'] = data['Patrimonio'].rolling(24).apply( lambda x : (x[-1] / x[0])-1)

    # (F) Calcular ganho medio diário, aplicando a diferença de dias contra o mes anterior para um
    # mes de 22 dias. Para fazer o SHIFT de INDEX não podemos fazer direto, então precisamos primeiro
    # gerar uma SERIES baseada nele para então fazer o SHIFT
    data['lag_2'] = pd.to_datetime(data.index.to_series().shift(1)).dt.date
    data['Ganho Medio Diario R$'] = data['Cresc. Patrimonio R$ Mes'] / ( ( 22 / 30 ) * (
        pd.to_datetime(data.index) - pd.to_datetime(data['lag_2'])).dt.days  )

    # (G) Calcular as diferenças acumuladas (absoluta e relativa) com relação ao patrimonio inicial
    patrimonio_inicial = data['Patrimonio'].iloc[0]
    data['Diferença acumulada TT R$'] = data['Patrimonio'] - patrimonio_inicial
    data['Diferença acumulada TT %'] = (data['Patrimonio'] / patrimonio_inicial) - 1

    data = data.drop(columns=['lag_1' , 'lag_2'] , axis=1)

    return data

# Persoanlizar a pagina (uma vez)
st.set_page_config(
    page_title="Controle de Finanças 2025",
    page_icon="💰")

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

    # EXPANDER 1 - DADOS BRUTOS (Aba 1 da Planilha)
    
    exp_DadosBrutos = st.expander(label="01.Dados Brutos")

    # Exibição dos dados, formatados (consultando a documentação do st.dataframe)
    exp_DadosBrutos.dataframe(data=df, 
                             # Ocultar a coluna de INDEX
                             hide_index=True, 
                             # Configurar as colunas em DICIONARIOS com Chave = Nome do Campo e Valor = método COLUMNCONFIG                            
                             column_config={
                                "Valor":st.column_config.NumberColumn(label="Valor em R$",
                                                                    help="Valor do Saldo no dia",
                                                                    format="%.2f")
                             })

    # EXPANDER 2 - RESUMO POR INSTITUIÇÃO (Aba 2 da Planilha)
    
    # Para evitar a rolagem dentro do EXPANDER podemos criar ABAS/TABS para exibir os dados
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
    
    # Aba com os dados do Pivot   
    tab_dados.dataframe(data = df_instituicao , column_config=columns_format)
    
    # Aba com o gráfico de histórico
    tab_historico.subheader("A. Saldo Histórico", divider="gray")
    tab_historico.line_chart(data=df_instituicao)

    with tab_distrib:   # Aba com o gráfico de saldo atual usando WITH

        flt_data = st.pills(label="Selecione a data para ver o saldo", 
                            options=df_instituicao.index,
                            format_func=lambda x : x.strftime("%b-%y"))
        if flt_data:
            df_ultimosaldo = df_instituicao.sort_index().loc[flt_data]
            st.bar_chart(df_ultimosaldo)

    # EXPANDER 3 - EVOLUÇÃO PATRIMONIAL (Aba 3 da Planilha)

    # Para trabalhar a tabela de evolução precisamos primeiro agrupar por datas o nosso DF original
    # SE formos inserir nomes de colunas com ESPAÇOS podemos usar o recurso de UNPACKING de dcionários
    # usando **{} para especificar os pares no argumento do AGG
    
    # (01) Agrupar Patrimonio por data
    df_data = df.groupby(by='Data').agg(
        Patrimonio = ('Valor' , 'sum'))

    # (02) Aplicar a função para calcular as estatisiticas
    df_data = calc_general_stats(df_data)
    
    exp_Estatisticas = st.expander(label="03.Estatísticas Gerais")

    # (03) Configurar as colunas para exibição do st.DF
    columns_format = {
        'Patrimonio' : st.column_config.NumberColumn(label='Patrimonio' , format="%.2f") ,
        'Cresc. Patrimonio R$ Mes' : st.column_config.NumberColumn(label='Cresc. Patrimonio R$ Mes' , format="%.2f") ,
        'Cresc. Patrimonio % Mes' : st.column_config.NumberColumn(label='Cresc. Patrimonio % Mes' , format='percent') ,
        'Cresc. R$ MM.06' : st.column_config.NumberColumn(label='Cresc. R$ MM.06' , format="%.2f") ,
        'Cresc. R$ MM.12' : st.column_config.NumberColumn(label='Cresc. R$ MM.12' , format="%.2f")  ,
        'Cresc. R$ MM.24' : st.column_config.NumberColumn(label='Cresc. R$ MM.24' , format="%.2f") ,
        'Evolução R$ MM.06' : st.column_config.NumberColumn(label='Evolução R$ MM.06' , format="%.2f") ,
        'Evolução R$ MM.12' : st.column_config.NumberColumn(label='Evolução R$ MM.12' , format="%.2f") ,
        'Evolução R$ MM.24' : st.column_config.NumberColumn(label='Evolução R$ MM.24' , format="%.2f") ,
        'Evolução % MM.06' : st.column_config.NumberColumn(label='Evolução % MM.06' , format='percent') ,
        'Evolução % MM.12' : st.column_config.NumberColumn(label='Evolução % MM.12' , format='percent') ,
        'Evolução % MM.24' : st.column_config.NumberColumn(label='Evolução % MM.24' , format='percent') ,
        'Ganho Medio Diario R$' : st.column_config.NumberColumn(label='Ganho Medio Diario R$' , format="%.2f") ,
        'Diferença acumulada TT R$' : st.column_config.NumberColumn(label='Diferença acumulada TT R$' , format="%.2f") ,
        'Diferença acumulada TT %' : st.column_config.NumberColumn(label='Diferença acumulada TT %' , format='percent')
    }

    tab_dados , tab_abs , tab_relativo = exp_Estatisticas.tabs(tabs=['Dados', 'Evolução Absoluta' , 'Crescimento Relativo'])

    with tab_dados:
        st.dataframe(df_data , column_config=columns_format)

    with tab_abs:
        abs = ['Cresc. Patrimonio R$ Mes', 'Cresc. R$ MM.06' ,'Cresc. R$ MM.12', 'Cresc. R$ MM.24']
        st.line_chart(df_data[abs])
    
    with tab_relativo:
        rel = ['Cresc. Patrimonio % Mes', 'Evolução % MM.06' ,'Evolução % MM.12', 'Evolução % MM.24']
        st.line_chart(df_data[rel])



    # EXPANDER 4 - METAS (Aba 4 da Planilha)

    with st.expander(label="04. Metas") as exp_Metas:

        # Organizar em colunas o Expander
        col11 , col12 = st.columns(spec=2)

        with col11:
            st.caption("Valor de início da meta")
            # Seletor da data de inicio da meta (ocultando o label para alinhar com col2)
            data_inicio_meta = st.date_input(label="Data de Início da Meta",
                                             label_visibility='collapsed' ,
                                             value=df_data.index.min() ,
                                             min_value=df_data.index.min() ,
                                             max_value=df_data.index.max())
            
            # Quando uma data anterior ao dia 5 de cada mes for selecionada, devemos pegar
            # o valor do mês anterior, então fazemos o filtro de todas as datas que antecedem
            # ou são iguais ao filtro e pegamos o ultimo valor
            data_filtrada = df_data.index[df_data.index <= data_inicio_meta][-1]
        
        with col12:
            # Valor do Patrimonio no periodo
            valor_inicio = df_data.loc[data_filtrada]["Patrimonio"]
            st.caption("Valor de início da meta")
            st.markdown(f"**R$ {valor_inicio:.2f}**")
            
        
        # Organizar as colunas dos proximos inputs
        col21 , col22 , col23 = st.columns(spec=3)

        salario_bruto_mensal = col21.number_input(label="Salário Bruto (R$)" , 
                                                  min_value=0.0 , 
                                                  format="%.2f" , )
        salario_liquido_mensal = col22.number_input(label="Salário Líquido (R$)" , 
                                                    min_value=0.0 , 
                                                    format="%.2f" , )
        gastos_mensal = col23.number_input(label="Gastos Mensais (R$)" , 
                                           min_value=0.0 , 
                                           format="%.2f" , )

        col31 , col32 , col33 , col34 = st.columns(4)

        total_liquido_ano = salario_liquido_mensal * 12
        total_gastos_ano = gastos_mensal * 12
        arrecadacao_potencial_ano = total_liquido_ano - total_gastos_ano
        arrecadacao_potencial_mes = arrecadacao_potencial_ano / 12

        with col31:
            st.caption("Total Líquido Ano")
            st.markdown(f"**R$ {total_liquido_ano: .2f}**")
        
        with col32:
            st.caption("Total Gastos Ano")
            st.markdown(f"**R$ {total_gastos_ano: .2f}**")
        
        with col33:
            st.caption("Potencial Econ. Ano")
            st.markdown(f"**R$ {arrecadacao_potencial_ano: .2f}**")
        
        with col34:
            st.caption("Potencial Econ. Mês")
            st.markdown(f"**R$ {arrecadacao_potencial_mes: .2f}**")

        col41 , col42 = st.columns(2)
        
        meta_estipulada = col41.number_input(label=f"**Meta Estipulada (R$)**" , 
                                             min_value=0.0 , 
                                             format="%.2f")
        
        patrimonio_estimado = valor_inicio + meta_estipulada

        col42.caption(f"**Patrimônio Estimado pós meta**")
        col42.markdown(body=f"**R$ {patrimonio_estimado:.2f}**")