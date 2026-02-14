from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import streamlit as st
import pandas as pd

def set_llm(groq_api_key):
    """
    Configura a chain da LLM para análise de sentimentos.

    Inicializa o modelo Llama-3.3, e define o parser de saída no formato JSON e 
    configura o prompt específico para a análise de reviews do produto 'Hegia'.

    Args:
        groq_api_key (str): A chave de API válida para o Groq.

    Returns:
        Runnable: Uma cadeia LangChain (Prompt | LLM | Parser) pronta para execução.
    """

    LLM = ChatGroq(
        model='llama-3.3-70b-versatile',
        temperature = 0,
        api_key=groq_api_key
    )
    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template='''
        Você é um mestre da psicologia bastante empático, e trabalha como analista de sentimentos de uma empresa do ramo da saúde.
        A empresa Hegia acabou de lanãr um novo produto: Uma máscara de dormir que melhora a noite de sono dos clientes
        
        TAREFA
        Analise as seguinte reviews: {reviews}

        OBJETIVOS:
        1. Classifique o sentimento das reviewsem (Positivo, Negativo ou Neutro)
        Exemplo: "Amei a máscara, dormi como um bebê" -> Positivo. "Horrível, uma porcaria" -> Negativo. 
        "Produto veio bem embalado e foi bom para dormir, mas a bateria é péssima e preciso recarregar todos os dias -> Neutro.
        2. Identifique pontos de melhoria de melhoria caso exista.
        3. Crie uma resposta automática empática ao cliente.
        4. Atribua um ID sequencial para cada review começando de 1 para cada review analisada.

        FORMATO DE SAÍDA:
        Retorne APENAS uma lista de objetos JSON. Sem markdown.
        As chaves do JSON devem ser estritamente: "id", "sentimento", "pontos_de_melhoria", "resposta_ao_cliente".

        EXEMPLO DE SAÍDA:
        [
            {{
                "id": 1,
                "sentimento": "Positivo",
                "pontos_de_melhoria": "Nenhum",
                "resposta_ao_cliente": "Ficamos felizes que tenha gostado!"
            }},
            {{
                "id": 2,
                "sentimento": "Negativo",
                "pontos_de_melhoria": "Elástico fraco",
                "resposta_ao_cliente": "Sinto muito pelo problema com o elástico..."
            }}
        ]
        ''',
        input_variables=['reviews']
    )

    return prompt | LLM | parser

def lendo_arquivo(arquivo):
    """
    Lê um arquivo (CSV ou Excel) e o converte para um DataFrame.

    Verifica a extensão do arquivo para determinar o método de leitura adequado.
    Em caso de erro, exibe uma mensagem no Streamlit e retorna um DataFrame vazio.

    Args:
        arquivo (UploadedFile): Objeto de arquivo vindo do st.file_uploader (ou similar).

    Returns:
        pd.DataFrame: O DataFrame contendo os dados do arquivo, ou vazio se houver erro.
    """

    try:
        if arquivo.name.endswith('csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        return pd.DataFrame()
    return df

def executar_analise(chain, df):
    """
    Executa a análise de sentimentos nos comentários do DataFrame usando a cadeia LLM.

    Invoca a chain configurada passando a coluna 'comentario' do DataFrame como entrada.

    Args:
        chain (Runnable): A cadeia LangChain configurada (retorno de set_llm).
        df (pd.DataFrame): DataFrame contendo obrigatoriamente a coluna 'comentario'.

    Returns:
        pd.DataFrame: Um novo DataFrame contendo os resultados da análise (ID, sentimento, resposta, etc).
    """
    try:
        resultado = chain.invoke(
            {
                'reviews' : df['comentario']
            }
        )
        return pd.DataFrame(resultado)
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        return pd.DataFrame()

@st.cache_data
def processar_reviews(arquivo, api_key):
    """
    Função orquestradora que processa o arquivo de reviews do início ao fim.

    Esta função é cacheada pelo Streamlit (@st.cache_data) para evitar reprocessamento 
    desnecessário de arquivos já analisados. Ela configura a LLM, lê o arquivo e executa a análise.

    Args:
        arquivo (UploadedFile): O arquivo enviado pelo usuário.
        api_key (str): A chave da API Groq.

    Returns:
        pd.DataFrame: DataFrame final consolidado com os resultados da análise.
    """
    chain = set_llm(api_key) 
    df_entrada = lendo_arquivo(arquivo)
    df_resultado = executar_analise(chain, df_entrada) 
    
    return df_resultado
