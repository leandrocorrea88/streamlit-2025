# Projeto de Controle Financeiro usando Python e Streamlit

## Objetivo

Criar um aplicativo para gestão financeira simplificada, abordando:

1. Dados de entrada de saldos diários em contas : Armazenar o histórico da evolução dos saldos em conta para acompanhamento
2. Metas : Definir uma meta para acompanhamento e cálculo dos gaps

## Materiais de apoio

1. Planilha base com modelo completo : https://docs.google.com/spreadsheets/d/1DUbFpbWFhT09lRLH-gWy6T75wINwFIucc-WNVK8N378/edit?gid=1065601768#gid=1065601768 :Essa planilha tem o esqueleto do projeto que vamos usar como base para modelar nossa aplicação

2. Documentação do Streamlit : https://docs.streamlit.io/develop/api-reference/status/st.info

3. Lista de Icones Streamlit : https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

4. Referencias de formatação de datas : https://strftime.org/



## Preparação do ambiente

1. Criação da pasta e abertura dela no VSCode para organização do projeto

2. Criação do novo ambiente Python para proteger nossa aplicação de eventuais conflitos com bibliotecas. 

Ponto importante é que é provavel que ao abrir esse novo terminal ele ainda estará com o Conda desativado, por dois motivos comuns no windows:

- O Conda não foi inicializado para esse tipo de terminal
- O VSCode abriu um terminal padrão (CMD ou PowerShell) que ainda não “conhece” o Conda

Ou seja, pode ser que o Conda não esteja ativo nesse terminal. A questão é que o Conda não é só um executável, mas ele precisa

- Estar no PATH, ou
- Ser "injetado" no terminal via (conda init)

2.1. Testando se o Conda está ativado:

- Digite (conda --version) e/ou (python --version). Caso positivo, avance para 2.2
- Caso não esteja precisamos iniciaizar o 2.3

2.2. Injetando Conda no terminal VSConde

- Abra Anaconda prompt
- Teste os (conda --version) e (python --version) [pode ser que esse útlimo não esteja disponivel se não esivermos em nenhum ambiente criado]
- Ainda no anaconda prompt insira (conda init)
- Feche tudo, incluindo VSCode

2.3. Inicializado um novo ambiente

- Abra VSCode e o terminal integrado
- Agora digite conda -- version e where conda para saber onde está a raiz do ambiente
- Ative o ambiente base com (conda activate base)
- Se o (conda activate base) der erro podemos ativar de modo mais manual com
-- call D:\Tools\Anaconda\condabin\activate.bat [caminho do (where conda)]
-- conda activate base
- Agora podemos inserir o comando de criação de ambiente
-- conda create --name streamlit-2025 python=3.
-- Isso vai criar o ambiente com o nome "streamlit-2025" e carregar para ele a versão mais atualizada do Python 3 com 3.
-- Confirme com o "y" a instalação do packages básicos no novo ambiente
- Para visualizar os ambientes use o (conda env list) e garanta que o ambiente está criado
- Ative o ambiente com (conda activate streamlit-2025)

* Se deu ruim em algo e você precis remover um ambiente criado

- Primeiro desative o ambiente [se estiver ativo] com (conda deactivate)
- Isso vai voltar para o ambiente base
- Agora use (conda remove --name NOME_DO_AMBIENTE --all)
- Confirme a exclusão
- Garanta a exclusão com (conda env list)

3. Instale os principais pacotes para o seu novo ambiente, no nosso caso

- pip install streamlit

4. Crie a estrutura do novo programa

- Na raiz crie main.py
- Ative o intepretador no canto inferior direito, caso não esteja ativo, direcionando para o Python do ambiente criado

5. Teste o novo ambiente

- Teste algum comando no streamlit
-- import streamlit as st
-- st.text("Teste de streamlit")
- No terminal, acesse o programa usando (streamlit run main.py)
- Veja o browser abrindo com a mensagem plotada
- Faça mais um teste no main.py inserindo
-- st.set_page_config(page_title="Controle de Finanças 2025")
-- Se o navegador ainda estiver aberto dê um F5 e veja o titulo da pagina
-- Se o navegador foi fechado no terminal use (Crtl + C) para encerrar o servidor e rode novamente o streamlit run main.py

6. Criar repositório Git

- Acessar GitHub e criar o repositorio remoto
- Iniciar um terminal GitBash
- Acessar a pasta mãe do projeto e rodar (git init .)
- Criar a branch main com (git branch -m main)
- Criar o .gitignore e adicionar os arquivos/pastas
- Status -> Add . -> Commit -m NOME_DO_COMMIT