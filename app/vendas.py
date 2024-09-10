import pandas as pd
from sqlalchemy import create_engine
import datetime
import streamlit as st
import os
import plotly.express as px
from app.py import agg_df

def graphs(filtered_df):
    #Subtitle
    st.subheader("Vendas")
    st.markdown(''':blue-background[As informações são melhor apresentadas se for selecionado apenas um shopping]''')
   
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("vendas ano x ano")
        fig1 = px.line(agg_df, color_discrete_sequence=px.colors.qualitative.T10, x="nome_mes", y="venda_total", color='shopping', facet_row="ano")
        fig1.update_traces(hovertemplate=None)
        fig1.update_layout(xaxis={'showticklabels': True, 'title': ''}, margin=dict(l=0, r=0, t=0, b=2), hovermode="x")
        fig1.update_yaxes(title_text="vendas", row=1)
        fig1.update_yaxes(title_text="vendas", row=2)
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig1, use_container_width=True)
        
    
    with col2:
        st.write("vendas/m² total ano x ano")
        fig2 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="nome_mes", y="venda_total_m2", color='ano', facet_row="shopping")
        fig2.update_traces(hovertemplate=None)
        fig2.update_layout(xaxis={'showticklabels': True, 'title': ''}, margin=dict(l=0, r=0, t=0, b=2), hovermode="x")
        fig2.update_yaxes(title_text="vendas/m²", row=1)
        fig2.update_yaxes(title_text="vendas/m²", row=2)
        fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig2, use_container_width=True)
    
    
    with col3:
        st.write("vendas/m² ocupado ano x ano")
        fig3 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="nome_mes", y="venda_total_m2_ocupado", color='ano', facet_row="shopping")
        fig3.update_traces(hovertemplate=None)
        fig3.update_layout(xaxis={'showticklabels': True, 'title': ''}, margin=dict(l=0, r=0, t=0, b=2), hovermode="x")
        fig3.update_yaxes(title_text="vendas/m²", row=1)
        fig3.update_yaxes(title_text="vendas/m²", row=2)
        fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig3, use_container_width=True)
    
    #Subtitle
    st.subheader("Por Tipo de Loja - Fazer os dados!!")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.write("NOI Caixa")
        fig4 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="mes", y="noi_caixa", color='shopping')
        fig4.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig4, use_container_width=True)

    #faz o gráfico de sunburst de vendas, classificando por tipo > setor > loja

        #df1 = df_vendas.loc[(df_vendas["data"] == "2023-08-01")] #deixar essa data como variável do dropdown
        #fig5 = px.sunburst(df1, path=['grupo', 'setor', 'nome_loja'], values='venda')
        #fig.show()

        #faz o gráfico de sunburst de vendas/m², classificando por tipo > setor > loja
        #df1 = df.loc[(df["data"] == "2023-08-01")]
        #df2 = df.loc[(df["data"] == "2023-09-01")]
        #fig5 = px.sunburst(df1, path=['grupo', 'setor', 'nome_loja'], values='venda_m2')
        #fig5.show()
    
    with col5:
        st.write("NOI Caixa/m² total")
        fig5 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="mes", y="noi_caixa_m2_abl_total", color='shopping')
        fig5.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa / m² - área total'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig5, use_container_width=True)
    
    
    with col6:
        st.write("NOI Caixa/m² ocupado")
        fig6 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="mes", y="noi_caixa_m2_abl_ocupado", color='shopping')
        fig6.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa / m² ocupado'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig6, use_container_width=True)
    
    #Subtitle
    st.subheader("Vacância")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.write("ABL vago")
        fig7 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="mes", y="abl_vago", color='shopping', barmode='group')
        fig7.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'ABL Vago'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig7, use_container_width=True)
    
    with col8:
        st.write("Lojas Vagas")
        fig8 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="mes", y="lojas_vagas", color='shopping', barmode='group')
        fig8.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Lojas Vagas'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig8, use_container_width=True)
    
    
    with col9:
        st.write("Vacância %")
        fig9 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.T10, x="mes", y="vacancia_pct", color='shopping', barmode='group')
        fig9.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vacância %'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig9, use_container_width=True)

    #Subtitle
    st.subheader("Inadimplência")

    with st.expander("Tabela de Dados"):
        # Display the filtered DataFrame
        st.write(filtered_df)
