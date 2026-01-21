import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard Executivo - Análise por Cluster",
    page_icon="📊",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .kpi-container {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
        flex-wrap: nowrap;
        overflow-x: auto;
    }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #FFE700;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        min-width: 180px;
        flex: 1;
    }
    .kpi-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #6b7280;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 800;
        color: #1a1a1a;
        margin-bottom: 4px;
    }
    .kpi-delta-positive {
        color: #10b981;
        font-size: 13px;
        font-weight: 600;
    }
    .kpi-delta-negative {
        color: #ef4444;
        font-size: 13px;
        font-weight: 600;
    }
    .kpi-subtitle {
        font-size: 11px;
        color: #6b7280;
    }
    .filter-section {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stDataFrame {
        font-size: 11px;
    }
    div[data-testid="stExpander"] {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def parse_time_to_minutes(time_str):
    """Convert HH:MM:SS or HH:MM to minutes"""
    if not time_str or time_str == '-':
        return 0
    try:
        parts = time_str.replace('-', '').split(':')
        hours = int(parts[0]) if len(parts) > 0 else 0
        mins = int(parts[1]) if len(parts) > 1 else 0
        secs = int(parts[2]) if len(parts) > 2 else 0
        total_mins = hours * 60 + mins + secs / 60.0
        return -total_mins if time_str.startswith('-') else total_mins
    except:
        return 0

def format_time_from_minutes(mins):
    """Convert minutes to HH:MM format"""
    if mins == 0 or pd.isna(mins):
        return '-'
    hours = int(abs(mins) // 60)
    minutes = int(abs(mins) % 60)
    return f"{hours:02d}:{minutes:02d}"

def parse_percentage(pct_str):
    """Convert percentage string to float"""
    if not pct_str or pct_str == '-':
        return 0
    try:
        return float(str(pct_str).replace(',', '.').replace('%', ''))
    except:
        return 0

def parse_number(num_str):
    """Convert number string to float"""
    if not num_str or num_str == '-':
        return 0
    try:
        return float(str(num_str).replace(',', '.'))
    except:
        return 0

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); color: white; padding: 32px; border-radius: 16px; margin-bottom: 32px;">
    <h1 style="font-size: 28px; font-weight: 800; margin-bottom: 8px;">📊 Dashboard Executivo</h1>
    <p style="font-size: 14px; opacity: 0.9; font-weight: 300;">Análise Detalhada por Cluster - RBM 2.0 vs 1.0</p>
</div>
""", unsafe_allow_html=True)

# Upload section
st.markdown("### 📁 Upload do Arquivo CSV")
file_cluster = st.file_uploader(
    "Selecione o arquivo de análise por cluster",
    type=['csv'],
    key='cluster',
    help="Arquivo: [RBM 2.0] TESTES XSP4 V2 - ANÁLISE_CLUSTER.csv"
)

if file_cluster is not None:
    try:
        # Read CSV
        df = pd.read_csv(file_cluster, encoding='utf-8')
        
        # Parse data
        cluster_data = []
        for idx, row in df.iterrows():
            try:
                cluster_data.append({
                    'cluster': row['CLUSTER'],
                    'orh20': parse_time_to_minutes(row['ORH RBM 2.0']),
                    'orh10': parse_time_to_minutes(row['ORH RBM 1.0']),
                    'start20': row['MÉDIA INÍCIO ROTA RBM 2.0'],
                    'start10': row['MÉDIA INÍCIO ROTA RBM 1.0'],
                    'end20': row['MÉDIA FIM DA ROTA RBM 2.0'],
                    'end10': row['MÉDIA FIM ROTA RBM 1.0'],
                    'eta20': row['MÉDIA ETA RBM 2.0'],
                    'eta10': row['MÉDIA ETA RBM 1.0'],
                    'ocupacao20': parse_percentage(row['MÉDIA OCUPAÇÃO RBM 2.0']),
                    'ocupacao10': parse_percentage(row['MÉDIA OCUPAÇÃO RBM 1.0']),
                    'km20': parse_number(row['MÉDIA KM RBM 2.0']),
                    'km10': parse_number(row['AVERAGE de CONVERT_KM RBM 1.0']),
                    'col1520': parse_percentage(row['COLETA > 15 RBM 2.0']),
                    'col1510': parse_percentage(row['COLETA > 15 RBM 1.0']),
                    'paradas20': parse_number(row['PARADAS POR ROTA RBM 2.0']),
                    'paradas10': parse_number(row['PARADAS POR ROTA RBM 1.0']),
                    'spr20': parse_number(row['SPR RBM 2.0']),
                    'spr10': parse_number(row['SPR RBM 1.0']),
                    'qtdeRotas20': int(row['QTDE. ROTAS RBM 2.0']),
                    'qtdeRotas10': int(row['QTDE. ROTAS RBM 1.0']),
                    'difOrh': parse_time_to_minutes(row['DIF ORH']),
                    'xd20': row['DESLOCAMENTO ATÉ O XD RBM 2.0'],
                    'xd10': row['DESLOCAMENTO ATÉ O XD RBM 1.O']
                })
            except Exception as e:
                st.warning(f"Erro ao processar linha {idx}: {str(e)}")
                continue
        
        if not cluster_data:
            st.error("Nenhum dado válido encontrado no arquivo CSV")
            st.stop()
        
        # Calculate Big Numbers
        total_rotas20 = sum(c['qtdeRotas20'] for c in cluster_data)
        total_rotas10 = sum(c['qtdeRotas10'] for c in cluster_data)
        
        avg_spr20 = np.mean([c['spr20'] for c in cluster_data])
        avg_spr10 = np.mean([c['spr10'] for c in cluster_data])
        
        avg_paradas20 = np.mean([c['paradas20'] for c in cluster_data])
        avg_paradas10 = np.mean([c['paradas10'] for c in cluster_data])
        
        avg_orh20 = np.mean([c['orh20'] for c in cluster_data])
        avg_orh10 = np.mean([c['orh10'] for c in cluster_data])
        
        avg_col1520 = np.mean([c['col1520'] for c in cluster_data])
        avg_col1510 = np.mean([c['col1510'] for c in cluster_data])
        
        # Count clusters with ORH variation >= 40 min
        clusters_var40 = sum(1 for c in cluster_data if abs(c['difOrh']) >= 40)
        rotas_var40 = sum(c['qtdeRotas20'] for c in cluster_data if abs(c['difOrh']) >= 40)
        perc_volume = (rotas_var40 / total_rotas20 * 100) if total_rotas20 > 0 else 0
        
        # Display Big Numbers
        st.markdown("---")
        st.markdown("### 📈 Indicadores Principais")
        
        cols = st.columns(6)
        
        with cols[0]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">🚗 Veículos Roteirizados</div>
                <div class="kpi-value">{total_rotas20}</div>
                <div class="kpi-subtitle">RBM 1.0: {total_rotas10}</div>
                <div class="kpi-delta-{'positive' if total_rotas20 - total_rotas10 < 0 else 'negative'}">
                    {'▼' if total_rotas20 - total_rotas10 < 0 else '▲'} {abs(total_rotas20 - total_rotas10)}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">📍 SPR Médio</div>
                <div class="kpi-value">{avg_spr20:.0f}</div>
                <div class="kpi-subtitle">RBM 1.0: {avg_spr10:.0f}</div>
                <div class="kpi-delta-{'positive' if avg_spr20 - avg_spr10 > 0 else 'negative'}">
                    {'+' if avg_spr20 - avg_spr10 > 0 else ''}{avg_spr20 - avg_spr10:.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[2]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">🛑 Paradas por Rota</div>
                <div class="kpi-value">{avg_paradas20:.1f}</div>
                <div class="kpi-subtitle">RBM 1.0: {avg_paradas10:.1f}</div>
                <div class="kpi-delta-{'positive' if avg_paradas20 - avg_paradas10 > 0 else 'negative'}">
                    {'+' if avg_paradas20 - avg_paradas10 > 0 else ''}{avg_paradas20 - avg_paradas10:.1f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[3]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">⏱️ ORH Médio</div>
                <div class="kpi-value">{format_time_from_minutes(avg_orh20)}</div>
                <div class="kpi-subtitle">RBM 1.0: {format_time_from_minutes(avg_orh10)}</div>
                <div class="kpi-delta-{'negative' if avg_orh20 - avg_orh10 > 0 else 'positive'}">
                    {'+' if avg_orh20 - avg_orh10 > 0 else ''}{int(avg_orh20 - avg_orh10)}m
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[4]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-header">📦 Coleta > 15min</div>
                <div class="kpi-value">{avg_col1520:.1f}%</div>
                <div class="kpi-subtitle">RBM 1.0: {avg_col1510:.1f}%</div>
                <div class="kpi-delta-{'negative' if avg_col1520 - avg_col1510 > 0 else 'positive'}">
                    {'+' if avg_col1520 - avg_col1510 > 0 else ''}{avg_col1520 - avg_col1510:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with cols[5]:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #ef4444;">
                <div class="kpi-header">⚠️ VAR. ORH >= 40 Min</div>
                <div class="kpi-value">{clusters_var40}/{len(cluster_data)}</div>
                <div class="kpi-subtitle">
                    <strong>{perc_volume:.1f}%</strong> do volume<br>
                    ({rotas_var40} de {total_rotas20} rotas)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Filters Section
        st.markdown("---")
        st.markdown("### 🔍 Filtrar Colunas e Clusters")
        
        with st.expander("⚙️ Configurar Visualização", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📍 Clusters**")
                select_all_clusters = st.checkbox("Selecionar Todos os Clusters", value=True, key='all_clusters')
                
                if select_all_clusters:
                    selected_clusters = [c['cluster'] for c in cluster_data]
                else:
                    selected_clusters = st.multiselect(
                        "Clusters visíveis",
                        options=[c['cluster'] for c in cluster_data],
                        default=[c['cluster'] for c in cluster_data]
                    )
            
            with col2:
                st.markdown("**⏱️ Métricas Temporais**")
                show_orh = st.checkbox("ORH", value=True, key='orh')
                show_start = st.checkbox("START", value=True, key='start')
                show_end = st.checkbox("END", value=True, key='end')
                show_eta = st.checkbox("ETA", value=True, key='eta')
                show_xd = st.checkbox("XD", value=True, key='xd')
                show_col15 = st.checkbox("COLETA >15", value=True, key='col15')
            
            with col3:
                st.markdown("**⚙️ Métricas Operacionais**")
                show_spr = st.checkbox("SPR", value=True, key='spr')
                show_km = st.checkbox("KM", value=True, key='km')
                show_ocupacao = st.checkbox("OCUPAÇÃO", value=True, key='ocupacao')
                show_rotas = st.checkbox("QTDE ROTAS", value=True, key='rotas')
                show_paradas = st.checkbox("PARADAS", value=True, key='paradas')
        
        # Build table data
        st.markdown("---")
        st.markdown("### 📊 Comparação Detalhada por Cluster")
        
        # Filter data
        filtered_data = [c for c in cluster_data if c['cluster'] in selected_clusters]
        
        if not filtered_data:
            st.warning("Nenhum cluster selecionado. Por favor, selecione ao menos um cluster nos filtros.")
            st.stop()
        
        # Build DataFrame
        table_data = []
        for c in filtered_data:
            row = {'CLUSTER': c['cluster']}
            
            # Add alert if ORH variation > 40 min
            if abs(c['difOrh']) > 40:
                row['CLUSTER'] = '⚠️ ' + c['cluster']
            
            # ORH
            if show_orh:
                row['ORH RBM 1.0'] = format_time_from_minutes(c['orh10'])
                row['ORH RBM 2.0'] = format_time_from_minutes(c['orh20'])
                row['ORH Dif'] = f"{'+' if c['difOrh'] > 0 else ''}{int(c['difOrh'])}m"
            
            # START
            if show_start:
                row['START RBM 1.0'] = c['start10']
                row['START RBM 2.0'] = c['start20']
            
            # END
            if show_end:
                row['END RBM 1.0'] = c['end10']
                row['END RBM 2.0'] = c['end20']
            
            # ETA
            if show_eta:
                row['ETA RBM 1.0'] = c['eta10']
                row['ETA RBM 2.0'] = c['eta20']
            
            # XD
            if show_xd:
                row['XD RBM 1.0'] = c['xd10']
                row['XD RBM 2.0'] = c['xd20']
            
            # COLETA >15
            if show_col15:
                row['COL>15 RBM 1.0'] = f"{c['col1510']:.1f}%"
                row['COL>15 RBM 2.0'] = f"{c['col1520']:.1f}%"
                row['COL>15 Dif'] = f"{c['col1520'] - c['col1510']:+.1f}%"
            
            # SPR
            if show_spr:
                row['SPR RBM 1.0'] = f"{c['spr10']:.0f}"
                row['SPR RBM 2.0'] = f"{c['spr20']:.0f}"
                row['SPR Dif'] = f"{c['spr20'] - c['spr10']:+.0f}"
            
            # KM
            if show_km:
                row['KM RBM 1.0'] = f"{c['km10']:.1f}"
                row['KM RBM 2.0'] = f"{c['km20']:.1f}"
                row['KM Dif'] = f"{c['km20'] - c['km10']:+.1f}"
            
            # OCUPAÇÃO
            if show_ocupacao:
                row['OCUP RBM 1.0'] = f"{c['ocupacao10']:.1f}%"
                row['OCUP RBM 2.0'] = f"{c['ocupacao20']:.1f}%"
                row['OCUP Dif'] = f"{c['ocupacao20'] - c['ocupacao10']:+.1f}%"
            
            # ROTAS
            if show_rotas:
                row['ROTAS RBM 1.0'] = c['qtdeRotas10']
                row['ROTAS RBM 2.0'] = c['qtdeRotas20']
                row['ROTAS Dif'] = c['qtdeRotas20'] - c['qtdeRotas10']
            
            # PARADAS
            if show_paradas:
                row['PARADAS RBM 1.0'] = f"{c['paradas10']:.1f}"
                row['PARADAS RBM 2.0'] = f"{c['paradas20']:.1f}"
                row['PARADAS Dif'] = f"{c['paradas20'] - c['paradas10']:+.1f}"
            
            table_data.append(row)
        
        # Create DataFrame
        df_table = pd.DataFrame(table_data)
        
        # Style function for highlighting
        def highlight_deltas(val):
            """Highlight positive values in green and negative in red"""
            if isinstance(val, str):
                if '+' in val and 'Dif' in str(val):
                    return 'background-color: #d1fae5; color: #065f46; font-weight: bold'
                elif '-' in val and 'Dif' in str(val):
                    return 'background-color: #fee2e2; color: #991b1b; font-weight: bold'
            return ''
        
        # Display table
        st.dataframe(
            df_table,
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        # Download button
        st.download_button(
            label="📥 Download Tabela (CSV)",
            data=df_table.to_csv(index=False).encode('utf-8'),
            file_name=f"analise_cluster_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {str(e)}")
        st.exception(e)

else:
    st.info("👆 Faça upload do arquivo CSV para visualizar o dashboard")
    
    st.markdown("""
    ### 📋 Informações
    
    Este dashboard executivo mostra uma análise detalhada comparando RBM 2.0 vs RBM 1.0 por cluster.
    
    **Funcionalidades:**
    - ✅ 6 KPIs principais (Veículos, SPR, Paradas, ORH, Coleta >15, Variação ORH)
    - ✅ Filtros dinâmicos de clusters e métricas
    - ✅ Alertas automáticos (⚠️) para clusters com ORH > 40 min
    - ✅ Comparação lado a lado (1.0 vs 2.0)
    - ✅ Download da tabela filtrada em CSV
    
    **Métricas Temporais:** ORH, START, END, ETA, XD, COLETA >15
    
    **Métricas Operacionais:** SPR, KM, OCUPAÇÃO, QTDE ROTAS, PARADAS
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 12px; padding: 20px;">
    Dashboard Executivo - Análise por Cluster | RBM 2.0
</div>
""", unsafe_allow_html=True)
