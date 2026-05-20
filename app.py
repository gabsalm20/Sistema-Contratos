import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="VL Construtora · Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS — POWER BI DARK BLUE
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');

/* BASE */
html, body, [class*="css"] {
    background-color: #0e1117;
    color: #e8eaf6;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

[data-testid="stAppViewContainer"] { background-color: #0e1117; }
[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
div.block-container { padding-top: 1.5rem; padding-bottom: 2rem; background-color: #0e1117; }
div[data-testid="stVerticalBlock"] { background-color: transparent; }
div[data-testid="stHorizontalBlock"] { background-color: transparent; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0d1526 100%);
    border-right: 1px solid #1a3a5c;
}
section[data-testid="stSidebar"] * { color: #c5d8f0 !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 14px; padding: 6px 0; }

/* KPI CARDS */
.kpi-card {
    background: linear-gradient(135deg, #0d2137 0%, #112c45 100%);
    border: 1px solid #1e4d7b;
    border-radius: 12px;
    padding: 20px 24px;
    min-height: 100px;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 100, 200, 0.2);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0078d4, #00b4d8);
}
.kpi-title {
    color: #7fb3d3;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}
.kpi-sub {
    color: #5b9bd5;
    font-size: 11px;
    margin-top: 6px;
}
.kpi-icon {
    position: absolute;
    top: 18px; right: 20px;
    font-size: 28px;
    opacity: 0.25;
}

/* STATUS CARDS */
.status-card {
    background: linear-gradient(135deg, #0d2137 0%, #112c45 100%);
    border: 1px solid #1e4d7b;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    min-height: 90px;
}
.status-card.pendente::before {
    content: '';
    display: block;
    height: 3px;
    border-radius: 3px 3px 0 0;
    background: #f59e0b;
    margin: -18px -20px 14px -20px;
    border-radius: 12px 12px 0 0;
}
.status-card.atrasada::before {
    content: '';
    display: block;
    height: 3px;
    background: #ef4444;
    margin: -18px -20px 14px -20px;
    border-radius: 12px 12px 0 0;
}
.status-card.andamento::before {
    content: '';
    display: block;
    height: 3px;
    background: #3b82f6;
    margin: -18px -20px 14px -20px;
    border-radius: 12px 12px 0 0;
}
.status-card.concluida::before {
    content: '';
    display: block;
    height: 3px;
    background: #10b981;
    margin: -18px -20px 14px -20px;
    border-radius: 12px 12px 0 0;
}
.status-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.status-value {
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
}

/* UPLOAD */
[data-testid="stFileUploader"] {
    background-color: #0d2137;
    border: 1px dashed #1e4d7b;
    border-radius: 12px;
    padding: 10px;
}

/* DIVIDER */
hr { border-color: #1a3a5c; }

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #1e4d7b;
    border-radius: 10px;
    overflow: hidden;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(90deg, #0064c8, #0078d4);
    color: white;
    border-radius: 8px;
    border: none;
    height: 42px;
    font-weight: 600;
    font-size: 13px;
    width: 100%;
    letter-spacing: 0.3px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #0078d4, #00b4d8);
    box-shadow: 0 4px 12px rgba(0, 120, 212, 0.4);
}

.stDownloadButton > button {
    background: linear-gradient(90deg, #057a3f, #059669);
    color: white;
    border-radius: 8px;
    border: none;
    height: 42px;
    font-weight: 600;
    width: 100%;
}

/* SECTION TITLE */
.section-title {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #5b9bd5;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1a3a5c;
}

/* ÚLTIMA ATUALIZAÇÃO */
.ultima-atualizacao {
    background: #0d2137;
    border: 1px solid #1e4d7b;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 12px;
    color: #7fb3d3;
    display: inline-block;
}

/* CHART CONTAINER */
.chart-container {
    background: linear-gradient(135deg, #0d2137 0%, #112c45 100%);
    border: 1px solid #1e4d7b;
    border-radius: 12px;
    padding: 16px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONSTANTES
# =====================================================

CAMINHO = "historico.csv"

COLUNAS = [
    "Solicitação", "Obra", "Solicitante",
    "Data", "Total", "Prazo",
    "Situação", "Status"
]

# =====================================================
# HELPERS
# =====================================================

def calcular_prazo(valor: float) -> int:
    """Retorna prazo em dias conforme faixa de valor."""
    if valor <= 5_000:
        return 15
    elif valor <= 100_000:
        return 30
    return 45


def calcular_situacao(data_str: str, prazo: int) -> str:
    """
    Calcula se a solicitação está 'Atrasada' ou 'No Prazo'
    com base na data da solicitação e no prazo em dias.
    """
    try:
        data_dt = pd.to_datetime(data_str, dayfirst=True, errors="coerce")
        if pd.isna(data_dt):
            return "No Prazo"
        dias_passados = (datetime.now() - data_dt).days
        return "Atrasada" if dias_passados > prazo else "No Prazo"
    except Exception:
        return "No Prazo"


def carregar_historico() -> pd.DataFrame:
    """Carrega ou cria o CSV de histórico."""
    if os.path.exists(CAMINHO):
        df = pd.read_csv(CAMINHO)
        # Garante todas as colunas
        for col in COLUNAS:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=COLUNAS)


def salvar_historico(df: pd.DataFrame):
    df.to_csv(CAMINHO, index=False)


def processar_excel(uploaded_file) -> tuple[pd.DataFrame, int]:
    """
    Lê o Excel enviado, extrai campos de cabeçalho e itens,
    retorna (dataframe_novos, qtd_importados).
    """
    df_raw = pd.read_excel(uploaded_file, header=None)
    df_raw = df_raw.dropna(how="all").reset_index(drop=True)

    dados = []
    solicitacao = obra = solicitante = data_sol = ""

    for _, linha in df_raw.iterrows():
        # Monta texto concatenado da linha para busca de campos
        celulas = [str(c).strip() for c in linha if pd.notna(c) and str(c).strip() != ""]
        linha_texto = " | ".join(celulas)
        linha_upper = linha_texto.upper()

        # ── Captura campos de cabeçalho ──────────────────────
        # Estratégia: pega o valor da última célula não-vazia da linha
        ultimo_valor = celulas[-1] if celulas else ""

        if "SOLICITAÇÃO" in linha_upper or "SOLICITACAO" in linha_upper:
            solicitacao = ultimo_valor

        elif "OBRA" in linha_upper and len(celulas) >= 2:
            solicitacao = celulas[0]   # primeira célula costuma ser o número
            obra = ultimo_valor

        elif "SOLICITANTE" in linha_upper:
            solicitante = ultimo_valor

        elif "DATA" in linha_upper and "SOLICITAÇÃO" not in linha_upper:
            data_sol = ultimo_valor

        # ── Captura linhas de item (numéricas) ────────────────
        # Critério: primeira célula começa com dígito ou tem formato "X.X"
        primeira = str(linha.iloc[0]).strip() if pd.notna(linha.iloc[0]) else ""

        eh_item = (
            primeira
            and primeira[0].isdigit()
            and any(c in primeira for c in [".", ",", " "])
        )

        if not eh_item:
            continue

        # Extrai todos os valores numéricos da linha
        numericos = []
        for cell in linha:
            if pd.isna(cell):
                continue
            try:
                val = pd.to_numeric(
                    str(cell).replace(".", "").replace(",", "."),
                    errors="coerce"
                )
                if pd.notna(val) and val > 0:
                    numericos.append(val)
            except Exception:
                pass

        if not numericos:
            continue

        total = max(numericos)
        prazo = calcular_prazo(total)
        situacao = calcular_situacao(data_sol, prazo)

        dados.append({
            "Solicitação": solicitacao,
            "Obra":        obra,
            "Solicitante": solicitante,
            "Data":        data_sol,
            "Total":       total,
            "Prazo":       prazo,
            "Situação":    situacao,
            "Status":      "Pendente"
        })

    return pd.DataFrame(dados), len(dados)


def recalcular_situacoes(df: pd.DataFrame) -> pd.DataFrame:
    """Recalcula a coluna Situação para todo o histórico (útil ao atualizar)."""
    if df.empty:
        return df
    df = df.copy()
    df["Total_num"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
    df["Prazo"]     = df["Total_num"].apply(calcular_prazo)
    df["Situação"]  = df.apply(
        lambda r: calcular_situacao(str(r["Data"]), int(r["Prazo"])), axis=1
    )
    df.drop(columns=["Total_num"], inplace=True)
    return df

# =====================================================
# ESTADO
# =====================================================

historico = carregar_historico()

# Recalcula situações ao carregar (atrasos podem mudar de dia para dia)
historico = recalcular_situacoes(historico)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0; text-align:center;">
        <div style="font-size:36px;">🏗️</div>
        <div style="font-size:18px; font-weight:700; color:#e8eaf6; margin-top:6px;">VL CONSTRUTORA</div>
        <div style="font-size:11px; color:#5b9bd5; letter-spacing:2px; margin-top:2px;">SISTEMA DE GESTÃO</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    menu = st.radio(
        "NAVEGAÇÃO",
        ["📊 Dashboard", "🗂️ Base de Dados", "📥 Exportar"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div style="font-size:10px; color:#3a6a9a; text-align:center; padding-top:10px;">
        VL Construtora © 2025<br>Gestão de Solicitações
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# ── DASHBOARD ────────────────────────────────────────
# =====================================================

if menu == "📊 Dashboard":

    # ── Cabeçalho ──────────────────────────────────────
    col_title, col_update = st.columns([7, 2])

    with col_title:
        st.markdown("""
        <div style="margin-bottom: 4px;">
            <span style="font-size:24px; font-weight:700; color:#e8eaf6;">📊 Dashboard Geral</span>
            <span style="font-size:13px; color:#5b9bd5; margin-left:12px;">Gestão de Solicitações · VL Construtora</span>
        </div>
        """, unsafe_allow_html=True)

    with col_update:
        if st.button("🔄 Atualizar dados"):
            historico = recalcular_situacoes(historico)
            salvar_historico(historico)
            st.rerun()

    # Última atualização
    ultima = datetime.now().strftime("%d/%m/%Y às %H:%M")
    st.markdown(f'<div class="ultima-atualizacao">🕐 Última atualização: <strong>{ultima}</strong></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Upload ─────────────────────────────────────────
    st.markdown('<div class="section-title">📤 Importar Planilha</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Arraste ou selecione um arquivo .xlsx",
        type=["xlsx"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        with st.spinner("Processando planilha..."):
            novos_df, qtd = processar_excel(uploaded_file)

        if qtd == 0:
            st.warning("⚠️ Nenhum item encontrado na planilha. Verifique o formato do arquivo.")
        else:
            # Remove duplicatas por número de solicitação
            historico["Solicitação"] = historico["Solicitação"].astype(str)
            novos_df["Solicitação"]  = novos_df["Solicitação"].astype(str)

            existentes = set(historico["Solicitação"].unique())
            novos_df   = novos_df[~novos_df["Solicitação"].isin(existentes)]

            if novos_df.empty:
                st.info("ℹ️ Todas as solicitações da planilha já estão registradas.")
            else:
                historico = pd.concat([historico, novos_df], ignore_index=True)
                historico = recalcular_situacoes(historico)
                salvar_historico(historico)
                st.success(f"✅ {len(novos_df)} nova(s) solicitação(ões) importada(s) com sucesso!")
                st.rerun()

    st.divider()

    # ── KPIs Principais ────────────────────────────────
    st.markdown('<div class="section-title">📈 Indicadores Gerais</div>', unsafe_allow_html=True)

    total_solic    = historico["Solicitação"].nunique()
    total_obras    = historico["Obra"].nunique()
    total_solicit  = historico["Solicitante"].nunique()
    valor_total    = pd.to_numeric(historico["Total"], errors="coerce").sum()

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-title">Total de Solicitações</div>
            <div class="kpi-value">{total_solic}</div>
            <div class="kpi-sub">solicitações registradas</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🏗️</div>
            <div class="kpi-title">Total de Obras</div>
            <div class="kpi-value">{total_obras}</div>
            <div class="kpi-sub">obras monitoradas</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">👤</div>
            <div class="kpi-title">Solicitantes</div>
            <div class="kpi-value">{total_solicit}</div>
            <div class="kpi-sub">usuários ativos</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-title">Valor Total</div>
            <div class="kpi-value">R$ {valor_total:,.0f}</div>
            <div class="kpi-sub">volume financeiro acumulado</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Status Cards ───────────────────────────────────
    st.markdown('<div class="section-title">🚦 Status das Solicitações</div>', unsafe_allow_html=True)

    n_pendentes  = int((historico["Status"] == "Pendente").sum())
    n_andamento  = int((historico["Status"] == "Em Andamento").sum())
    n_concluidas = int((historico["Status"] == "Concluída").sum())
    n_atrasadas  = int((historico["Situação"] == "Atrasada").sum())

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(f"""
        <div class="status-card pendente">
            <div class="status-label" style="color:#f59e0b;">🟡 Pendentes</div>
            <div class="status-value">{n_pendentes}</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown(f"""
        <div class="status-card andamento">
            <div class="status-label" style="color:#3b82f6;">🔵 Em Andamento</div>
            <div class="status-value">{n_andamento}</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown(f"""
        <div class="status-card concluida">
            <div class="status-label" style="color:#10b981;">🟢 Concluídas</div>
            <div class="status-value">{n_concluidas}</div>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown(f"""
        <div class="status-card atrasada">
            <div class="status-label" style="color:#ef4444;">🔴 Atrasadas</div>
            <div class="status-value">{n_atrasadas}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Gráficos ───────────────────────────────────────
    if not historico.empty:

        st.markdown('<div class="section-title">📊 Análises Visuais</div>', unsafe_allow_html=True)

        PLOTLY_LAYOUT = dict(
            paper_bgcolor="rgba(13,33,55,0)",
            plot_bgcolor="rgba(13,33,55,0)",
            font=dict(family="Segoe UI", size=11, color="#c5d8f0"),
            margin=dict(l=10, r=10, t=30, b=10),
            colorway=["#0078d4", "#00b4d8", "#50e6ff", "#005a9e", "#1da1f2"],
        )

        g1, g2 = st.columns(2)

        with g1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            obras_df = (
                historico
                .groupby("Obra")["Solicitação"]
                .nunique()
                .reset_index()
                .rename(columns={"Solicitação": "Qtd"})
                .sort_values("Qtd", ascending=True)
            )

            fig_obras = go.Figure(go.Bar(
                x=obras_df["Qtd"],
                y=obras_df["Obra"],
                orientation="h",
                marker=dict(
                    color=obras_df["Qtd"],
                    colorscale=[[0, "#005a9e"], [1, "#00b4d8"]],
                    showscale=False
                ),
                text=obras_df["Qtd"],
                textposition="outside",
                textfont=dict(color="#e8eaf6", size=12)
            ))

            fig_obras.update_layout(
                title=dict(text="Solicitações por Obra", font=dict(size=13, color="#7fb3d3")),
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False),
                **PLOTLY_LAYOUT
            )

            st.plotly_chart(fig_obras, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with g2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            solicit_df = (
                historico
                .groupby("Solicitante")["Solicitação"]
                .nunique()
                .reset_index()
                .rename(columns={"Solicitação": "Qtd"})
            )

            fig_solic = go.Figure(go.Pie(
                labels=solicit_df["Solicitante"],
                values=solicit_df["Qtd"],
                hole=0.6,
                marker=dict(colors=["#0078d4", "#00b4d8", "#50e6ff", "#005a9e", "#1da1f2", "#0064a4"]),
                textfont=dict(color="#e8eaf6", size=11),
                hovertemplate="%{label}<br>%{value} solicitações<extra></extra>"
            ))

            fig_solic.update_layout(
                title=dict(text="Distribuição por Solicitante", font=dict(size=13, color="#7fb3d3")),
                legend=dict(font=dict(color="#c5d8f0", size=10)),
                **PLOTLY_LAYOUT
            )

            st.plotly_chart(fig_solic, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Segundo par de gráficos
        g3, g4 = st.columns(2)

        with g3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            status_counts = historico["Status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Qtd"]

            cor_status = {
                "Pendente":     "#f59e0b",
                "Em Andamento": "#3b82f6",
                "Concluída":    "#10b981",
            }

            fig_status = go.Figure(go.Bar(
                x=status_counts["Status"],
                y=status_counts["Qtd"],
                marker_color=[cor_status.get(s, "#0078d4") for s in status_counts["Status"]],
                text=status_counts["Qtd"],
                textposition="outside",
                textfont=dict(color="#e8eaf6", size=12)
            ))

            fig_status.update_layout(
                title=dict(text="Solicitações por Status", font=dict(size=13, color="#7fb3d3")),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False, visible=False),
                **PLOTLY_LAYOUT
            )

            st.plotly_chart(fig_status, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with g4:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)

            sit_counts = historico["Situação"].value_counts().reset_index()
            sit_counts.columns = ["Situação", "Qtd"]

            cor_sit = {"No Prazo": "#10b981", "Atrasada": "#ef4444"}

            fig_sit = go.Figure(go.Pie(
                labels=sit_counts["Situação"],
                values=sit_counts["Qtd"],
                hole=0.6,
                marker=dict(colors=[cor_sit.get(s, "#0078d4") for s in sit_counts["Situação"]]),
                textfont=dict(color="#e8eaf6", size=12),
                hovertemplate="%{label}<br>%{value} solicitações<extra></extra>"
            ))

            fig_sit.update_layout(
                title=dict(text="No Prazo vs Atrasadas", font=dict(size=13, color="#7fb3d3")),
                legend=dict(font=dict(color="#c5d8f0", size=11)),
                **PLOTLY_LAYOUT
            )

            st.plotly_chart(fig_sit, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("📂 Nenhum dado ainda. Faça o upload de uma planilha para começar.")

# =====================================================
# ── BASE DE DADOS ─────────────────────────────────────
# =====================================================

elif menu == "🗂️ Base de Dados":

    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-size:22px; font-weight:700; color:#e8eaf6;">🗂️ Base Consolidada</span>
        <span style="font-size:12px; color:#5b9bd5; margin-left:12px;">Todas as solicitações registradas</span>
    </div>
    """, unsafe_allow_html=True)

    if historico.empty:
        st.info("📂 Nenhum registro encontrado. Importe uma planilha no Dashboard.")
    else:
        # Filtros rápidos
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            obras_lista = ["Todas"] + sorted(historico["Obra"].dropna().unique().tolist())
            filtro_obra = st.selectbox("Filtrar por Obra", obras_lista)

        with col_f2:
            status_lista = ["Todos"] + sorted(historico["Status"].dropna().unique().tolist())
            filtro_status = st.selectbox("Filtrar por Status", status_lista)

        with col_f3:
            sit_lista = ["Todas"] + sorted(historico["Situação"].dropna().unique().tolist())
            filtro_sit = st.selectbox("Filtrar por Situação", sit_lista)

        df_view = historico.copy()

        if filtro_obra   != "Todas": df_view = df_view[df_view["Obra"]    == filtro_obra]
        if filtro_status != "Todos": df_view = df_view[df_view["Status"]  == filtro_status]
        if filtro_sit    != "Todas": df_view = df_view[df_view["Situação"]== filtro_sit]

        st.markdown(f"<div style='font-size:12px;color:#5b9bd5;margin:8px 0;'>{len(df_view)} registro(s) exibido(s)</div>", unsafe_allow_html=True)

        # Edição de status inline
        st.markdown('<div class="section-title">✏️ Editar Status</div>', unsafe_allow_html=True)
        df_editavel = st.data_editor(
            df_view[["Solicitação", "Obra", "Solicitante", "Data", "Total", "Prazo", "Situação", "Status"]],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Pendente", "Em Andamento", "Concluída"],
                    required=True
                ),
                "Total": st.column_config.NumberColumn("Total (R$)", format="R$ %.2f"),
            },
            use_container_width=True,
            hide_index=True,
            num_rows="fixed"
        )

        if st.button("💾 Salvar alterações"):
            # Atualiza apenas as linhas visíveis no histórico original
            idx_map = df_view.index
            historico.loc[idx_map, "Status"] = df_editavel["Status"].values
            salvar_historico(historico)
            st.success("✅ Alterações salvas com sucesso!")
            st.rerun()

# =====================================================
# ── EXPORTAR ──────────────────────────────────────────
# =====================================================

elif menu == "📥 Exportar":

    st.markdown("""
    <div style="margin-bottom:20px;">
        <span style="font-size:22px; font-weight:700; color:#e8eaf6;">📥 Exportar Dados</span>
        <span style="font-size:12px; color:#5b9bd5; margin-left:12px;">Baixe o histórico completo</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-card" style="max-width:400px; margin-bottom:24px;">
        <div class="kpi-title">REGISTROS DISPONÍVEIS</div>
        <div class="kpi-value">{len(historico)}</div>
        <div class="kpi-sub">linhas no histórico consolidado</div>
    </div>
    """, unsafe_allow_html=True)

    nome_arquivo = f"vl_construtora_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    try:
        historico.to_excel("historico_exportado.xlsx", index=False, engine="openpyxl")

        with open("historico_exportado.xlsx", "rb") as f:
            st.download_button(
                label="📥 Baixar Excel (.xlsx)",
                data=f,
                file_name=nome_arquivo,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"Erro ao gerar arquivo: {e}. Verifique se o openpyxl está instalado (pip install openpyxl).")

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 O arquivo exportado contém todas as colunas: Solicitação, Obra, Solicitante, Data, Total, Prazo, Situação e Status.")