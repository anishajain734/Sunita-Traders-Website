"""Catalog PDF in the website's exact color pattern:
cream (#FAF6EE) pages, dark maroon (#2A0707) cover + contact like the hero,
gold (#C9A227) rules/badges, white cards with gold borders.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Image, Table, TableStyle, PageBreak,
                                NextPageTemplate, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from pathlib import Path

BASE = Path("/mnt/c/Users/deepak jain/projects/sunita-traders")
IMG_C = sorted((BASE / "images/carpets").glob("*.jpg"))
IMG_D = sorted((BASE / "images/doormats").glob("*.jpg"))
OUT = BASE / "Sunita-Traders-Catalog.pdf"
PHONE = "+91 7976943373"
WA_LINK = "wa.me/917976943373"
ADDR = "Shop No. 228, Badi Choupad, Tripolia Bazar, Biseswarji, Jaipur 302002"

# --- website palette ---
MAROON = HexColor("#4A0E0E"); DARK = HexColor("#2A0707")
GOLD = HexColor("#C9A227"); GOLDLT = HexColor("#E9CE7A")
CREAM = HexColor("#FAF6EE"); WHITE = HexColor("#FFFFFF")
INK = HexColor("#241612"); MUTED = HexColor("#6F6259"); LINE = HexColor("#EADFC3")
CREAM_TXT = HexColor("#F3E6C8")
PW, PH = A4
LM = RM = 14 * mm; TM = 12 * mm; BM = 18 * mm

def draw_cream(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM)
    canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(1.2)
    canvas.line(LM, 15 * mm, PW - LM, 15 * mm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(MUTED)
    canvas.drawCentredString(PW / 2, 11 * mm,
        f"Sunita Traders • Since 1970 • {ADDR} • {PHONE} • Page {doc.page}")
    canvas.restoreState()

def draw_dark(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(2)
    canvas.line(LM, 15 * mm, PW - LM, 15 * mm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GOLDLT)
    canvas.drawCentredString(PW / 2, 11 * mm,
        f"Sunita Traders • Since 1970 • {PHONE} • Page {doc.page}")
    canvas.restoreState()


COVER_IMG = BASE / "images/doormats/doormat-01.jpg"  # clean, watermark-free photo
LOGO_IMG = str(BASE / "images/logo-round.png")
LOGO_TAG = lambda s=110: f'<img src="{LOGO_IMG}" width="{s}" height="{s}"/>'
LOGO_P = ParagraphStyle("logo", alignment=TA_CENTER, spaceAfter=4, spaceBefore=0,
                         fontName="Helvetica", fontSize=10, leading=12)

def draw_cover(canvas, doc):
    # full-bleed carpet photo (like the website hero) + dark overlay
    canvas.saveState()
    try:
        from PIL import Image as PILImage
        iw, ih = PILImage.open(COVER_IMG).size
        scale = max(PW / iw, PH / ih)
        w, h = iw * scale, ih * scale
        canvas.drawImage(str(COVER_IMG), (PW - w) / 2, (PH - h) / 2,
                         width=w, height=h, preserveAspectRatio=False, mask="auto")
    except Exception:
        canvas.setFillColor(DARK)
        canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.setFillColor(DARK)
    canvas.setFillAlpha(0.84)
    canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.restoreState()
    canvas.saveState()
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(2)
    canvas.line(LM, 15 * mm, PW - LM, 15 * mm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GOLDLT)
    canvas.drawCentredString(PW / 2, 11 * mm,
        f"Sunita Traders • Since 1970 • {PHONE} • Page {doc.page}")
    canvas.restoreState()

class CatalogDoc(BaseDocTemplate):
    """Adds PDF sidebar bookmarks for every section heading."""
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._bm_n = 0
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name.startswith("BMH"):
            key = f"bm-{self._bm_n}"
            self._bm_n += 1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=0, closed=0)

doc = CatalogDoc(str(OUT), pagesize=A4, leftMargin=LM, rightMargin=RM,
                      topMargin=TM, bottomMargin=BM, showBoundary=0,
                      title="Sunita Traders - Catalog (Since 1970)", author="Sunita Traders")
fw = PW - LM - RM; fh = PH - TM - BM
doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[Frame(LM, BM, fw, fh)], onPage=draw_cover),
    PageTemplate(id="Dark", frames=[Frame(LM, BM, fw, fh)], onPage=draw_dark),
    PageTemplate(id="Cream", frames=[Frame(LM, BM, fw, fh)], onPage=draw_cream),
])

# cream-page styles (site sections)
sTitle = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=40, leading=44, textColor=MAROON, alignment=TA_CENTER)
sKicker = ParagraphStyle("k", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=MAROON, alignment=TA_CENTER)
sSub = ParagraphStyle("s", fontName="Helvetica", fontSize=11.5, leading=16, textColor=MUTED, alignment=TA_CENTER)
sH = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=MAROON, alignment=TA_LEFT)
sBMH = ParagraphStyle("BMH", parent=sH)  # bookmarked section heading (cream pages)
sBody = ParagraphStyle("b", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK, alignment=TA_LEFT)
sCap = ParagraphStyle("c", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=MAROON, alignment=TA_CENTER)
sFoot = ParagraphStyle("f", fontName="Helvetica", fontSize=8, leading=10, textColor=MUTED, alignment=TA_CENTER)
sBadge = ParagraphStyle("bd", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=MAROON, alignment=TA_CENTER)
# dark-page styles (hero / contact)
dKicker = ParagraphStyle("dk", parent=sKicker, textColor=GOLD)
dTitle = ParagraphStyle("dt", parent=sTitle, textColor=WHITE)
dTitleG = ParagraphStyle("dtg", parent=sTitle, textColor=GOLDLT, fontSize=40)
dSub = ParagraphStyle("ds", parent=sSub, textColor=CREAM_TXT)
dBadge = ParagraphStyle("db", parent=sBadge, textColor=GOLDLT)
dPhone = ParagraphStyle("dp", parent=sSub, textColor=GOLDLT, fontSize=20)
sBMHd = ParagraphStyle("BMHd", parent=dTitle, fontSize=32)  # bookmarked title (dark pages)

def gold_rule():
    return HRFlowable(width="12%", thickness=2.2, color=GOLD, spaceAfter=4, spaceBefore=4,
                       hAlign="CENTER", vAlign="BOTTOM", dash=None)

story = []

# ---------- COVER (dark, like hero) ----------
story.append(Spacer(1, 12 * mm))
story.append(Paragraph(LOGO_TAG(120), LOGO_P))
story.append(Paragraph("TRIPOLIA BAZAR &nbsp;•&nbsp; JAIPUR &nbsp;•&nbsp; SINCE 1970", dKicker))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph("SUNITA TRADERS", dTitle))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph("Carpets & Door Mats for <b>Home, Weddings & Events</b>", ParagraphStyle("dsh", parent=dSub, textColor=GOLDLT, fontSize=13)))
story.append(gold_rule())
story.append(Paragraph("45+ ready-stock designs with honest pricing. Wedding red carpets,<br/>designer runners and anti-skid door mats — with all-India delivery.", dSub))
story.append(Spacer(1, 6 * mm))
badges = Table([[Paragraph("45+ designs<br/>in stock", dBadge), Paragraph("Retail at<br/>wholesale rates", dBadge),
                 Paragraph("Bulk event<br/>orders", dBadge), Paragraph("All-India<br/>delivery", dBadge)]],
               colWidths=[42 * mm] * 4)
badges.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, GOLD), ("INNERGRID", (0, 0), (-1, -1), 0.5, GOLD),
                            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
story.append(badges)
story.append(Spacer(1, 7 * mm))
story.append(Paragraph(f"<b>{PHONE}</b>", dPhone))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph(f"WhatsApp: {WA_LINK}<br/>{ADDR}<br/>Open Daily: 9 AM – 9 PM", dSub))

# ---------- switch to cream ----------
story.append(NextPageTemplate("Cream"))
story.append(PageBreak())

story.append(Paragraph("ABOUT THE SHOP", ParagraphStyle("k2", parent=sKicker, alignment=TA_LEFT)))
story.append(Paragraph("A neighbourhood store with event-grade stock", sBMH))
story.append(HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=4, spaceBefore=4))
story.append(Paragraph("Sunita Traders, Tripolia Bazar — serving customers <b>since 1970</b>, delivering <b>all over India</b>. Every photo in this catalog is from our own ready stock. What you see is what you get.", sBody))
story.append(Spacer(1, 3 * mm))
for b in ["<b>Wedding & event carpets</b> — classic reds, maroons, golds, runners by the metre",
          "<b>Home carpets</b> — floral, modern and traditional weaves",
          "<b>Door mats & runners</b> — anti-skid, washable, set shades",
          "<b>Bulk supply</b> — weddings, hotels, offices, exhibitions"]:
    story.append(Paragraph("• &nbsp;" + b, sBody)); story.append(Spacer(1, 1.5 * mm))
story.append(Spacer(1, 3 * mm))
# hours box like .hours (beige #F6EDD3 -> use LINE-tinted box)
hours = Table([[Paragraph(f"<b>Visit us:</b> {ADDR}<br/><b>Hours:</b> Mon–Sun, 9:00 AM – 9:00 PM &nbsp;•&nbsp; <b>Phone:</b> {PHONE}", sBody)]],
              colWidths=[fw - 4 * mm])
hours.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HexColor("#F6EDD3")),
                           ("BOX", (0, 0), (-1, -1), 0.8, LINE),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
story.append(hours)
story.append(Spacer(1, 5 * mm))

story.append(Paragraph("HOW TO ORDER ON WHATSAPP", ParagraphStyle("k3", parent=sKicker, alignment=TA_LEFT)))
story.append(Paragraph("3 easy steps", sBMH))
story.append(HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=4, spaceBefore=4))
for i, b in enumerate(["<b>Note the design code</b> — every design has a code like ST-C07 or ST-D03.",
                       f"<b>Send it on WhatsApp</b> to {PHONE} (screenshot works too).",
                       "<b>Get price & delivery time</b> — Jaipur same/next-day, all-India by transport/courier."], 1):
    story.append(Paragraph(f"<b>{i}.</b> &nbsp;{b}", sBody)); story.append(Spacer(1, 1.5 * mm))

# ---------- CATEGORY CHOOSER (mirrors index.html #collection) ----------
story.append(Spacer(1, 5 * mm))
story.append(Paragraph("FULL CATALOGUE", ParagraphStyle("k6", parent=sKicker, alignment=TA_LEFT)))
story.append(Paragraph('<a name="sec-choose"/>Choose a category', sBMH))
story.append(HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=4, spaceBefore=4))
story.append(Paragraph("Tap a button below to jump straight to that section.", ParagraphStyle("cs", parent=sBody, textColor=MUTED)))
story.append(Spacer(1, 4 * mm))

def _cat_card(imgfile, title, sub, dest, btn):
    thumb = Image(str(imgfile), width=80 * mm, height=58 * mm, kind="proportional")
    inner = Table([[thumb],
                   [Paragraph(f"<b>{title}</b>", ParagraphStyle("ct", parent=sBody, fontSize=13, textColor=MAROON, alignment=TA_CENTER))],
                   [Paragraph(sub, ParagraphStyle("cb", parent=sBody, fontSize=9.5, textColor=MUTED, alignment=TA_CENTER))],
                   [Paragraph(f'<a href="#{dest}" color="#E9CE7A"><b>{btn}</b></a>',
                              ParagraphStyle("cbtn", parent=sBody, fontSize=12, textColor=GOLDLT, alignment=TA_CENTER))]],
                  colWidths=[86 * mm])
    inner.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                               ("BOX", (0, 0), (-1, -1), 1, GOLD),
                               ("BACKGROUND", (0, 3), (0, 3), MAROON),
                               ("TOPPADDING", (0, 3), (0, 3), 7), ("BOTTOMPADDING", (0, 3), (0, 3), 7),
                               ("TOPPADDING", (0, 0), (-1, 2), 4), ("BOTTOMPADDING", (0, 0), (-1, 2), 2)]))
    return inner

story.append(Table([[ _cat_card(IMG_C[0], "Carpets — 31 Designs", "Wedding • Home • Event • Runners",
                                "sec-carpets", "Open Carpets →"),
                       _cat_card(IMG_D[0], "Door Mats — 14 Designs", "Anti-skid • Washable • Floral & striped",
                                "sec-mats", "Open Door Mats →") ]],
                   colWidths=[88 * mm, 88 * mm], hAlign="CENTER",
                   style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                     ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)])))

def section_header(kicker, title, sub, anchor):
    story.append(PageBreak())
    story.append(Paragraph(kicker, ParagraphStyle("sk", parent=sKicker, alignment=TA_LEFT)))
    story.append(Paragraph(f'<a name="{anchor}"/>' + title, sBMH))
    story.append(HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=4, spaceBefore=4))
    story.append(Paragraph(sub, ParagraphStyle("ss", parent=sBody, textColor=MUTED)))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph('<a href="#sec-choose" color="#4A0E0E">← Back to categories</a>',
                           ParagraphStyle("bk", parent=sBody, fontSize=10, textColor=MAROON)))
    story.append(Spacer(1, 3 * mm))

def grid_pages(files, prefix, catlabel):
    for i in range(0, len(files), 4):
        chunk = files[i:i + 4]
        if i > 0:
            story.append(PageBreak())
            story.append(Paragraph(f"{catlabel} (continued — {i + 1}–{i + len(chunk)} of {len(files)})",
                                   ParagraphStyle("cc", parent=sBody, textColor=MUTED)))
            story.append(Spacer(1, 3 * mm))
        rows = []
        for r in range(0, len(chunk), 2):
            row = []
            for c in chunk[r:r + 2]:
                n = files.index(c) + 1
                code = f"{prefix}-{n:02d}"
                try:
                    im = Image(str(c), width=82 * mm, height=62 * mm, kind="proportional")
                except Exception:
                    im = Paragraph("[photo]", sBody)
                cell = Table([[im], [Paragraph(f"{code}<br/>{catlabel}<br/>{PHONE}", sCap)]],
                             colWidths=[85 * mm])
                cell.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                          ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                                          ("BOX", (0, 0), (-1, -1), 0.8, GOLD)]))
                row.append(cell)
            while len(row) < 2:
                row.append(Paragraph("", sBody))
            rows.append(row)
        t = Table(rows, colWidths=[85 * mm, 85 * mm], hAlign="CENTER")
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        story.append(t)
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("Screenshot lekar WhatsApp par bhejein — price turant milega.", sFoot))

section_header("FULL CATALOGUE — CATEGORY 1", "Carpets — 31 Designs",
               "Wedding • Home • Event • Runners. Trusted since 1970.", "sec-carpets")
grid_pages(IMG_C, "ST-C", "Carpet")
section_header("FULL CATALOGUE — CATEGORY 2", "Door Mats — 14 Designs",
               "Anti-skid • Washable • Floral & striped. Trusted since 1970.", "sec-mats")
grid_pages(IMG_D, "ST-D", "Door Mat")

story.append(PageBreak())
story.append(Paragraph("WHY BUY FROM US", ParagraphStyle("k4", parent=sKicker, alignment=TA_LEFT)))
story.append(Paragraph("Simple, honest retail", sBMH))
story.append(HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=4, spaceBefore=4))
why = [[Paragraph("<b>True wholesale pricing</b><br/>No middlemen. Ask for event-lot rates.", sBody),
        Paragraph("<b>Ready stock</b><br/>45+ designs physically in shop.", sBody)],
       [Paragraph("<b>WhatsApp ordering</b><br/>Send SKU screenshot, get price fast.", sBody),
        Paragraph("<b>All-India delivery</b><br/>Homes, weddings, hotels, offices.", sBody)]]
t = Table(why, colWidths=[85 * mm, 85 * mm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), WHITE),
                       ("BOX", (0, 0), (-1, -1), 0.8, GOLD), ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                       ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                       ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
story.append(t)
story.append(Spacer(1, 6 * mm))

story.append(Paragraph("GOOD TO KNOW", ParagraphStyle("k5", parent=sKicker, alignment=TA_LEFT)))
story.append(Paragraph("FAQs", sBMH))
story.append(HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT", spaceAfter=4, spaceBefore=4))
for q, a in [("How do I order on WhatsApp?",
              f"Note the design code (e.g. ST-C07) and send it to {PHONE} — we reply with price and delivery time."),
             ("Do you sell carpet by the metre for events?",
              "Yes. Wedding reds and runners are available in running lengths. Share length × width for a quote."),
             ("Do you deliver all over India?",
              "Yes! We deliver all over India by transport/courier on actual charges. Jaipur gets same/next-day delivery."),
             ("Are colours exactly as in photos?",
              "Photos are real stock; slight lot variation is normal in textiles. Visit the shop for exact shade matching.")]:
    story.append(Paragraph(f"<b>Q: {q}</b>", sBody)); story.append(Spacer(1, 1 * mm))
    story.append(Paragraph(f"A: {a}", sBody)); story.append(Spacer(1, 3 * mm))

# ---------- CONTACT (dark, like .contact box) ----------
story.append(NextPageTemplate("Dark"))
story.append(PageBreak())
story.append(Spacer(1, 14 * mm))
story.append(Paragraph(LOGO_TAG(100), LOGO_P))
story.append(Paragraph("VISIT • CALL • WHATSAPP", dKicker))
story.append(Paragraph("Sunita Traders", sBMHd))
story.append(gold_rule())
story.append(Paragraph(ADDR, dSub))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph(f"<b>{PHONE}</b>", dPhone))
story.append(Spacer(1, 2 * mm))
story.append(Paragraph(f"WhatsApp: {WA_LINK}<br/>Hours: Mon–Sun, 9:00 AM – 9:00 PM", dSub))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph("Serving Since 1970 &nbsp;•&nbsp; All-India Delivery<br/>Thank You! 🙏 &nbsp;•&nbsp; © 2026 Sunita Traders", dSub))

doc.build(story)
print(f"Saved {OUT} — {OUT.stat().st_size / 1024 / 1024:.1f} MB, carpets={len(IMG_C)}, mats={len(IMG_D)}")
