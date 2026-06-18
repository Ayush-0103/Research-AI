import re
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas as rl_canvas


# ─────────────────────────────────────────────
#  Brand colours
# ─────────────────────────────────────────────
INDIGO       = colors.HexColor("#6366F1")
INDIGO_LIGHT = colors.HexColor("#818CF8")
INDIGO_DARK  = colors.HexColor("#4338CA")
VIOLET       = colors.HexColor("#8B5CF6")
SLATE_900    = colors.HexColor("#080C14")
SLATE_800    = colors.HexColor("#0F1623")
SLATE_700    = colors.HexColor("#1E293B")
SLATE_600    = colors.HexColor("#334155")
SLATE_400    = colors.HexColor("#94A3B8")
SLATE_300    = colors.HexColor("#CBD5E1")
SLATE_200    = colors.HexColor("#E2E8F0")
WHITE        = colors.HexColor("#FFFFFF")
EMERALD      = colors.HexColor("#10B981")
AMBER        = colors.HexColor("#F59E0B")

PAGE_W, PAGE_H = A4          # 210 × 297 mm
MARGIN_L = 20 * mm
MARGIN_R = 20 * mm
MARGIN_T = 24 * mm
MARGIN_B = 22 * mm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R


# ─────────────────────────────────────────────
#  Canvas template – headers / footers
# ─────────────────────────────────────────────
class ReportCanvas(rl_canvas.Canvas):
    """Adds a persistent header bar and footer to every page."""

    def __init__(self, filename, topic, **kwargs):
        super().__init__(filename, **kwargs)
        self._topic = topic
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page(num_pages)
            super().showPage()
        super().save()

    def _draw_page(self, total_pages):
        page_num = self._pageNumber

        # ── header bar (skip cover page 1) ────────────────────────────────
        if page_num > 1:
            # dark header strip
            self.setFillColor(SLATE_800)
            self.rect(0, PAGE_H - 14 * mm, PAGE_W, 14 * mm, fill=1, stroke=0)

            # accent line under header
            self.setFillColor(INDIGO)
            self.rect(0, PAGE_H - 14 * mm - 1, PAGE_W, 1.5, fill=1, stroke=0)

            # topic name (truncated)
            topic_short = self._topic if len(self._topic) <= 70 else self._topic[:67] + "…"
            self.setFillColor(SLATE_400)
            self.setFont("Helvetica", 7.5)
            self.drawString(MARGIN_L, PAGE_H - 9 * mm, topic_short.upper())

            # logo text right
            self.setFillColor(INDIGO_LIGHT)
            self.setFont("Helvetica-Bold", 7.5)
            self.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 9 * mm, "◈ ResearchAI")

        # ── footer ────────────────────────────────────────────────────────
        # accent line above footer
        self.setFillColor(SLATE_700)
        self.rect(0, MARGIN_B - 2 * mm, PAGE_W, 0.75, fill=1, stroke=0)

        # left: date
        self.setFillColor(SLATE_600)
        self.setFont("Helvetica", 7)
        self.drawString(MARGIN_L, MARGIN_B - 6 * mm,
                        datetime.now().strftime("%d %B %Y"))

        # centre: confidential tag
        self.setFillColor(SLATE_600)
        self.setFont("Helvetica", 7)
        self.drawCentredString(PAGE_W / 2, MARGIN_B - 6 * mm,
                               "CONFIDENTIAL — FOR INTERNAL USE ONLY")

        # right: page number
        self.setFillColor(SLATE_400)
        self.setFont("Helvetica-Bold", 7.5)
        self.drawRightString(PAGE_W - MARGIN_R, MARGIN_B - 6 * mm,
                             f"Page {page_num} / {total_pages}")


