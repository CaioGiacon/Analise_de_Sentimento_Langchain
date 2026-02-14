import streamlit as st
import pandas as pd
from llm import processar_reviews
import altair as alt

st.set_page_config(page_title='Hegia Tech', page_icon='🌙', layout='wide')
st.title('🌙 Hegia Tech: Analisador de Sentimentos')
st.markdown('Faça upload das reviews dos clientes e deixe a IA gerar insights e respostas automáticas.')

with st.expander('Exemplo de formatação do arquivo (CSV ou Excel)'):
    st.markdown('O seu arquivo deve conter as opiniões em formato de texto. Seguindo o seguinte padrão de nomes nas colunas: ')
    
    df_exemplo = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'usuario': ['Ana Silva', 'Carlos Mendes', 'Mariana Souza', 'Ricardo Oliveira', 'Beatriz Costa'],
        'nota': [5, 2, 4, 1, 5],
        'comentario': [
            'A melhor compra que já fiz! O material é super macio e não aperta os olhos.',
            'A máscara é boa mas o elástico afrouxou em menos de uma semana de uso.',
            'Bloqueia a luz perfeitamente mas sinto que esquenta um pouco o rosto no verão.',
            'Péssima experiência. O cheiro de produto químico quando abri a caixa era insuportável.',
            'Finalmente consegui dormir durante o dia! Moro em frente a uma avenida e a luz não entra.'
        ]
    })
    
    st.dataframe(df_exemplo, use_container_width=True, hide_index=True)
    st.caption('Exemplo baseado em reviews reais de clientes.')

with st.expander('Subir Arquivo'):
    uploaded_file = st.file_uploader('Carregue seu arquivo de reviews (CSV ou Excel)', type=['csv', 'xlsx'])

with st.sidebar:
    st.image('https://cdn-icons-png.flaticon.com/512/2083/2083213.png', width=50) 
    st.title('Configurações')
    groq_api_key = st.text_input('Insira sua Groq API Key:', type='password')
    st.info('Sua chave não será salva, usada apenas para esta sessão.')

if uploaded_file and groq_api_key:
    if st.button('Iniciar Análise 🚀'):
        with st.spinner('A IA está analisando as reviews dos clientes... aguarde...'):
            df_resultado = processar_reviews(uploaded_file, groq_api_key)
            
            if not df_resultado.empty:
                st.success('Análise concluída!')

                tab1, tab2 = st.tabs(['📊 Dashboard Gerencial', '📄 Dados Detalhados'])
                with tab1:
                    st.subheader('Visão Geral dos Sentimentos')
                    col_metrica1, col_metrica2, col_metrica3, col_metrica4 = st.columns(4)
                    total = len(df_resultado)
                    positivos = len(df_resultado[df_resultado['sentimento'] == 'Positivo'])
                    negativos = len(df_resultado[df_resultado['sentimento'] == 'Negativo'])
                    neutros = len(df_resultado[df_resultado['sentimento'] == 'Neutro'])

                    col_metrica1.metric('Total Analisado', total)
                    col_metrica2.metric('Positivos', positivos, delta_color='normal')
                    col_metrica3.metric('Negativos', negativos, delta_color='inverse')
                    col_metrica4.metric('Neutros', neutros, delta_color='inverse')
                    
                    st.divider()
                    col_graf1, col_graf2 = st.columns(2)
                    
                    with col_graf1:
                        st.markdown('#### Distribuição de Sentimentos')
                        base = alt.Chart(df_resultado).encode(
                            theta=alt.Theta('count()', stack=True)
                        )
                        pie = base.mark_arc(outerRadius=120, innerRadius=80).encode(
                            color=alt.Color('sentimento', scale=alt.Scale(domain=['Positivo', 'Negativo', 'Neutro'], range=['#28a745', '#dc3545', '#ffc107'])),
                            order=alt.Order('sentimento', sort='descending'),
                            tooltip=['sentimento', 'count()']
                        )
                        text = base.mark_text(radius=140).encode(
                            text=alt.Text('count()'),
                            order=alt.Order('sentimento', sort='descending'),
                            color=alt.value('white')  
                        )
                        st.altair_chart(pie + text, use_container_width=True)

                    with col_graf2:
                        st.markdown('#### Principais Pontos de Melhoria')
                        df_problemas = df_resultado[df_resultado['pontos_de_melhoria'] != 'Nenhum']
                        
                        if not df_problemas.empty:
                            bar = alt.Chart(df_problemas).mark_bar().encode(
                                x=alt.X('count()', title='Qtd. Reclamações'),
                                y=alt.Y('pontos_de_melhoria', sort='-x', title='Ponto de Melhoria'),
                                color=alt.Color('pontos_de_melhoria', legend=None),
                                tooltip=['pontos_de_melhoria', 'count()']
                            )
                            st.altair_chart(bar, use_container_width=True)
                        else:
                            st.info('Nenhum ponto de melhoria identificado nos dados.')
                with tab2:
                    st.subheader('Resultados Detalhados')
                    st.dataframe(df_resultado, use_container_width=True)
                    
                    csv = df_resultado.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
                    st.download_button(
                        label='📥 Baixar Relatório CSV',
                        data=csv,
                        file_name='analise_hegia_final.csv',
                        mime='text/csv',
                    )
elif uploaded_file and not groq_api_key:
    st.warning('Por favor, insinar a sua API KEY para darmos prosseguimento na análise das reviews')