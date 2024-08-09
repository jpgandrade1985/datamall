import pandas as pd
from sqlalchemy import create_engine
import datetime
import streamlit as st
import os
import plotly.express as px

def graphs(filtered_df):
    #st.set_page_config(page_title="Legatus Data Mall", layout="wide")
    #Subtitle
    st.subheader("Vendas")
   
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("vendas ano x ano")
        fig1 = px.line(agg_df, color_discrete_sequence=px.colors.qualitative.Set2, x="nome_mes", y="venda_total", color='ano', facet_row="shopping")
        fig1.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vendas'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.write("vendas/m² ano x ano")
        fig2 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Set2, x="nome_mes", y="venda_total_m2", color='ano')
        fig2.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vendas / m² - área total'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig2, use_container_width=True)
    
    
    with col3:
        st.write("vendas/m² ocupado")
        fig3 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Set2, x="mes", y="venda_total_m2_ocupado", color='shopping')
        fig3.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vendas / m² - área ocupada'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig3, use_container_width=True)
    
    #Subtitle
    st.subheader("NOI")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.write("NOI Caixa")
        fig4 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="noi_caixa", color='shopping')
        fig4.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig4, use_container_width=True)
    
    with col5:
        st.write("NOI Caixa/m² total")
        fig5 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="noi_caixa_m2_abl_total", color='shopping')
        fig5.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa / m² - área total'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig5, use_container_width=True)
    
    
    with col6:
        st.write("NOI Caixa/m² ocupado")
        fig6 = px.line(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="noi_caixa_m2_abl_ocupado", color='shopping')
        fig6.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'NOI Caixa / m² ocupado'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig6, use_container_width=True)
    
    #Subtitle
    st.subheader("Vacância e Inadimplência")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.write("ABL vago")
        fig7 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="abl_vago", color='shopping', barmode='group')
        fig7.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'ABL Vago'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig7, use_container_width=True)
    
    with col8:
        st.write("Lojas Vagas")
        fig8 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="lojas_vagas", color='shopping', barmode='group')
        fig8.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Lojas Vagas'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig8, use_container_width=True)
    
    
    with col9:
        st.write("Vacância %")
        fig9 = px.bar(filtered_df, color_discrete_sequence=px.colors.qualitative.Safe, x="mes", y="vacancia_pct", color='shopping', barmode='group')
        fig9.update_layout(xaxis={'showticklabels': True, 'title': ''}, yaxis={'showticklabels': True, 'title': 'Vacância %'}, margin=dict(l=0, r=0, t=0, b=2))
        st.plotly_chart(fig9, use_container_width=True)

    with st.expander("Tabela de Dados"):
        # Display the filtered DataFrame
        st.write(filtered_df)