# ─────────────────────────────────────────────
#  Style sheet
# ─────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    return {
        # ── body / paragraphs ──
        "body": S("body",
            fontName="Helvetica", fontSize=9.5, leading=15,
            textColor=SLATE_300, alignment=TA_JUSTIFY,
            spaceAfter=5, spaceBefore=0),

        "body_small": S("body_small",
            fontName="Helvetica", fontSize=8.5, leading=13,
            textColor=SLATE_400, alignment=TA_LEFT, spaceAfter=3),

        # ── headings ──
        "h1": S("h1",
            fontName="Helvetica-Bold", fontSize=20, leading=26,
            textColor=SLATE_200, alignment=TA_LEFT,
            spaceBefore=14, spaceAfter=6),

        "h2": S("h2",
            fontName="Helvetica-Bold", fontSize=13.5, leading=18,
            textColor=INDIGO_LIGHT, alignment=TA_LEFT,
            spaceBefore=18, spaceAfter=4),

        "h3": S("h3",
            fontName="Helvetica-Bold", fontSize=11, leading=15,
            textColor=SLATE_200, alignment=TA_LEFT,
            spaceBefore=12, spaceAfter=3),

        "h4": S("h4",
            fontName="Helvetica-Bold", fontSize=9.5, leading=13,
            textColor=INDIGO_LIGHT, alignment=TA_LEFT,
            spaceBefore=8, spaceAfter=2),

        # ── bullet list ──
        "bullet": S("bullet",
            fontName="Helvetica", fontSize=9.5, leading=15,
            textColor=SLATE_300, alignment=TA_LEFT,
            leftIndent=14, firstLineIndent=0,
            spaceAfter=3, bulletIndent=0),

        # ── TOC entries ──
        "toc_section": S("toc_section",
            fontName="Helvetica-Bold", fontSize=9.5, leading=14,
            textColor=SLATE_200, leftIndent=0, spaceAfter=4),

        "toc_sub": S("toc_sub",
            fontName="Helvetica", fontSize=8.5, leading=13,
            textColor=SLATE_400, leftIndent=14, spaceAfter=2),

        # ── cover ──
        "cover_eyebrow": S("cover_eyebrow",
            fontName="Helvetica-Bold", fontSize=8.5, leading=12,
            textColor=INDIGO_LIGHT, alignment=TA_CENTER,
            spaceAfter=10, spaceBefore=0),

        "cover_title": S("cover_title",
            fontName="Helvetica-Bold", fontSize=30, leading=38,
            textColor=WHITE, alignment=TA_CENTER,
            spaceAfter=14, spaceBefore=0),

        "cover_subtitle": S("cover_subtitle",
            fontName="Helvetica", fontSize=12, leading=17,
            textColor=SLATE_400, alignment=TA_CENTER,
            spaceAfter=6),

        "cover_meta": S("cover_meta",
            fontName="Helvetica", fontSize=9, leading=13,
            textColor=SLATE_600, alignment=TA_CENTER,
            spaceAfter=4),
    }


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def hr(color=SLATE_700, thickness=0.75):
    return HRFlowable(width="100%", thickness=thickness,
                      color=color, spaceAfter=4, spaceBefore=4)


def accent_hr():
    return HRFlowable(width="100%", thickness=1.5,
                      color=INDIGO, spaceAfter=6, spaceBefore=0)


def sanitize(text: str) -> str:
    """Strip markdown and escape ReportLab XML special chars."""
    # Convert **bold** → <b>bold</b>
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*',     r'<b>\1</b>',        text)
    text = re.sub(r'\*(.+?)\*',          r'<i>\1</i>',        text)
    # Remove remaining bare * or # that leak through
    text = re.sub(r'^#+\s*', '', text)
    # Escape raw ampersands not already in entity form
    text = re.sub(r'&(?!amp;|lt;|gt;|nbsp;|#)', '&amp;', text)
    return text.strip()


