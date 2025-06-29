import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Otimização de Produção - Fábrica de Móveis",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para tema escuro
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .section-header {
        font-size: 1.5rem;
        color: #a476cf;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #a476cf;
        padding-bottom: 0.5rem;
    }
    
    .metric-container {
        background-color: #2a2829;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #a476cf;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background-color: #4a1a4a;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #a476cf;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #1a4a1a;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        width: fit-content;
    }
    
    .info-box {
        background-color: #1a1a4a;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4444ff;
        margin: 1rem 0;
    }
    
    .subsection-title {
        color: #a476cf;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<div class="main-header">Sistema de Otimização de Produção</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #cccccc; margin-bottom: 3rem;">Fábrica de Móveis - Programação Linear</div>', unsafe_allow_html=True)

# Dados fixos do problema
MATERIAIS = ["Tábua", "Prancha", "Painéis"]
PRODUTOS = ["Escrivaninha", "Mesa", "Armário", "Prateleira"]

# Matriz de consumo de materiais (FIXA) - metros por unidade de produto
CONSUMO_MATRIZ = np.array([
    [1, 1, 1, 4],  # Tábua: Escrivaninha=1, Mesa=1, Armário=1, Prateleira=4
    [0, 1, 1, 2],  # Prancha: Escrivaninha=0, Mesa=1, Armário=1, Prateleira=2
    [3, 2, 4, 0]   # Painéis: Escrivaninha=3, Mesa=2, Armário=4, Prateleira=0
])

# Disponibilidade inicial de recursos (metros)
DISPONIBILIDADE_INICIAL_DEFAULT = np.array([250, 600, 500])  # Tábua, Prancha, Painéis

# Preços de venda (padrão)
PRECOS_DEFAULT = np.array([100, 80, 120, 20])  # Escrivaninha, Mesa, Armário, Prateleira

# Inicializar session state
if 'quantidades' not in st.session_state:
    st.session_state.quantidades = [0, 0, 0, 0]

if 'disponibilidade' not in st.session_state:
    st.session_state.disponibilidade = DISPONIBILIDADE_INICIAL_DEFAULT.copy()

if 'precos' not in st.session_state:
    st.session_state.precos = PRECOS_DEFAULT.copy()

if 'modo_edicao' not in st.session_state:
    st.session_state.modo_edicao = False

# Usar valores do session state
DISPONIBILIDADE_INICIAL = st.session_state.disponibilidade
PRECOS = st.session_state.precos

# Layout em colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="section-header">Entrada de Dados</div>', unsafe_allow_html=True)
    
    # Botão para alternar modo de edição
    if not st.session_state.modo_edicao:
        if st.button("Editar Parâmetros", use_container_width=True):
            st.session_state.modo_edicao = True
            st.rerun()
    else:
        if st.button("Confirmar Alterações", use_container_width=True):
            st.session_state.modo_edicao = False
            st.rerun()
    
    # Exibir matriz de consumo fixa
    st.markdown('<p class="subsection-title">Matriz de Consumo de Materiais (Fixa)</p>', unsafe_allow_html=True)
    df_consumo = pd.DataFrame(
        CONSUMO_MATRIZ,
        index=MATERIAIS,
        columns=PRODUTOS
    )
    df_consumo = df_consumo.astype(str) + "m"
    st.dataframe(df_consumo, use_container_width=True)
    
    # Preços de venda - editáveis quando em modo de edição
    st.markdown('<p class="subsection-title">Preços de Venda</p>', unsafe_allow_html=True)
    if st.session_state.modo_edicao:
        st.markdown("*Editando preços de venda:*")
        precos_temp = []
        for i, produto in enumerate(PRODUTOS):
            preco = st.number_input(
                f"Preço {produto} (u.m.)",
                min_value=0.0,
                value=float(st.session_state.precos[i]),
                step=1.0,
                key=f"preco_{i}"
            )
            precos_temp.append(preco)
        st.session_state.precos = np.array(precos_temp)
        PRECOS = st.session_state.precos
    else:
        df_precos = pd.DataFrame({
            'Produto': PRODUTOS,
            'Preço (u.m.)': PRECOS
        })
        st.dataframe(df_precos, use_container_width=True, hide_index=True)
    
    # Disponibilidade de recursos - editável quando em modo de edição
    st.markdown('<p class="subsection-title">Disponibilidade de Recursos</p>', unsafe_allow_html=True)
    if st.session_state.modo_edicao:
        st.markdown("*Editando disponibilidade de recursos:*")
        disponibilidade_temp = []
        for i, material in enumerate(MATERIAIS):
            disponibilidade = st.number_input(
                f"Disponibilidade {material} (m)",
                min_value=0,
                value=int(st.session_state.disponibilidade[i]),
                step=1,
                key=f"disp_{i}"
            )
            disponibilidade_temp.append(disponibilidade)
        st.session_state.disponibilidade = np.array(disponibilidade_temp)
        DISPONIBILIDADE_INICIAL = st.session_state.disponibilidade
    else:
        df_disponibilidade = pd.DataFrame({
            'Recurso': MATERIAIS,
            'Disponibilidade (metros)': DISPONIBILIDADE_INICIAL
        })
        st.dataframe(df_disponibilidade, use_container_width=True, hide_index=True)
        
        # Mostrar receita máxima teórica (valores contínuos - permite frações)
        # Usar valores atuais do session state, não os iniciais fixos
        c_teorico = -st.session_state.precos
        A_ub_teorico = CONSUMO_MATRIZ
        b_ub_teorico = st.session_state.disponibilidade
        bounds_teorico = [(0, None) for _ in range(len(PRODUTOS))]
        
        from scipy.optimize import linprog
        resultado_teorico = linprog(c_teorico, A_ub=A_ub_teorico, b_ub=b_ub_teorico, bounds=bounds_teorico, method='highs')
        
        if resultado_teorico.success:
            receita_maxima_teorica = -resultado_teorico.fun
            st.metric("Máxima Teórica", f"{receita_maxima_teorica:.2f} u.m.")

with col2:
    st.markdown('<div class="section-header">Quantidades de Produção</div>', unsafe_allow_html=True)
    
    # Inputs para quantidades de produtos
    quantidades_novas = []
    for i, produto in enumerate(PRODUTOS):
        quantidade = st.number_input(
            f"Quantidade de {produto}",
            min_value=0,
            value=int(st.session_state.quantidades[i]),
            step=1,
            key=f"qty_{i}",
            format="%d"
        )
        quantidades_novas.append(int(quantidade))
    
    # Atualizar session state
    st.session_state.quantidades = quantidades_novas
    quantidades = np.array(quantidades_novas)

# Cálculos
st.markdown('<div class="section-header">Análise de Consumo</div>', unsafe_allow_html=True)

# Calcular consumo total
consumo_total = CONSUMO_MATRIZ @ quantidades
disponibilidade_restante = DISPONIBILIDADE_INICIAL - consumo_total
receita_atual = np.sum(PRECOS * quantidades)

# Exibir resultados em tabela
col3, col4 = st.columns([2, 1])

with col3:
    st.markdown('<p class="subsection-title">Análise de Consumo de Recursos</p>', unsafe_allow_html=True)
    
    # Criar DataFrame para análise de consumo
    status_recursos = []
    for i, material in enumerate(MATERIAIS):
        restante = disponibilidade_restante[i]
        status = "Excedido" if restante < 0 else "OK"
        status_recursos.append(status)
    
    df_analise = pd.DataFrame({
        'Recurso': MATERIAIS,
        'Disponível (m)': DISPONIBILIDADE_INICIAL,
        'Consumo (m)': consumo_total,
        'Restante (m)': disponibilidade_restante,
        'Status': status_recursos
    })
    st.dataframe(df_analise, use_container_width=True, hide_index=True)

with col4:
    st.markdown('<p class="subsection-title">Resumo Financeiro</p>', unsafe_allow_html=True)
    st.metric("Receita Atual", f"{receita_atual:.2f} u.m.", delta=None)
    
    # Verificar violações
    violacoes = np.sum(consumo_total > DISPONIBILIDADE_INICIAL)
    if violacoes > 0:
        st.markdown(f'<div class="warning-box">{violacoes} restrição(ões) violada(s)!</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="success-box">Todas as restrições respeitadas!</div>', unsafe_allow_html=True)

# Otimização Linear
st.markdown('<div class="section-header">Otimização Linear</div>', unsafe_allow_html=True)

def resolver_otimizacao():
    """Resolve o problema de programação linear para maximizar receita"""
    # Coeficientes da função objetivo (negativos para maximização)
    c = -PRECOS
    
    # Restrições de desigualdade (Ax <= b)
    A_ub = CONSUMO_MATRIZ
    b_ub = DISPONIBILIDADE_INICIAL
    
    # Limites das variáveis (x >= 0)
    bounds = [(0, None) for _ in range(len(PRODUTOS))]
    
    # Resolver
    resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    return resultado

# Resolver otimização
resultado = resolver_otimizacao()

col6, col7 = st.columns(2)

with col6:
    st.markdown('<p class="subsection-title">Solução Ótima</p>', unsafe_allow_html=True)
    
    if resultado.success:
        solucao_otima = resultado.x
        receita_otima = -resultado.fun
        
        # Converter para inteiros (arredondar para baixo para garantir viabilidade)
        solucao_otima_int = np.floor(solucao_otima).astype(int)
        receita_otima_int = np.sum(solucao_otima_int * PRECOS)
        
        # Exibir quantidades ótimas
        df_solucao = pd.DataFrame({
            'Produto': PRODUTOS,
            'Quantidade Ótima': solucao_otima_int,
            'Receita (u.m.)': (solucao_otima_int * PRECOS)
        })
        st.dataframe(df_solucao, use_container_width=True, hide_index=True)
        
        st.metric("Receita Máxima", f"{receita_otima_int:.2f} u.m.")
        
        # Botão para aplicar solução ótima
        if st.button("Aplicar Solução Ótima", use_container_width=True):
            st.session_state.quantidades = solucao_otima_int.tolist()
            st.rerun()
    else:
        st.markdown('<div class="warning-box">Não foi possível encontrar solução ótima!</div>', unsafe_allow_html=True)
        st.write(f"Motivo: {resultado.message}")

with col7:
    st.markdown('<p class="subsection-title">Análise de Sensibilidade</p>', unsafe_allow_html=True)
    
    if resultado.success:
        # Consumo com solução ótima
        consumo_otimo = CONSUMO_MATRIZ @ resultado.x
        margem_recursos = DISPONIBILIDADE_INICIAL - consumo_otimo
        
        # Preços sombra (dual values)
        precos_sombra = resultado.ineqlin.marginals if hasattr(resultado, 'ineqlin') else [0, 0, 0]
        
        df_sensibilidade = pd.DataFrame({
            'Recurso': MATERIAIS,
            'Consumo Ótimo': consumo_otimo.round(2),
            'Margem Disponível': margem_recursos.round(2)
        })
        st.dataframe(df_sensibilidade, use_container_width=True, hide_index=True)
        
        st.markdown('<div class="success-box">Solução encontrada com sucesso!</div>', unsafe_allow_html=True)

def resolver_otimizacao_recomendada():
    """Resolve otimização com produção mínima de 25 unidades por produto"""
    # Coeficientes da função objetivo (negativos para maximização)
    c = -PRECOS
    
    # Restrições de desigualdade (Ax <= b) - recursos
    A_ub = CONSUMO_MATRIZ
    b_ub = DISPONIBILIDADE_INICIAL
    
    # Restrições de igualdade para produção mínima (x >= 25)
    bounds = [(25, None) for _ in range(len(PRODUTOS))]
    
    # Resolver
    resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    return resultado

# Comparação atual vs ótimo vs recomendado
if resultado.success:
    st.markdown('<div class="section-header">Comparação: Atual vs Ótimo vs Recomendado</div>', unsafe_allow_html=True)
    
    # Resolver configuração recomendada
    resultado_recomendado = resolver_otimizacao_recomendada()
    
    col8, col9, col10 = st.columns(3)
    
    with col8:
        st.markdown('<p class="subsection-title">Configuração Atual</p>', unsafe_allow_html=True)
        df_atual = pd.DataFrame({
            'Produto': PRODUTOS,
            'Quantidade': quantidades,
            'Receita (u.m.)': (quantidades * PRECOS)
        })
        st.dataframe(df_atual, use_container_width=True, hide_index=True)
        st.metric("Receita Total", f"{receita_atual:.2f} u.m.")
    
    with col9:
        st.markdown('<p class="subsection-title">Configuração Ótima</p>', unsafe_allow_html=True)
        solucao_otima = resultado.x
        solucao_otima_int_display = np.floor(solucao_otima).astype(int)
        df_otima = pd.DataFrame({
            'Produto': PRODUTOS,
            'Quantidade': solucao_otima_int_display,
            'Receita (u.m.)': (solucao_otima_int_display * PRECOS)
        })
        st.dataframe(df_otima, use_container_width=True, hide_index=True)
        receita_otima_int_final = np.sum(solucao_otima_int_display * PRECOS)
        st.metric("Receita Total", f"{receita_otima_int_final:.2f} u.m.")
        
        # Diferença de receita
        diferenca = receita_otima_int_final - receita_atual
        if diferenca > 0:
            st.metric("Ganho Potencial", f"+{diferenca:.2f} u.m.", delta=f"+{((diferenca/receita_atual)*100):.1f}%" if receita_atual > 0 else None)
    
    with col10:
        st.markdown('<p class="subsection-title">Configuração Recomendada</p>', unsafe_allow_html=True)
        if resultado_recomendado.success:
            solucao_recomendada = resultado_recomendado.x
            solucao_recomendada_int = np.floor(solucao_recomendada).astype(int)
            df_recomendada = pd.DataFrame({
                'Produto': PRODUTOS,
                'Quantidade': solucao_recomendada_int,
                'Receita (u.m.)': (solucao_recomendada_int * PRECOS)
            })
            st.dataframe(df_recomendada, use_container_width=True, hide_index=True)
            receita_recomendada = np.sum(solucao_recomendada_int * PRECOS)
            st.metric("Receita Total", f"{receita_recomendada:.2f} u.m.")
            
            # Botão para aplicar configuração recomendada
            if st.button("Aplicar Configuração Recomendada", use_container_width=True):
                st.session_state.quantidades = solucao_recomendada_int.tolist()
                st.rerun()
        else:
            st.markdown('<div class="warning-box">Não é possível produzir 25+ de cada produto com os recursos disponíveis!</div>', unsafe_allow_html=True)
            st.write(f"Motivo: {resultado_recomendado.message}")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #888888; margin-top: 2rem;">'
    'Sistema de Otimização de Produção - Programação Linear<br>'
    'Desenvolvido por FATEC Ourinhos'
    '</div>', 
    unsafe_allow_html=True
)
