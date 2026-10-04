"""Gated catalog set (like the website's select-then-open flow):
  Sunita-Traders-Main.pdf     - cover, about, how-to, CHOOSE A CATEGORY, why, faq, contact
  Sunita-Traders-Carpets.pdf  - ST-C01..31 grids only (opens only when Carpets is tapped)
  Sunita-Traders-Doormats.pdf - ST-D01..14 grids only (opens only when Door Mats is tapped)
Buttons are file-links, so keep all 3 PDFs in the same folder when sharing.
Same website color pattern: cream pages, dark maroon cover/contact, gold accents.
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
PHONE = "+91 7976943373"
WA_LINK = "wa.me/917976943373"
ADDR = "Shop No. 228, Badi Choupad, Tripolia Bazar, Biseswarji, Jaipur 302002"
MAIN = "Sunita-Traders-Main.pdf"
FCARP = "Sunita-Traders-Carpets.pdf"
FMAT = "Sunita-Traders-Doormats.pdf"
LOGO_IMG = str(BASE / "images/logo-round.png")
LOGO_TAG = lambda s=110: f'<img src="{LOGO_IMG}" width="{s}" height="{s}"/>'
LOGO_P = ParagraphStyle("logo", alignment=TA_CENTER, spaceAfter=4, spaceBefore=0,
                         fontName="Helvetica", fontSize=10, leading=12)

MAROON = HexColor("#4A0E0E"); DARK = HexColor("#2A0707")
GOLD = HexColor("#C9A227"); GOLDLT = HexColor("#E9CE7A")
CREAM = HexColor("#FAF6EE"); WHITE = HexColor("#FFFFFF")
INK = HexColor("#241612"); MUTED = HexColor("#6F6259"); LINE = HexColor("#EADFC3")
CREAM_TXT = HexColor("#F3E6C8")
PW, PH = A4
LM = RM = 14 * mm; TM = 12 * mm; BM = 18 * mm


class CatalogDoc(BaseDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._bm_n = 0
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name.startswith("BMH"):
            key = f"bm-{self._bm_n}"
            self._bm_n += 1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=0, closed=0)


def _cream_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(CREAM); canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(1.2)
    canvas.line(LM, 15 * mm, PW - LM, 15 * mm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(MUTED)
    canvas.drawCentredString(PW / 2, 11 * mm, f"Sunita Traders • Since 1970 • {PHONE} • Page {doc.page}")
    canvas.restoreState()


def _dark_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK); canvas.rect(0, 0, PW, PH, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(2)
    canvas.line(LM, 15 * mm, PW - LM, 15 * mm)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GOLDLT)
    canvas.drawCentredString(PW / 2, 11 * mm, f"Sunita Traders • Since 1970 • {PHONE} • Page {doc.page}")
    canvas.restoreState()


def _new_doc(out):
    doc = CatalogDoc(str(out), pagesize=A4, leftMargin=LM, rightMargin=RM,
                     topMargin=TM, bottomMargin=BM, showBoundary=0,
                     title="Sunita Traders - Catalog (Since 1970)", author="Sunita Traders")
    fw = PW - LM - RM; fh = PH - TM - BM
    doc.addPageTemplates([
        PageTemplate(id="Dark", frames=[Frame(LM, BM, fw, fh)], onPage=_dark_page),
        PageTemplate(id="Cream", frames=[Frame(LM, BM, fw, fh)], onPage=_cream_page),
    ])
    return doc


def _styles():
    sKicker = ParagraphStyle("k", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=MAROON, alignment=TA_CENTER)
    sSub = ParagraphStyle("s", fontName="Helvetica", fontSize=11.5, leading=16, textColor=MUTED, alignment=TA_CENTER)
    sBody = ParagraphStyle("b", fontName="Helvetica", fontSize=10.5, leading=15, textColor=INK, alignment=TA_LEFT)
    sCap = ParagraphStyle("c", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=MAROON, alignment=TA_CENTER)
    sFoot = ParagraphStyle("f", fontName="Helvetica", fontSize=8, leading=10, textColor=MUTED, alignment=TA_CENTER)
    sBMH = ParagraphStyle("BMH", fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=MAROON, alignment=TA_LEFT)
    dKicker = ParagraphStyle("dk", parent=sKicker, textColor=GOLD)
    dTitle = ParagraphStyle("dt", fontName="Helvetica-Bold", fontSize=40, leading=44, textColor=WHITE, alignment=TA_CENTER)
    dSub = ParagraphStyle("ds", parent=sSub, textColor=CREAM_TXT)
    dBadge = ParagraphStyle("db", fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=GOLDLT, alignment=TA_CENTER)
    dPhone = ParagraphStyle("dp", parent=sSub, textColor=GOLDLT, fontSize=20)
    sBMHd = ParagraphStyle("BMHd", parent=dTitle, fontSize=32)
    return dict(sKicker=sKicker, sSub=sSub, sBody=sBody, sCap=sCap, sFoot=sFoot,
                sBMH=sBMH, dKicker=dKicker, dTitle=dTitle, dSub=dSub, dBadge=dBadge,
                dPhone=dPhone, sBMHd=sBMHd)


def _hrule(left=True):
    return HRFlowable(width="15%", thickness=3, color=GOLD, hAlign="LEFT" if left else "CENTER",
                       spaceAfter=4, spaceBefore=4)


def _cat_card(st, imgfile, title, sub, target_file, btn):
    thumb = Image(str(imgfile), width=80 * mm, height=58 * mm, kind="proportional")
    inner = Table([[thumb],
                   [Paragraph(f"<b>{title}</b>", ParagraphStyle("ct", parent=st["sBody"], fontSize=13, textColor=MAROON, alignment=TA_CENTER))],
                   [Paragraph(sub, ParagraphStyle("cb", parent=st["sBody"], fontSize=9.5, textColor=MUTED, alignment=TA_CENTER))],
                   [Paragraph(f'<a href="{target_file}" color="#E9CE7A"><b>{btn}</b></a>',
                              ParagraphStyle("cbtn", parent=st["sBody"], fontSize=12, textColor=GOLDLT, alignment=TA_CENTER))]],
                  colWidths=[86 * mm])
    inner.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                               ("BOX", (0, 0), (-1, -1), 1, GOLD),
                               ("BACKGROUND", (0, 3), (0, 3), MAROON),
                               ("TOPPADDING", (0, 3), (0, 3), 7), ("BOTTOMPADDING", (0, 3), (0, 3), 7),
                               ("TOPPADDING", (0, 0), (-1, 2), 4), ("BOTTOMPADDING", (0, 0), (-1, 2), 2)]))
    return inner


def build_main():
    st = _styles(); story = []
    story.append(Spacer(1, 12 * mm))
    story.append(Paragraph(LOGO_TAG(120), LOGO_P))
    story.append(Paragraph("TRIPOLIA BAZAR &nbsp;•&nbsp; JAIPUR &nbsp;•&nbsp; SINCE 1970", st["dKicker"]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("SUNITA TRADERS", st["dTitle"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("Carpets & Door Mats for <b>Home, Weddings & Events</b>",
                           ParagraphStyle("dsh", parent=st["dSub"], textColor=GOLDLT, fontSize=13)))
    story.append(HRFlowable(width="12%", thickness=2.2, color=GOLD, hAlign="CENTER", spaceAfter=4, spaceBefore=4))
    story.append(Paragraph("45+ ready-stock designs with honest pricing. Wedding red carpets,<br/>designer runners and anti-skid door mats — with all-India delivery.", st["dSub"]))
    story.append(Spacer(1, 6 * mm))
    badges = Table([[Paragraph("45+ designs<br/>in stock", st["dBadge"]), Paragraph("Retail at<br/>wholesale rates", st["dBadge"]),
                     Paragraph("Bulk event<br/>orders", st["dBadge"]), Paragraph("All-India<br/>delivery", st["dBadge"])]],
                   colWidths=[42 * mm] * 4)
    badges.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 1, GOLD), ("INNERGRID", (0, 0), (-1, -1), 0.5, GOLD),
                                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    story.append(badges)
    story.append(Spacer(1, 7 * mm))
    story.append(Paragraph(f"<b>{PHONE}</b>", st["dPhone"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(f"WhatsApp: {WA_LINK}<br/>{ADDR}<br/>Open Daily: 9 AM – 9 PM", st["dSub"]))

    story.append(NextPageTemplate("Cream")); story.append(PageBreak())
    story.append(Paragraph("ABOUT THE SHOP", ParagraphStyle("k2", parent=st["sKicker"], alignment=TA_LEFT)))
    story.append(Paragraph("A neighbourhood store with event-grade stock", st["sBMH"]))
    story.append(_hrule())
    story.append(Paragraph("Sunita Traders, Tripolia Bazar — serving customers <b>since 1970</b>, delivering <b>all over India</b>. Every photo in this catalog is from our own ready stock.", st["sBody"]))
    story.append(Spacer(1, 3 * mm))
    for b in ["<b>Wedding & event carpets</b> — classic reds, maroons, golds, runners by the metre",
              "<b>Home carpets</b> — floral, modern and traditional weaves",
              "<b>Door mats & runners</b> — anti-skid, washable, set shades",
              "<b>Bulk supply</b> — weddings, hotels, offices, exhibitions"]:
        story.append(Paragraph("• &nbsp;" + b, st["sBody"])); story.append(Spacer(1, 1.5 * mm))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("HOW TO ORDER ON WHATSAPP", ParagraphStyle("k3", parent=st["sKicker"], alignment=TA_LEFT)))
    story.append(Paragraph("3 easy steps", st["sBMH"]))
    story.append(_hrule())
    for i, b in enumerate(["<b>Note the design code</b> — like ST-C07 or ST-D03.",
                           f"<b>Choose a category below</b> — products open only after you select one.",
                           f"<b>Send the code on WhatsApp</b> to {PHONE} and get price & delivery time."], 1):
        story.append(Paragraph(f"<b>{i}.</b> &nbsp;{b}", st["sBody"])); story.append(Spacer(1, 1.5 * mm))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("FULL CATALOGUE", ParagraphStyle("k6", parent=st["sKicker"], alignment=TA_LEFT)))
    story.append(Paragraph("Choose a category", st["sBMH"]))
    story.append(_hrule())
    story.append(Paragraph("Tap a button — that category file opens. Nothing else is shown until you choose.",
                           ParagraphStyle("cs", parent=st["sBody"], textColor=MUTED)))
    story.append(Spacer(1, 4 * mm))
    story.append(Table([[ _cat_card(st, IMG_C[0], "Carpets — 31 Designs", "Wedding • Home • Event • Runners", FCARP, "Open Carpets →"),
                           _cat_card(st, IMG_D[0], "Door Mats — 14 Designs", "Anti-skid • Washable • Floral & striped", FMAT, "Open Door Mats →") ]],
                       colWidths=[88 * mm, 88 * mm], hAlign="CENTER",
                       style=TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                         ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)])))

    story.append(PageBreak())
    story.append(Paragraph("WHY BUY FROM US", ParagraphStyle("k4", parent=st["sKicker"], alignment=TA_LEFT)))
    story.append(Paragraph("Simple, honest retail", st["sBMH"]))
    story.append(_hrule())
    why = [[Paragraph("<b>True wholesale pricing</b><br/>No middlemen. Ask for event-lot rates.", st["sBody"]),
            Paragraph("<b>Ready stock</b><br/>45+ designs physically in shop.", st["sBody"])],
           [Paragraph("<b>WhatsApp ordering</b><br/>Send SKU screenshot, get price fast.", st["sBody"]),
            Paragraph("<b>All-India delivery</b><br/>Homes, weddings, hotels, offices.", st["sBody"])]]
    t = Table(why, colWidths=[85 * mm, 85 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), WHITE),
                           ("BOX", (0, 0), (-1, -1), 0.8, GOLD), ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    story.append(t)
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("GOOD TO KNOW", ParagraphStyle("k5", parent=st["sKicker"], alignment=TA_LEFT)))
    story.append(Paragraph("FAQs", st["sBMH"]))
    story.append(_hrule())
    for q, a in [("How do I order on WhatsApp?",
                  f"Choose a category, note the design code (e.g. ST-C07) and send it to {PHONE}."),
                 ("Do you sell carpet by the metre for events?",
                  "Yes. Wedding reds and runners in running lengths — share length × width for a quote."),
                 ("Do you deliver all over India?",
                  "Yes! All-India delivery by transport/courier on actuals. Jaipur same/next-day."),
                 ("Are colours exactly as in photos?",
                  "Photos are real stock; slight lot variation is normal. Visit the shop for exact shades.")]:
        story.append(Paragraph(f"<b>Q: {q}</b>", st["sBody"])); story.append(Spacer(1, 1 * mm))
        story.append(Paragraph(f"A: {a}", st["sBody"])); story.append(Spacer(1, 3 * mm))

    story.append(NextPageTemplate("Dark")); story.append(PageBreak())
    story.append(Spacer(1, 14 * mm))
    story.append(Paragraph(LOGO_TAG(100), LOGO_P))
    story.append(Paragraph("VISIT • CALL • WHATSAPP", st["dKicker"]))
    story.append(Paragraph("Sunita Traders", st["sBMHd"]))
    story.append(HRFlowable(width="12%", thickness=2.2, color=GOLD, hAlign="CENTER", spaceAfter=4, spaceBefore=4))
    story.append(Paragraph(ADDR, st["dSub"]))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(f"<b>{PHONE}</b>", st["dPhone"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(f"WhatsApp: {WA_LINK}<br/>Hours: Mon–Sun, 9:00 AM – 9:00 PM", st["dSub"]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Serving Since 1970 &nbsp;•&nbsp; All-India Delivery<br/>Thank You! 🙏 &nbsp;•&nbsp; © 2026 Sunita Traders", st["dSub"]))

    doc = _new_doc(BASE / MAIN)
    doc.build(story)
    print(f"Saved {MAIN}")


def build_products(out_name, files, prefix, title, sub, back_label):
    st = _styles(); story = []
    # header page (cream is second template; first page uses Dark by default -> switch first)
    story.append(NextPageTemplate("Cream"))
    story.append(Paragraph(LOGO_TAG(80), LOGO_P))
    story.append(Paragraph("FULL CATALOGUE", ParagraphStyle("pk", parent=st["sKicker"], alignment=TA_LEFT)))
    story.append(Paragraph(title, st["sBMH"]))
    story.append(_hrule())
    story.append(Paragraph(sub, ParagraphStyle("ps", parent=st["sBody"], textColor=MUTED)))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(f'<a href="{MAIN}" color="#4A0E0E">← Back to main catalog</a>',
                           ParagraphStyle("pb", parent=st["sBody"], fontSize=10, textColor=MAROON)))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(f"Tap any design, note its code, and send it on WhatsApp to {PHONE}.", st["sBody"]))
    for i in range(0, len(files), 4):
        chunk = files[i:i + 4]
        story.append(PageBreak())
        story.append(Paragraph(f"{title} ({i + 1}–{i + len(chunk)} of {len(files)})",
                               ParagraphStyle("cc", parent=st["sBody"], textColor=MUTED)))
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(f'<a href="{MAIN}" color="#4A0E0E">← Back to main catalog</a>',
                               ParagraphStyle("pb2", parent=st["sBody"], fontSize=9, textColor=MAROON)))
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
                    im = Paragraph("[photo]", st["sBody"])
                cell = Table([[im], [Paragraph(f"{code}<br/>{back_label}<br/>{PHONE}", st["sCap"])]],
                             colWidths=[85 * mm])
                cell.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                                          ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                                          ("BOX", (0, 0), (-1, -1), 0.8, GOLD)]))
                row.append(cell)
            while len(row) < 2:
                row.append(Paragraph("", st["sBody"]))
            rows.append(row)
        t = Table(rows, colWidths=[85 * mm, 85 * mm], hAlign="CENTER")
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        story.append(t)
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("Screenshot lekar WhatsApp par bhejein — price turant milega.", st["sFoot"]))
    doc = _new_doc(BASE / out_name)
    doc.build(story)
    print(f"Saved {out_name}")


if __name__ == "__main__":
    build_main()
    build_products(FCARP, IMG_C, "ST-C", "Carpets — 31 Designs",
                   "Wedding • Home • Event • Runners. Trusted since 1970.", "Carpet")
    build_products(FMAT, IMG_D, "ST-D", "Door Mats — 14 Designs",
                   "Anti-skid • Washable • Floral & striped. Trusted since 1970.", "Door Mat")