def kpi_table(kpis: dict, styles: dict):
    """Render a 5-column KPI summary table."""
    if not kpis:
        return []
    labels = list(kpis.keys())
    values = list(kpis.values())
    n = len(labels)
    col_w = CONTENT_W / n

    val_style = ParagraphStyle("kpi_val",
        fontName="Helvetica-Bold", fontSize=14, leading=18,
        textColor=INDIGO_LIGHT, alignment=TA_CENTER)
    lbl_style = ParagraphStyle("kpi_lbl",
        fontName="Helvetica", fontSize=7, leading=10,
        textColor=SLATE_400, alignment=TA_CENTER)

    val_row = [Paragraph(str(v), val_style) for v in values]
    lbl_row = [Paragraph(l.upper(), lbl_style) for l in labels]

    t = Table([val_row, lbl_row], colWidths=[col_w] * n, rowHeights=[18, 13])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), SLATE_800),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [SLATE_800, SLATE_800]),
        ("BOX",         (0, 0), (-1, -1), 0.5, SLATE_700),
        ("INNERGRID",   (0, 0), (-1, -1), 0.4, SLATE_700),
        ("TOPPADDING",  (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING",(0, 0), (-1, -1), 4),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 8)]


# ─────────────────────────────────────────────
#  Cover page builder
# ─────────────────────────────────────────────
def build_cover(topic: str, styles: dict) -> list:
    story = []

    # ── large background handled by canvas; we just add flowables ──
    story.append(Spacer(1, 52 * mm))

    # eyebrow
    story.append(Paragraph("◈ &nbsp; AUTONOMOUS RESEARCH REPORT", styles["cover_eyebrow"]))
    story.append(Spacer(1, 2 * mm))

    # title (wrapped, centred)
    story.append(Paragraph(topic, styles["cover_title"]))
    story.append(Spacer(1, 6 * mm))

    # divider
    story.append(HRFlowable(width="40%", thickness=2, color=INDIGO,
                             hAlign="CENTER", spaceAfter=8, spaceBefore=0))

    story.append(Paragraph("Generated by <b>ResearchAI</b> — Autonomous Research Intelligence",
                            styles["cover_subtitle"]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        f"Strategic Research &amp; Intelligence Division &nbsp;|&nbsp; "
        f"{datetime.now().strftime('%d %B %Y')}",
        styles["cover_meta"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("CONFIDENTIAL — FOR INTERNAL USE ONLY", styles["cover_meta"]))

    story.append(PageBreak())
    return story


# ─────────────────────────────────────────────
#  TOC builder  (dynamic, from parsed sections)
# ─────────────────────────────────────────────
def build_toc(sections: list, styles: dict) -> list:
    story = []
    story.append(Paragraph("Table of Contents", styles["h1"]))
    story.append(accent_hr())
    story.append(Spacer(1, 4))

    for i, sec in enumerate(sections, 1):
        title = sec.get("title", "")
        subs  = sec.get("subs", [])
        story.append(Paragraph(f"{i}.&nbsp;&nbsp;{sanitize(title)}", styles["toc_section"]))
        for j, sub in enumerate(subs, 1):
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{i}.{j}&nbsp;&nbsp;{sanitize(sub)}",
                                   styles["toc_sub"]))

    story.append(PageBreak())
    return story


# ─────────────────────────────────────────────
#  Markdown → ReportLab flowables
# ─────────────────────────────────────────────
def parse_report(report_text: str, styles: dict) -> list:
    """
    Convert the markdown report text into a list of ReportLab flowables.
    Handles: # ## ### ####, bullet lists (- * •), numbered lists, blank lines,
    bold/italic inline, and horizontal rules.
    """
    story = []
    lines = report_text.split("\n")
    i = 0

    def flush_bullet(items, ordered=False):
        """Emit a bullet/numbered list block."""
        block = []
        for idx, item in enumerate(items, 1):
            prefix = f"{idx}.&nbsp;" if ordered else "&#8226;&nbsp;"
            block.append(Paragraph(f"{prefix}{sanitize(item)}", styles["bullet"]))
        return block

    bullet_buffer = []
    ordered_buffer = []

    def flush_buffers():
        out = []
        if bullet_buffer:
            out += flush_bullet(bullet_buffer, ordered=False)
            bullet_buffer.clear()
        if ordered_buffer:
            out += flush_bullet(ordered_buffer, ordered=True)
            ordered_buffer.clear()
        return out

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        # ── horizontal rule ──────────────────────────────────────────────
        if re.match(r'^-{3,}$', line) or re.match(r'^={3,}$', line):
            story += flush_buffers()
            story.append(hr())
            i += 1
            continue

        # ── headings ─────────────────────────────────────────────────────
        h4m = re.match(r'^####\s+(.*)', line)
        h3m = re.match(r'^###\s+(.*)', line)
        h2m = re.match(r'^##\s+(.*)', line)
        h1m = re.match(r'^#\s+(.*)', line)

        if h4m:
            story += flush_buffers()
            story.append(Paragraph(sanitize(h4m.group(1)), styles["h4"]))
            i += 1; continue
        if h3m:
            story += flush_buffers()
            story.append(Paragraph(sanitize(h3m.group(1)), styles["h3"]))
            i += 1; continue
        if h2m:
            story += flush_buffers()
            # H2 gets a left-accent bar rendered as a mini table
            text = sanitize(h2m.group(1))
            bar = Table(
                [[Paragraph(text, styles["h2"])]],
                colWidths=[CONTENT_W],
            )
            bar.setStyle(TableStyle([
                ("LEFTPADDING",  (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING",   (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
                ("LINEBEFORE",   (0, 0), (0, -1), 4, INDIGO),
                ("BACKGROUND",   (0, 0), (-1, -1), SLATE_800),
            ]))
            story.append(Spacer(1, 6))
            story.append(bar)
            story.append(Spacer(1, 4))
            i += 1; continue
        if h1m:
            story += flush_buffers()
            story.append(Spacer(1, 8))
            story.append(Paragraph(sanitize(h1m.group(1)), styles["h1"]))
            story.append(accent_hr())
            i += 1; continue

        # ── unordered bullet ─────────────────────────────────────────────
        bm = re.match(r'^[\-\*\+•]\s+(.*)', line)
        if bm:
            story += [x for x in flush_buffers() if x not in bullet_buffer]
            ordered_buffer and story.extend(flush_bullet(ordered_buffer, ordered=True)) and ordered_buffer.clear()
            bullet_buffer.append(bm.group(1))
            i += 1; continue

        # ── ordered list ─────────────────────────────────────────────────
        om = re.match(r'^\d+[\.\)]\s+(.*)', line)
        if om:
            if bullet_buffer:
                story += flush_bullet(bullet_buffer, ordered=False)
                bullet_buffer.clear()
            ordered_buffer.append(om.group(1))
            i += 1; continue

        # ── blank line ───────────────────────────────────────────────────
        if line.strip() == "":
            story += flush_buffers()
            story.append(Spacer(1, 4))
            i += 1; continue

        # ── normal paragraph ─────────────────────────────────────────────
        story += flush_buffers()
        clean = sanitize(line)
        if clean:
            story.append(Paragraph(clean, styles["body"]))
        i += 1

    story += flush_buffers()
    return story


# ─────────────────────────────────────────────
#  Cover-page canvas decorator
# ─────────────────────────────────────────────
class CoverCanvasDecorator:
    """Wraps ReportCanvas to paint a dark cover background on page 1."""

    def __init__(self, topic):
        self._topic = topic

    def __call__(self, filename, **kwargs):
        c = ReportCanvas(filename, topic=self._topic, **kwargs)
        return c


# ─────────────────────────────────────────────
#  Main PDF Generator class
# ─────────────────────────────────────────────
class PDFGenerator:

    # ------------------------------------------------------------------
    def _cover_background(self, canv, doc):
        """Paint dark cover background on page 1 only."""
        if doc.page == 1:
            canv.setFillColor(SLATE_900)
            canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

            # gradient bands (faked with rects)
            for idx, alpha in enumerate([0.07, 0.05, 0.03]):
                band_h = PAGE_H / 3
                canv.setFillColorRGB(0.388, 0.400, 0.945, alpha=alpha)
                canv.rect(0, PAGE_H - band_h * (idx + 1),
                          PAGE_W, band_h, fill=1, stroke=0)

            # bottom accent strip
            canv.setFillColor(INDIGO)
            canv.rect(0, 0, PAGE_W, 3, fill=1, stroke=0)

            # top-right decorative circle
            canv.setFillColorRGB(0.388, 0.400, 0.945, alpha=0.08)
            canv.circle(PAGE_W - 30 * mm, PAGE_H - 30 * mm, 60 * mm, fill=1, stroke=0)

    # ------------------------------------------------------------------
    def _later_background(self, canv, doc):
        """Slightly tinted background on content pages."""
        if doc.page > 1:
            canv.setFillColor(colors.HexColor("#0A0F1C"))
            canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # ------------------------------------------------------------------
    def _on_page(self, canv, doc):
        self._cover_background(canv, doc)
        self._later_background(canv, doc)

    # ------------------------------------------------------------------
    def _extract_sections(self, report_text: str) -> list:
        """
        Walk the markdown and collect H1/H2 headings for the TOC.
        Returns list of {"title": str, "subs": [str, ...]}
        """
        sections = []
        current = None
        for line in report_text.split("\n"):
            h2m = re.match(r'^##\s+(.*)', line.rstrip())
            h1m = re.match(r'^#\s+(.*)', line.rstrip())
            if h1m and not h2m:
                if current:
                    sections.append(current)
                current = {"title": h1m.group(1).strip(), "subs": []}
            elif h2m:
                if current is None:
                    current = {"title": "Overview", "subs": []}
                current["subs"].append(h2m.group(1).strip())
        if current:
            sections.append(current)
        return sections

    # ------------------------------------------------------------------
    def generate_pdf(self, topic: str, report_text: str, output_file=None) -> str:

        if output_file is None:
            safe = (topic.replace(" ", "_").replace(":", "")
                        .replace("/", "_").replace("\\", "_"))
            output_file = f"{safe}.pdf"

        styles  = build_styles()
        sections = self._extract_sections(report_text)

        # ── assemble story ─────────────────────────────────────────────
        story = []

        # 1. Cover
        story += build_cover(topic, styles)

        # 2. TOC  (only if we found headings)
        if sections:
            story += build_toc(sections, styles)

        # 3. Report body
        story += parse_report(report_text, styles)

        # 4. Back page
        story.append(PageBreak())
        story.append(Spacer(1, 80 * mm))
        story.append(HRFlowable(width="30%", thickness=2, color=INDIGO,
                                 hAlign="CENTER", spaceAfter=10, spaceBefore=0))
        story.append(Paragraph("End of Report", ParagraphStyle(
            "end", fontName="Helvetica", fontSize=9,
            textColor=SLATE_600, alignment=TA_CENTER)))
        story.append(Paragraph(
            f"Generated by <b>ResearchAI</b> &nbsp;|&nbsp; {datetime.now().strftime('%d %B %Y')}",
            ParagraphStyle("end2", fontName="Helvetica", fontSize=8,
                           textColor=SLATE_700, alignment=TA_CENTER, spaceBefore=4)))

        # ── build document ─────────────────────────────────────────────
        doc = SimpleDocTemplate(
            output_file,
            pagesize=A4,
            leftMargin=MARGIN_L,
            rightMargin=MARGIN_R,
            topMargin=MARGIN_T + 10 * mm,   # extra room for header bar
            bottomMargin=MARGIN_B + 8 * mm,
            title=topic,
            author="ResearchAI — Autonomous Research Intelligence",
            subject="Research Report",
            creator="ResearchAI",
        )

        # Use a canvas maker that knows the topic for header/footer
        topic_ref = topic

        class _Canvas(ReportCanvas):
            def __init__(self, filename, **kw):
                super().__init__(filename, topic=topic_ref, **kw)

        doc.build(
            story,
            onFirstPage=self._on_page,
            onLaterPages=self._on_page,
            canvasmaker=_Canvas,
        )

        return output_file