## Análise de Sentimento com LangChain - Hegia Tech 🌙🤖
Este projeto é uma ferramenta de Processamento de Linguagem Natural (NLP) desenvolvida para analisar feedbacks de clientes sobre o novo produto da Hegia Tech: uma solução inovadora focada na melhoria da qualidade do sono.

A aplicação utiliza LangChain para orquestrar LLMs (Large Language Models) e Streamlit para a interface, permitindo que a equipe de produto transforme reviews desestruturadas em dados acionáveis (CSV) para métricas de sucesso.

# 🎯 Contexto do Negócio
A Hegia Tech acabou de lançar um dispositivo/produto para auxiliar pessoas com insônia e dificuldades para dormir. Com o aumento do volume de reviews em e-commerce e redes sociais, tornou-se inviável classificar manualmente cada comentário.

O objetivo deste software é automatizar a leitura dessas reviews para responder a perguntas de negócio:

- O sentimento geral é positivo ou negativo?

- Quais são as principais reclamações?

- O produto está cumprindo sua promessa de melhorar o sono?

# 🛠️ Tecnologias Utilizadas
- Python 3.x

- LangChain: Framework para orquestração da LLM.

- Streamlit: Criação da interface web interativa.

- Pandas: Manipulação de dados e exportação para CSV.

- LLM (Integração): Uso de modelos de linguagem para interpretação semântica do texto.

# ⚙️ Funcionalidades
1. Input de Dados: Interface para inserção de reviews (texto direto ou upload).

2. Processamento Inteligente: O sistema analisa o texto, identifica o sentimento (Positivo, Negativo, Neutro) e extrai pontos-chave.

3. Estruturação de Saída: Transforma a resposta textual da IA em um formato estruturado.

4. Exportação para Business Intelligence: Gera um arquivo .csv pronto para ser consumido por analistas ou ferramentas de visualização de dados.

# 💡 Decisões de Arquitetura e Desafios
Durante o desenvolvimento, algumas decisões técnicas foram tomadas para alinhar o projeto aos objetivos de negócio:

1. Estruturação da Resposta (JSON Parsing)
O Desafio: Inicialmente, tentei utilizar classes com BaseModel e Field (Pydantic) para forçar a LLM a responder em um formato estrito. No entanto, o modelo apresentava alucinações ou erros de formatação que quebravam o parser.

A Solução: Optei por utilizar o JsonOutputParser() diretamente e refinei a Engenharia de Prompt. Ao instruir a LLM com exemplos claros (Few-Shot Prompting) e focar na estrutura do parser direto na variável, consegui estabilidade na conversão de Texto -> Objeto Python.

2. Exportação: Por que CSV e não JSON?
A Decisão: Embora JSON seja o padrão para comunicação entre APIs, o objetivo deste projeto era resolver um problema de negócio imediato. A equipe de produto da Hegia Tech precisa metrificar o sucesso do lançamento agora.
Exportar para CSV permite que esses dados sejam imediatamente abertos no Excel, Google Sheets ou Power BI para criação de gráficos e relatórios, sem a necessidade de um sistema intermediário para ler JSON.

# 🚀 Como Executar o Projeto
1. Clone o repositório:

```Bash
git clone https://github.com/CaioGiacon/Analise_de_Sentimento_Langchain.git
cd Analise_de_Sentimento_Langchain
```

2. Instale as dependências:

```Bash
pip install -r requirements.txt
```

3. Configure as Variáveis de Ambiente:
   
Crie um arquivo .env na raiz e adicione sua chave de API (ex: Groq, OpenAI, etc, conforme seu código):

```Snippet de código
GROQ_API_KEY=sua_chave_aqui
```

4.Execute a aplicação:

```Bash
streamlit run app.py
```
# 📂 Estrutura do Projeto
```
/Analise_de_Sentimento_Langchain
│
├── app.py              # Interface principal (Streamlit)
├── chain.py            # Lógica da LangChain e Prompts (estimado)
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação
```

# 👤 Autor
Caio Giacon

Desenvolvedor focado em Engenharia de IA e soluções de software que resolvem problemas reais.



