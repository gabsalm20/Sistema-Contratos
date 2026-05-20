"""
VL Construtora – Análise de Contrato
Sistema de gestão de solicitações de serviços por obra.

Regras:
- 1 solicitação = 1 linha (múltiplos serviços agrupados)
- Prazo conta da segunda-feira seguinte à data da solicitação
- Fim de Cotação = Início de Cotação + 15 dias
- Elaboração Contrato = Fim de Cotação + 5 dias
- Prazo de Assinatura = Elaboração Contrato + 10 dias
- Status: Concluído se Contrato Assinado == Assinado
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime, date, timedelta
from io import BytesIO

LOGO_B64 = "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"


st.set_page_config(
    page_title="VL Construtora · Análise de Contrato",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html,body,[class*="css"]{background:#07111f;color:#cde0f5;font-family:'Inter',system-ui,sans-serif;}
[data-testid="stAppViewContainer"]{background:#07111f;}
[data-testid="stHeader"]{background:transparent;}
div.block-container{padding-top:1rem;padding-bottom:2rem;background:#07111f;max-width:1440px;}

/* sidebar */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#030812 0%,#060f1e 60%,#081428 100%);
    border-right:1px solid #112030;}
section[data-testid="stSidebar"] *{color:#9ec4e8 !important;}
section[data-testid="stSidebar"] .stRadio label{
    font-size:13px;font-weight:500;padding:7px 10px;border-radius:7px;transition:background .15s;}
section[data-testid="stSidebar"] .stRadio label:hover{background:rgba(0,90,190,.2);}

/* kpi */
.kpi-card{background:linear-gradient(145deg,#091e36,#0d2640);border:1px solid #163550;
    border-radius:13px;padding:18px 20px 14px;position:relative;overflow:hidden;
    transition:transform .15s,box-shadow .15s;min-height:100px;}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,80,180,.18);}
.kpi-card .bar{position:absolute;top:0;left:0;right:0;height:3px;border-radius:13px 13px 0 0;}
.kpi-card .ico{position:absolute;top:14px;right:16px;font-size:26px;opacity:.14;}
.kpi-lbl{font-size:9.5px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:#4a80aa;margin-bottom:8px;}
.kpi-val{font-size:30px;font-weight:800;color:#fff;line-height:1;}
.kpi-sub{font-size:10px;color:#2e5e84;margin-top:5px;}

/* sidebar metric */
.sb-metric{background:linear-gradient(145deg,#091e36,#0d2640);border:1px solid #163550;
    border-radius:10px;padding:12px 14px;margin-bottom:9px;position:relative;overflow:hidden;}
.sb-metric .bar{position:absolute;top:0;left:0;right:0;height:2px;border-radius:10px 10px 0 0;}
.sb-metric-lbl{font-size:8.5px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#3a6888;margin-bottom:4px;}
.sb-metric-val{font-size:20px;font-weight:800;color:#fff;line-height:1;}
.sb-metric-sub{font-size:9px;color:#264e6a;margin-top:3px;}

/* chips */
.status-chip{background:linear-gradient(145deg,#091e36,#0d2640);border:1px solid #163550;
    border-radius:11px;padding:14px 12px;text-align:center;position:relative;overflow:hidden;}
.status-chip .bar{position:absolute;top:0;left:0;right:0;height:3px;border-radius:11px 11px 0 0;}
.chip-lbl{font-size:9px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;}
.chip-val{font-size:24px;font-weight:800;color:#fff;}

/* section title */
.sec-title{font-size:9.5px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;
    color:#2e5e84;margin-bottom:11px;padding-bottom:6px;border-bottom:1px solid #112030;}

/* chart box */
.chart-box{background:linear-gradient(145deg,#091e36,#0d2640);border:1px solid #163550;
    border-radius:13px;padding:14px 14px 6px;}

[data-testid="stFileUploader"]{background:#091e36;border:1.5px dashed #163550;border-radius:11px;padding:6px;}
[data-testid="stDataFrame"],[data-testid="data-editor-container"]{border:1px solid #163550;border-radius:9px;overflow:hidden;}

.stButton>button{background:linear-gradient(90deg,#003fa0,#005cc8);color:#fff;border:none;
    border-radius:8px;height:38px;font-size:12px;font-weight:600;width:100%;transition:all .2s;}
.stButton>button:hover{background:linear-gradient(90deg,#005cc8,#0094d4);box-shadow:0 3px 12px rgba(0,92,200,.35);}
.stDownloadButton>button{background:linear-gradient(90deg,#03451f,#056635);color:#fff;border:none;
    border-radius:8px;height:38px;font-size:12px;font-weight:600;width:100%;}

.stTabs [data-baseweb="tab-list"]{background:transparent;border-bottom:1px solid #163550;}
.stTabs [data-baseweb="tab"]{background:transparent;border-radius:7px 7px 0 0;
    color:#4a80aa;font-size:12px;font-weight:500;padding:7px 16px;}
.stTabs [aria-selected="true"]{background:#0d2640 !important;color:#fff !important;
    border-bottom:2px solid #005cc8 !important;}

hr{border-color:#112030;}
.ts-badge{background:#091e36;border:1px solid #163550;border-radius:7px;
    padding:6px 12px;font-size:10px;color:#4a80aa;display:inline-block;}

.page-header{background:linear-gradient(135deg,#091e36 0%,#0c2240 60%,#091830 100%);
    border:1px solid #163550;border-radius:15px;padding:20px 26px;margin-bottom:18px;
    position:relative;overflow:hidden;}
.page-header::before{content:\'\';position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,#18e06a,#40f080,#005cc8,#00a0d8);border-radius:15px 15px 0 0;}
.page-title{font-size:24px;font-weight:800;color:#e8f4ff;letter-spacing:-.2px;}
.page-subtitle{font-size:12px;color:#3d6e90;margin-top:3px;font-weight:400;letter-spacing:.3px;}
.page-obra-tag{display:inline-block;background:rgba(0,92,200,.16);border:1px solid rgba(0,92,200,.35);
    border-radius:18px;padding:2px 11px;font-size:10px;font-weight:600;color:#55a0d8;
    margin-top:7px;letter-spacing:.4px;}

/* upload area múltipla */
.upload-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:4px;}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES EDITÁVEIS ──────────────────────────────────
HISTORICO_PATH           = "historico_vl.csv"
DIAS_JANELA_COTACAO      = 15
DIAS_COTACAO_CONTRATO    = 5
DIAS_CONTRATO_ASSINATURA = 10

COLUNAS_MANUAIS = [
    "Data Início Desejado","Início de Cotação",
    "Contrato Assinado","Status Cotação",
    "Observação 1","Observação 2","Observação 3",
]

COLUNAS_BASE2 = [
    "Solicitação","Data solicitada","Obra","Serviços","Qtd Serviços",
    "Solicitante","Data Início Desejado","Prazo Resposta (dias)",
    "Início de Cotação","Fim de Cotação","Elaboração Contrato",
    "Prazo de Assinatura","Contrato Assinado","Status Cotação",
    "Status","Observação 1","Observação 2","Observação 3",
    "Observação Original",
]

STATUS_COTACAO_OPTS = [
    "","Aguardando decisão da Obra","Solicitação Incompleta",
    "Em negociação","Em cotação","Fase de Proposta",
    "Negociação","Fornecedor Definido",
]

# paleta com variação real por gráfico
CORES_OBRAS    = ["#005cc8","#0080e0","#00a8f0","#00caf8","#40deff","#003088","#0050a8"]
CORES_STATUS   = {"Concluído":"#10b981","Em andamento":"#3b82f6",
                  "Aguardando cotação":"#f59e0b","Em atraso":"#ef4444"}
CORES_SOLIC    = ["#7c3aed","#a855f7","#c084fc","#581c87","#ddd6fe","#4c1d95","#ede9fe"]
CORES_COT      = ["#0e7490","#06b6d4","#67e8f9","#164e63","#a5f3fc","#083344","#cffafe"]

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", size=10, color="#7aabcc"),
    margin=dict(l=6, r=6, t=32, b=6),
)

# ── FUNÇÕES DE DATA ───────────────────────────────────────

def safe_parse_date(valor):
    """Converte para date Python puro. Nunca retorna NaT — sempre None ou date."""
    try:
        if valor is None:
            return None
        s = str(valor).strip()
        if s in ("","nan","NaT","None","NaN"):
            return None
        r = pd.to_datetime(s, dayfirst=True, errors="coerce")
        if pd.isnull(r):
            return None
        return r.date()
    except Exception:
        return None

def fmt_date(d):
    try:
        return d.strftime("%d/%m/%Y") if isinstance(d, date) else ""
    except Exception:
        return ""

def proxima_segunda(d):
    dias = (7 - d.weekday()) % 7
    return d + timedelta(days=dias if dias != 0 else 7)

def dias_entre(d1, d2):
    try:
        if not isinstance(d1, date) or not isinstance(d2, date):
            return None
        return (d2 - d1).days
    except Exception:
        return None

# ── PARSER BASE 1 ─────────────────────────────────────────

def parse_base1(uploaded_file):
    """Uma linha por solicitação; múltiplos serviços agrupados."""
    from openpyxl import load_workbook
    wb = load_workbook(uploaded_file, read_only=True, data_only=True)
    ws = wb.active
    solicitacoes, sol_atual, servicos, in_items = [], {}, [], False
    for row in ws.iter_rows(values_only=True):
        rv = [str(c).strip() if c is not None else "" for c in row]
        if rv[0] == "Solicitação":
            if sol_atual:
                sol_atual["servicos"] = servicos
                sol_atual["qtd"]      = len(servicos)
                solicitacoes.append(sol_atual)
            num = next((v for v in rv if v.isdigit() and len(v) >= 4), "")
            sol_atual = {"numero":num,"data":"","solicitante":"","obra":"","obs":"","total":0.0}
            servicos  = []
            in_items  = False
        elif rv[0] == "Data" and sol_atual and not in_items:
            sol_atual["data"]        = rv[3] if len(rv) > 3 else ""
            sol_atual["solicitante"] = rv[12] if len(rv) > 12 else ""
        elif rv[0] == "Obra" and sol_atual:
            sol_atual["obra"] = rv[3] if len(rv) > 3 else ""
        elif rv[0] == "Unidade construtiva" and sol_atual:
            in_items = True
        elif rv[0] == "Observação" and sol_atual:
            sol_atual["obs"] = " ".join(v for v in rv if v and v != "Observação")
            in_items = False
        elif in_items and rv[0] and rv[0][0].isdigit() and "." in rv[0]:
            desc = rv[1] if len(rv) > 1 else ""
            if desc and desc not in servicos:
                servicos.append(desc)
            for v in rv:
                try:
                    val = float(v.replace(".","").replace(",","."))
                    if val > sol_atual.get("total",0): sol_atual["total"] = val
                except Exception: pass
    if sol_atual:
        sol_atual["servicos"] = servicos
        sol_atual["qtd"]      = len(servicos)
        solicitacoes.append(sol_atual)
    rows = []
    for s in solicitacoes:
        rows.append({
            "Solicitação":s.get("numero",""),"Data solicitada":s.get("data",""),
            "Obra":s.get("obra",""),"Serviços":"; ".join(s.get("servicos",[])),
            "Qtd Serviços":str(s.get("qtd",0)),"Solicitante":s.get("solicitante",""),
            "Observação Original":s.get("obs",""),"Data Início Desejado":"",
            "Início de Cotação":"","Contrato Assinado":"","Status Cotação":"",
            "Observação 1":"","Observação 2":"","Observação 3":"",
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["Solicitação"] = df["Solicitação"].astype(str)
    return df

# ── CÁLCULOS DERIVADOS ────────────────────────────────────

def calcular_derivados(df):
    if df.empty: return df
    df   = df.copy()
    hoje = date.today()
    def prazo_resp(v):
        try:
            d = safe_parse_date(v)
            if d is None: return ""
            return str(max((hoje - proxima_segunda(d)).days, 0))
        except: return ""
    def fim_cot(v):
        try:
            d = safe_parse_date(v)
            return fmt_date(d + timedelta(days=DIAS_JANELA_COTACAO)) if d else ""
        except: return ""
    def elab_ctrt(v):
        try:
            d = safe_parse_date(v)
            return fmt_date(d + timedelta(days=DIAS_COTACAO_CONTRATO)) if d else ""
        except: return ""
    def prazo_assn(v):
        try:
            d = safe_parse_date(v)
            return fmt_date(d + timedelta(days=DIAS_CONTRATO_ASSINATURA)) if d else ""
        except: return ""
    def calc_status(row):
        try:
            if str(row.get("Contrato Assinado","")).strip().lower() == "assinado": return "Concluído"
            if not str(row.get("Início de Cotação","")).strip(): return "Aguardando cotação"
            p = str(row.get("Prazo Resposta (dias)","")).strip()
            if p.lstrip("-").isdigit() and int(float(p)) > 30: return "Em atraso"
            return "Em andamento"
        except: return "Aguardando cotação"
    df["Prazo Resposta (dias)"] = df["Data solicitada"].apply(prazo_resp)
    df["Fim de Cotação"]        = df["Início de Cotação"].apply(fim_cot)
    df["Elaboração Contrato"]   = df["Fim de Cotação"].apply(elab_ctrt)
    df["Prazo de Assinatura"]   = df["Elaboração Contrato"].apply(prazo_assn)
    df["Status"]                = df.apply(calc_status, axis=1)
    for col in COLUNAS_BASE2:
        if col not in df.columns: df[col] = ""
    return df[COLUNAS_BASE2]

# ── PERSISTÊNCIA ──────────────────────────────────────────

def carregar():
    if os.path.exists(HISTORICO_PATH):
        df = pd.read_csv(HISTORICO_PATH, dtype=str).fillna("")
        for col in COLUNAS_BASE2:
            if col not in df.columns: df[col] = ""
        return df
    return pd.DataFrame(columns=COLUNAS_BASE2)

def salvar(df):
    df.to_csv(HISTORICO_PATH, index=False)

def merge_historico(historico, novos):
    if historico.empty:
        return calcular_derivados(novos), len(novos)
    existentes = set(historico["Solicitação"].astype(str))
    novas = novos[~novos["Solicitação"].astype(str).isin(existentes)].copy()
    if novas.empty: return historico, 0
    resultado = pd.concat([historico, calcular_derivados(novas)], ignore_index=True)
    return calcular_derivados(resultado), len(novas)

# ── MÉTRICAS DE TEMPO ─────────────────────────────────────

def calc_media_total(df):
    vals = []
    for _, row in df.iterrows():
        try:
            d1 = safe_parse_date(row.get("Data solicitada",""))
            d2 = safe_parse_date(row.get("Contrato Assinado",""))
            diff = dias_entre(d1, d2)
            if diff and diff > 0: vals.append(diff)
        except: pass
    return round(sum(vals)/len(vals)) if vals else None

def calc_media_cotacao(df):
    vals = []
    for _, row in df.iterrows():
        try:
            d1 = safe_parse_date(row.get("Início de Cotação",""))
            d2 = safe_parse_date(row.get("Fim de Cotação",""))
            diff = dias_entre(d1, d2)
            if diff and diff > 0: vals.append(diff)
        except: pass
    return round(sum(vals)/len(vals)) if vals else None

def calc_media_prazo(df):
    vals = []
    for _, row in df.iterrows():
        try:
            v = str(row.get("Prazo Resposta (dias)","")).strip()
            if v.lstrip("-").isdigit():
                n = int(float(v))
                if n >= 0: vals.append(n)
        except: pass
    return round(sum(vals)/len(vals)) if vals else None

# ── HELPERS VISUAIS ───────────────────────────────────────

def kpi(label, value, sub, icon, color="#005cc8"):
    return (f'<div class="kpi-card">'
            f'<div class="bar" style="background:linear-gradient(90deg,{color},{color}70);"></div>'
            f'<div class="ico">{icon}</div>'
            f'<div class="kpi-lbl">{label}</div>'
            f'<div class="kpi-val">{value}</div>'
            f'<div class="kpi-sub">{sub}</div></div>')

def chip(label, value, color):
    return (f'<div class="status-chip">'
            f'<div class="bar" style="background:{color};"></div>'
            f'<div class="chip-lbl" style="color:{color};">{label}</div>'
            f'<div class="chip-val">{value}</div></div>')

def sb_metric(label, value, sub, color="#005cc8"):
    return (f'<div class="sb-metric">'
            f'<div class="bar" style="background:{color};"></div>'
            f'<div class="sb-metric-lbl">{label}</div>'
            f'<div class="sb-metric-val">{value}</div>'
            f'<div class="sb-metric-sub">{sub}</div></div>')

def render_header(titulo, subtitulo, obra_tag=None):
    tag = f'<div class="page-obra-tag">🏗️ {obra_tag}</div>' if obra_tag else ""
    ts  = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(
        f'<div class="page-header">'
        f'<div class="page-title">{titulo}</div>'
        f'<div class="page-subtitle">{subtitulo}</div>'
        f'{tag}'
        f'<div style="position:absolute;top:18px;right:22px;">'
        f'<div class="ts-badge">🕐 {ts}</div></div></div>',
        unsafe_allow_html=True
    )

# ── ESTADO ────────────────────────────────────────────────
if "historico" not in st.session_state:
    raw = carregar()
    st.session_state.historico = calcular_derivados(raw) if not raw.empty else raw

historico = st.session_state.historico

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    # Logo via st.image (mais confiável que HTML base64 no Streamlit Cloud)
    try:
        import base64, io
        from PIL import Image
        img_bytes = base64.b64decode(LOGO_B64)
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, use_container_width=False, width=120)
    except Exception:
        st.markdown("**VL**", unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center;font-size:8.5px;letter-spacing:2.5px;'+
        'color:#234a6a;padding-bottom:12px;margin-top:2px;">SISTEMA DE GESTÃO</div>',
        unsafe_allow_html=True
    )
    st.divider()

    menu = st.radio("", ["📊  Análise de Contrato","📋  Controle & Exportar"],
                    label_visibility="collapsed")
    st.divider()

    st.markdown('<div style="font-size:8.5px;font-weight:700;letter-spacing:1.6px;'+
                'color:#234a6a;text-transform:uppercase;margin-bottom:5px;">Filtrar Obra</div>',
                unsafe_allow_html=True)
    obras_disp = ["Todas as obras"]
    if not historico.empty:
        obras_disp += sorted(historico["Obra"].dropna().unique().tolist())
    obra_sel = st.selectbox("", obras_disp, label_visibility="collapsed")
    st.divider()

    st.markdown('<div style="font-size:8.5px;font-weight:700;letter-spacing:1.6px;'+
                'color:#234a6a;text-transform:uppercase;margin-bottom:9px;">Tempos Médios</div>',
                unsafe_allow_html=True)

    df_m = historico.copy() if not historico.empty else pd.DataFrame()
    if obra_sel != "Todas as obras" and not df_m.empty:
        df_m = df_m[df_m["Obra"] == obra_sel]

    tm_total = calc_media_total(df_m)   if not df_m.empty else None
    tm_cot   = calc_media_cotacao(df_m) if not df_m.empty else None
    tm_prazo = calc_media_prazo(df_m)   if not df_m.empty else None

    st.markdown(sb_metric("Sol. → Assinatura",
        f"{tm_total} dias" if tm_total is not None else "—",
        "tempo médio total","#10b981"), unsafe_allow_html=True)
    st.markdown(sb_metric("Janela de Cotação",
        f"{tm_cot} dias" if tm_cot is not None else "—",
        "início → fim de cotação","#3b82f6"), unsafe_allow_html=True)
    st.markdown(sb_metric("Prazo de Resposta",
        f"{tm_prazo} dias" if tm_prazo is not None else "—",
        "média desde a 2ª feira","#f59e0b"), unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-size:8px;color:#122030;text-align:center;">'+
                'VL Construtora © 2025</div>', unsafe_allow_html=True)

# ── filtro global ─────────────────────────────────────────
df_fil = historico.copy()
if obra_sel != "Todas as obras" and not historico.empty:
    df_fil = historico[historico["Obra"] == obra_sel].copy()

# ═════════════════════════════════════════════════════════
#  PÁGINA 1 — ANÁLISE DE CONTRATO
# ═════════════════════════════════════════════════════════
if menu == "📊  Análise de Contrato":

    render_header(
        "Análise de Contrato",
        "Monitoramento de solicitações · prazos · status de cotação e assinatura",
        obra_sel if obra_sel != "Todas as obras" else None
    )

    # ── Upload múltiplo (vários relatórios de uma vez) ──
    st.markdown('<div class="sec-title">📤 Importar planilhas — uma por obra, pode enviar várias de uma vez</div>',
                unsafe_allow_html=True)
    col_up, col_btn = st.columns([5,1])
    with col_up:
        uploaded_files = st.file_uploader(
            "Arraste um ou mais .xlsx do ERP",
            type=["xlsx"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="Selecione quantas obras quiser de uma só vez."
        )
    with col_btn:
        st.markdown("<div style='margin-top:4px;'></div>", unsafe_allow_html=True)
        if st.button("↻ Recalcular"):
            st.session_state.historico = calcular_derivados(historico)
            salvar(st.session_state.historico)
            st.rerun()

    if uploaded_files:
        total_novas = 0
        erros       = []
        df_atual    = historico.copy()
        for uf in uploaded_files:
            try:
                novos_df = parse_base1(uf)
                if novos_df.empty:
                    erros.append(f"⚠️ {uf.name}: nenhuma solicitação encontrada.")
                    continue
                df_atual, qtd = merge_historico(df_atual, novos_df)
                total_novas  += qtd
            except Exception as e:
                erros.append(f"❌ {uf.name}: {e}")

        st.session_state.historico = df_atual
        historico = df_atual
        df_fil    = historico if obra_sel == "Todas as obras" else                     historico[historico["Obra"] == obra_sel]
        salvar(df_atual)

        for msg in erros:
            st.warning(msg)
        if total_novas == 0 and not erros:
            st.info("ℹ️ Todas as solicitações já estão no histórico.")
        elif total_novas > 0:
            st.success(f"✅ {total_novas} nova(s) solicitação(ões) importada(s) de {len(uploaded_files)} arquivo(s)!")
            st.rerun()

    st.divider()

    # ── KPIs ─────────────────────────────────────────────
    st.markdown('<div class="sec-title">📈 Indicadores Gerais</div>', unsafe_allow_html=True)

    total_sol   = df_fil["Solicitação"].nunique() if not df_fil.empty else 0
    total_obras = df_fil["Obra"].nunique()         if not df_fil.empty else 0
    total_pess  = df_fil["Solicitante"].nunique()  if not df_fil.empty else 0
    total_serv  = sum(int(v) for v in df_fil["Qtd Serviços"] if str(v).lstrip("-").isdigit()) if not df_fil.empty else 0
    acima30     = sum(1 for v in df_fil["Prazo Resposta (dias)"] if str(v).lstrip("-").isdigit() and int(float(v))>30) if not df_fil.empty else 0
    conc        = int((df_fil["Status"]=="Concluído").sum()) if not df_fil.empty else 0

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: st.markdown(kpi("Solicitações",     total_sol,   f"{total_serv} serviços",      "📋","#005cc8"), unsafe_allow_html=True)
    with k2: st.markdown(kpi("Obras",            total_obras, "monitoradas",                 "🏗️","#0891b2"), unsafe_allow_html=True)
    with k3: st.markdown(kpi("Solicitantes",     total_pess,  "usuários com demandas",       "👤","#7c3aed"), unsafe_allow_html=True)
    with k4: st.markdown(kpi("Acima de 30 dias", acima30,     "prazo estourado",             "⏱️","#d97706"), unsafe_allow_html=True)
    with k5: st.markdown(kpi("Firmados",         conc,        "contratos concluídos",        "✅","#059669"), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)

    # ── Status chips ─────────────────────────────────────
    st.markdown('<div class="sec-title">🚦 Status das Solicitações</div>', unsafe_allow_html=True)
    cnt = df_fil["Status"].value_counts() if not df_fil.empty else pd.Series(dtype=int)
    s1,s2,s3,s4 = st.columns(4)
    with s1: st.markdown(chip("Aguardando cotação", int(cnt.get("Aguardando cotação",0)),"#f59e0b"), unsafe_allow_html=True)
    with s2: st.markdown(chip("Em andamento",       int(cnt.get("Em andamento",0)),      "#3b82f6"), unsafe_allow_html=True)
    with s3: st.markdown(chip("Concluído",          int(cnt.get("Concluído",0)),          "#10b981"), unsafe_allow_html=True)
    with s4: st.markdown(chip("Em atraso",          int(cnt.get("Em atraso",0)),          "#ef4444"), unsafe_allow_html=True)

    st.divider()

    # ── Gráficos em layout compacto 3 colunas ────────────
    if not df_fil.empty:
        st.markdown('<div class="sec-title">📊 Análises Visuais</div>', unsafe_allow_html=True)

        H = 260  # altura padrão de todos os gráficos

        # Linha 1: 3 colunas
        g1, g2, g3 = st.columns(3)

        # G1 — Solicitações por Obra
        with g1:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            d = df_fil.groupby("Obra")["Solicitação"].nunique().reset_index()
            d.columns = ["Obra","Qtd"]
            d = d.sort_values("Qtd")
            fig1 = go.Figure(go.Bar(
                x=d["Qtd"], y=d["Obra"], orientation="h",
                marker_color=CORES_OBRAS[:len(d)],
                text=d["Qtd"], textposition="outside",
                textfont=dict(color="#b0d4f0",size=11),
            ))
            fig1.update_layout(
                title=dict(text="Por Obra",font=dict(size=11,color="#4a80aa")),
                xaxis=dict(visible=False,showgrid=False),
                yaxis=dict(showgrid=False,tickfont=dict(size=10)),
                height=H, **PLOTLY_BASE)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # G2 — Status donut
        with g2:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            if not cnt.empty:
                cores2 = [CORES_STATUS.get(s,"#005cc8") for s in cnt.index]
                fig2 = go.Figure(go.Pie(
                    labels=cnt.index.tolist(), values=cnt.values.tolist(),
                    hole=0.60, marker=dict(colors=cores2),
                    textfont=dict(color="#cde0f5",size=10),
                    hovertemplate="%{label}: %{value}<extra></extra>",
                ))
                fig2.update_layout(
                    title=dict(text="Por Status",font=dict(size=11,color="#4a80aa")),
                    legend=dict(font=dict(color="#7aabcc",size=9),orientation="h",y=-0.15),
                    height=H, **PLOTLY_BASE)
                st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # G3 — Evolução mensal
        with g3:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            df_t = df_fil.copy()
            df_t["dt"] = pd.to_datetime(df_t["Data solicitada"], dayfirst=True, errors="coerce")
            df_t = df_t.dropna(subset=["dt"])
            if not df_t.empty:
                ev = df_t.groupby(df_t["dt"].dt.to_period("M"))["Solicitação"].nunique().reset_index()
                ev["Mês"] = ev["dt"].astype(str)
                fig3 = go.Figure(go.Scatter(
                    x=ev["Mês"], y=ev["Solicitação"],
                    mode="lines+markers",
                    line=dict(color="#10b981",width=2),
                    marker=dict(color="#34d399",size=6),
                    fill="tozeroy", fillcolor="rgba(16,185,129,.10)",
                ))
                fig3.update_layout(
                    title=dict(text="Evolução Mensal",font=dict(size=11,color="#4a80aa")),
                    xaxis=dict(showgrid=False,tickangle=-35,tickfont=dict(size=9)),
                    yaxis=dict(showgrid=False),
                    height=H, **PLOTLY_BASE)
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("Sem dados temporais.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Linha 2: 3 colunas
        g4, g5, g6 = st.columns(3)

        # G4 — Por Solicitante
        with g4:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            ds = df_fil.groupby("Solicitante")["Solicitação"].nunique().reset_index()
            ds.columns = ["Solicitante","Qtd"]
            ds = ds.sort_values("Qtd", ascending=False)
            fig4 = go.Figure(go.Bar(
                x=ds["Solicitante"], y=ds["Qtd"],
                marker_color=CORES_SOLIC[:len(ds)],
                text=ds["Qtd"], textposition="outside",
                textfont=dict(color="#b0d4f0",size=11),
            ))
            fig4.update_layout(
                title=dict(text="Por Solicitante",font=dict(size=11,color="#4a80aa")),
                xaxis=dict(showgrid=False,tickfont=dict(size=10)),
                yaxis=dict(visible=False,showgrid=False),
                height=H, **PLOTLY_BASE)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # G5 — Histograma de prazos
        with g5:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            prazos = pd.to_numeric(df_fil["Prazo Resposta (dias)"], errors="coerce").dropna()
            if not prazos.empty:
                fig5 = go.Figure(go.Histogram(
                    x=prazos, nbinsx=8,
                    marker=dict(color="#d97706", line=dict(color="#fbbf24",width=1)),
                ))
                fig5.update_layout(
                    title=dict(text="Prazo de Resposta (dias)",font=dict(size=11,color="#4a80aa")),
                    xaxis=dict(showgrid=False,title="dias",titlefont=dict(size=9)),
                    yaxis=dict(showgrid=False),
                    height=H, **PLOTLY_BASE)
                st.plotly_chart(fig5, use_container_width=True)
            else:
                st.info("Sem dados de prazo.")
            st.markdown('</div>', unsafe_allow_html=True)

        # G6 — Status de Cotação donut
        with g6:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            sc = df_fil["Status Cotação"].replace("","(sem status)").value_counts()
            if not sc.empty:
                fig6 = go.Figure(go.Pie(
                    labels=sc.index.tolist(), values=sc.values.tolist(),
                    hole=0.55, marker=dict(colors=CORES_COT[:len(sc)]),
                    textfont=dict(color="#cde0f5",size=10),
                    hovertemplate="%{label}: %{value}<extra></extra>",
                ))
                fig6.update_layout(
                    title=dict(text="Status de Cotação",font=dict(size=11,color="#4a80aa")),
                    legend=dict(font=dict(color="#7aabcc",size=9),orientation="h",y=-0.15),
                    height=H, **PLOTLY_BASE)
                st.plotly_chart(fig6, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("📂 Nenhum dado ainda. Faça o upload da Base 1 para começar.")


# ═════════════════════════════════════════════════════════
#  PÁGINA 2 — CONTROLE & EXPORTAR
# ═════════════════════════════════════════════════════════
elif menu == "📋  Controle & Exportar":

    render_header(
        "Controle & Exportar",
        "Edição de campos manuais · histórico consolidado · exportação",
        obra_sel if obra_sel != "Todas as obras" else None
    )

    if df_fil.empty:
        st.info("📂 Nenhum dado. Importe a Base 1 na página Análise de Contrato.")
    else:
        cf1,cf2,cf3 = st.columns(3)
        with cf1:
            st_opts = ["Todos"] + sorted(df_fil["Status"].dropna().unique().tolist())
            f_st = st.selectbox("Status", st_opts)
        with cf2:
            sl_opts = ["Todos"] + sorted(df_fil["Solicitante"].dropna().unique().tolist())
            f_sl = st.selectbox("Solicitante", sl_opts)
        with cf3:
            busca = st.text_input("🔍 Buscar", placeholder="nº ou palavra-chave…")

        df_view = df_fil.copy()
        if f_st != "Todos": df_view = df_view[df_view["Status"]      == f_st]
        if f_sl != "Todos": df_view = df_view[df_view["Solicitante"] == f_sl]
        if busca:
            mask = (df_view["Solicitação"].str.contains(busca,case=False,na=False)|
                    df_view["Serviços"].str.contains(busca,case=False,na=False))
            df_view = df_view[mask]

        st.markdown(f"<div style='font-size:10px;color:#2e5e84;margin:5px 0 9px;'>"
                    f"{len(df_view)} registro(s)</div>", unsafe_allow_html=True)

        tab_view, tab_edit, tab_exp = st.tabs(["👁️ Visualizar","✏️ Editar","📥 Exportar"])

        COLS_VIEW = ["Solicitação","Data solicitada","Obra","Solicitante","Serviços",
                     "Qtd Serviços","Prazo Resposta (dias)","Início de Cotação",
                     "Fim de Cotação","Elaboração Contrato","Prazo de Assinatura",
                     "Contrato Assinado","Status Cotação","Status"]

        with tab_view:
            st.dataframe(df_view[COLS_VIEW], use_container_width=True, hide_index=True,
                column_config={"Prazo Resposta (dias)":st.column_config.TextColumn("Prazo (dias)"),
                               "Qtd Serviços":st.column_config.TextColumn("Serviços")})

        with tab_edit:
            st.markdown("<div style='font-size:10px;color:#4a80aa;margin-bottom:9px;'>"
                        "Edite os campos manuais e clique em <strong>Salvar</strong>.</div>",
                        unsafe_allow_html=True)
            COLS_EDIT = ["Solicitação","Obra","Serviços","Data Início Desejado",
                         "Início de Cotação","Contrato Assinado","Status Cotação",
                         "Observação 1","Observação 2","Observação 3"]
            df_ed = st.data_editor(
                df_view[COLS_EDIT].copy(),
                column_config={
                    "Solicitação":st.column_config.TextColumn("Nº",disabled=True),
                    "Obra":st.column_config.TextColumn("Obra",disabled=True),
                    "Serviços":st.column_config.TextColumn("Serviços",disabled=True),
                    "Status Cotação":st.column_config.SelectboxColumn("Status Cotação",options=STATUS_COTACAO_OPTS),
                    "Contrato Assinado":st.column_config.SelectboxColumn("Contrato Assinado",
                                         options=["","Assinado","Pendente","Cancelado"]),
                },
                use_container_width=True, hide_index=True, num_rows="fixed",
            )
            if st.button("💾 Salvar alterações"):
                idx = df_view.index
                for col in COLUNAS_MANUAIS:
                    if col in df_ed.columns:
                        historico.loc[idx, col] = df_ed[col].values
                st.session_state.historico = calcular_derivados(historico)
                salvar(st.session_state.historico)
                st.success("✅ Salvo! Prazos recalculados.")
                st.rerun()

        with tab_exp:
            st.markdown(kpi("Registros disponíveis", len(historico),
                f"{historico['Obra'].nunique()} obra(s) · {historico['Solicitação'].nunique()} solicitação(ões)",
                "📂","#005cc8"), unsafe_allow_html=True)
            st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
            ex1,ex2 = st.columns(2)
            with ex1:
                st.markdown('<div class="sec-title">📄 CSV</div>', unsafe_allow_html=True)
                csv_data = historico.to_csv(index=False).encode("utf-8-sig")
                st.download_button("⬇️ Baixar CSV", data=csv_data,
                    file_name=f"vl_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv")
            with ex2:
                st.markdown('<div class="sec-title">📊 Excel</div>', unsafe_allow_html=True)
                try:
                    buf = BytesIO()
                    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                        historico.to_excel(writer, sheet_name="Controle", index=False)
                        pd.DataFrame({"Status Cotação":STATUS_COTACAO_OPTS[1:]}
                                     ).to_excel(writer, sheet_name="Referência", index=False)
                    st.download_button("⬇️ Baixar Excel", data=buf.getvalue(),
                        file_name=f"vl_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                except Exception as e:
                    st.error(f"Erro ao gerar Excel: {e}")
            st.divider()
            st.markdown('<div class="sec-title">👁️ Pré-visualização</div>', unsafe_allow_html=True)
            st.dataframe(historico.head(15), use_container_width=True, hide_index=True)
