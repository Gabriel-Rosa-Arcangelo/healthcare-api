# reports/pdf.py
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, Image
)

# ============ Paleta dark ============
HEX_BG       = "#0B0F19"   # fundo da página
HEX_TEXT     = "#E2E8F0"   # texto principal
HEX_MUTED    = "#A0AEC0"   # texto secundário
HEX_CYAN     = "#38B2AC"   # destaque/ações
HEX_PURPLE   = "#7C3AED"   # títulos/seções
HEX_CARD     = "#111827"   # painéis
HEX_BORDER   = "#2D3748"   # bordas sutis

C_BG     = colors.HexColor(HEX_BG)
C_TEXT   = colors.HexColor(HEX_TEXT)
C_MUTED  = colors.HexColor(HEX_MUTED)
C_CARD   = colors.HexColor(HEX_CARD)
C_BORDER = colors.HexColor(HEX_BORDER)

H1 = ParagraphStyle("H1", fontSize=16, textColor=colors.HexColor(HEX_CYAN),  leading=20, spaceAfter=6)
H2 = ParagraphStyle("H2", fontSize=11, textColor=colors.HexColor(HEX_PURPLE),leading=15, spaceAfter=4)
P  = ParagraphStyle("P",  fontSize=9,  textColor=C_TEXT,                 leading=12)

PAGE_IMG_W_MM = 162.0  # largura alvo para as imagens (dentro da margem)

# --------- fundo dark em cada página ---------
def _draw_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BG)
    # página inteira:
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
    canvas.restoreState()

# --------- Cards de métricas ----------
from reportlab.graphics.shapes import Drawing, Rect, String
def _metric_card(title, value, width=38*mm, height=20*mm):
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=C_CARD, strokeColor=C_BORDER, strokeWidth=0.6, radius=5))
    d.add(String(6, height-10, str(title), fontName="Helvetica", fontSize=8, fillColor=C_MUTED))
    d.add(String(6, height-18, str(value), fontName="Helvetica-Bold", fontSize=12, fillColor=C_TEXT))
    return d

def _summary_cards(story, stats: Dict[str, Any]):
    cards = [
        _metric_card("Rows", stats.get("rows","-")),
        _metric_card("Min value", stats.get("min","-")),
        _metric_card("Max value", stats.get("max","-")),
        _metric_card("Avg value", stats.get("avg","-")),
        _metric_card("% out-of-range", f"{stats.get('pct_out',0):.1f}%"),
    ]
    t = Table([cards], colWidths=[(PAGE_IMG_W_MM/5.0)*mm]*5)
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("BACKGROUND",(0,0),(-1,-1), C_BG),
        ("LEFTPADDING",(0,0),(-1,-1), 0),
        ("RIGHTPADDING",(0,0),(-1,-1), 6),
        ("TOPPADDING",(0,0),(-1,-1), 2),
        ("BOTTOMPADDING",(0,0),(-1,-1), 2),
    ]))
    story.append(t)
    story.append(Spacer(1, 6))

# --------- Helpers ----------
def _short(s: str, n=12):
    s = str(s)
    return s if len(s) <= n else s[:n-1] + "…"

# --------- Gráficos (dark style) ----------
def _render_bar_png(pairs: List[Tuple[str, float]], title="Top values"):
    labels = [p[0] for p in pairs]
    values = [float(p[1]) for p in pairs]

    # figura um pouco mais larga/baixa pra caber em 1 página
    fig_w_in, fig_h_in, dpi = 6.3, 2.7, 180
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in), dpi=dpi)

    bars = ax.bar(labels, values, edgecolor="#1F2937", linewidth=0.5)
    for b in bars:
        b.set_color(HEX_CYAN)

    ax.set_facecolor(HEX_BG)
    fig.patch.set_facecolor(HEX_BG)
    ax.tick_params(axis='x', labelrotation=0, labelsize=8, colors=HEX_TEXT)
    ax.tick_params(axis='y', colors=HEX_TEXT)
    ax.grid(axis='y', linestyle=':', linewidth=0.6, alpha=0.28, color="#718096")
    ax.set_title(title, color=HEX_PURPLE, fontsize=10, pad=6)
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    buf._aspect = fig_w_in / fig_h_in
    return buf

def _render_pie_png(labels: List[str], values: List[int], title="Distribution"):
    total = float(sum(values)) if values else 0.0

    # deixa a pizza maior (aumentando altura; mantém proporção sem distorção)
    fig_w_in, fig_h_in, dpi = 6.3, 3.1, 180
    fig, ax = plt.subplots(figsize=(fig_w_in, fig_h_in), dpi=dpi)
    fig.patch.set_facecolor(HEX_BG)
    ax.set_facecolor(HEX_BG)

    if total > 0:
        autopct = lambda pct: f"{pct:.1f}%"
        colors_pal = [HEX_CYAN, "#49BFB7", "#3D9BCB", "#2F78AD", "#225C8E"]
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct=autopct,
            startangle=90,
            colors=colors_pal,
            pctdistance=0.78,
            textprops={'fontsize':8, 'color':HEX_TEXT}
        )
        for t in texts:     t.set_color(HEX_TEXT)
        for t in autotexts: t.set_color(HEX_TEXT)

    ax.set_title(title, color=HEX_PURPLE, fontsize=10, pad=6)
    fig.tight_layout()

    buf = BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    buf._aspect = fig_w_in / fig_h_in
    return buf

# --------- Builder principal (1 página) ----------
def build_clinical_pdf(path_or_buffer, title: str, df, *, top_n=6, meta=None):
    """
    Gera 1 página dark:
      • Título + data + paciente
      • Cards: rows, min/max/avg, % out-of-range
      • Bar: Top N por valor
      • Pie: distribuição por faixas
    df esperado: colunas ["label", "value", "ref_low", "ref_high"]
    """
    # Estatísticas
    rows = len(df.index)
    vals = df["value"].astype(float) if rows else []
    ref_lo = df["ref_low"].astype(float) if rows else []
    ref_hi = df["ref_high"].astype(float) if rows else []
    out_mask = ((vals < ref_lo) | (vals > ref_hi)) if rows else []

    stats = {
        "rows": rows,
        "min": round(float(vals.min()), 2) if rows else "-",
        "max": round(float(vals.max()), 2) if rows else "-",
        "avg": round(float(vals.mean()), 2) if rows else "-",
        "pct_out": float(out_mask.mean()*100) if rows else 0.0,
    }

    # Documento
    doc = SimpleDocTemplate(
        path_or_buffer, pagesize=A4,
        leftMargin=12*mm, rightMargin=12*mm,
        topMargin=12*mm, bottomMargin=12*mm
    )
    story = []

    # Cabeçalho
    story.append(Paragraph(title, H1))
    subtitle = f"Generated at: {datetime.now():%Y-%m-%d %H:%M}"
    if meta and meta.get("patient"):
        subtitle += f" — Patient: <b>{meta['patient']}</b>"
    story.append(Paragraph(subtitle, H2))
    story.append(Spacer(1, 4))

    # Cards
    _summary_cards(story, stats)

    # Texto explicativo
    explain = [
        "This report summarizes recent lab results using a dark, portfolio-friendly layout. ",
        "We highlight the highest analyte values and illustrate the distribution across binned ranges. ",
        f"Currently, <b>{stats['pct_out']:.1f}%</b> of results fall outside reference intervals, which may require attention."
    ]
    story.append(Paragraph("".join(explain), P))
    story.append(Spacer(1, 4))

    # BAR: top N
    if rows:
        top_df = df.sort_values("value", ascending=False).head(top_n)
        pairs = list(zip([_short(x) for x in top_df["label"].tolist()],
                         top_df["value"].astype(float).tolist()))
        if pairs:
            bar = _render_bar_png(pairs, title=f"Top {top_n} by value")
            w = PAGE_IMG_W_MM; h = w / bar._aspect
            story.append(KeepTogether([Image(bar, width=w*mm, height=h*mm)]))
            story.append(Spacer(1, 4))

    # PIE: distribuição (4 bins)
    if rows:
        vmin, vmax = float(vals.min()), float(vals.max())
        rng = max(1.0, vmax - vmin); step = rng / 4.0
        edges = [vmin, vmin+step, vmin+2*step, vmin+3*step, vmax]
        labels = [f"{edges[i]:.1f}–{edges[i+1]:.1f}" for i in range(4)]
        counts = []
        for i in range(4):
            if i < 3:
                counts.append(int(((vals >= edges[i]) & (vals <  edges[i+1])).sum()))
            else:
                counts.append(int(((vals >= edges[i]) & (vals <= edges[i+1])).sum()))
        pie = _render_pie_png(labels, counts, title="Value distribution (bins)")
        w = PAGE_IMG_W_MM; h = w / pie._aspect
        story.append(KeepTogether([Image(pie, width=w*mm, height=h*mm)]))

    # Build com fundo dark nas páginas
    doc.build(story, onFirstPage=_draw_bg, onLaterPages=_draw_bg)
