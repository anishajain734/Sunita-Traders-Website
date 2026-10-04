"""PPT version of sunita-traders-presentation.html:
cover > about > carpets header + grids > doormats header + grids > contact.
Website colors: maroon/gold/cream. Logo, Since 1970, All-India delivery.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from pathlib import Path

BASE = Path("/mnt/c/Users/deepak jain/projects/sunita-traders")
IMG_C = sorted((BASE / "images/carpets").glob("*.jpg"))
IMG_D = sorted((BASE / "images/doormats").glob("*.jpg"))
LOGO = BASE / "images/logo-round.png"
OUT = BASE / "Sunita-Traders-Presentation-v2.pptx"
PHONE = "+91 7976943373"
ADDR = "Shop No. 228, Badi Choupad, Tripolia Bazar, Biseswarji, Jaipur 302002"

DARK = RGBColor(0x2A, 0x07, 0x07)
MAROON = RGBColor(0x4A, 0x0E, 0x0E)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
GOLDLT = RGBColor(0xE9, 0xCE, 0x7A)
CREAM = RGBColor(0xFA, 0xF6, 0xEE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAMTXT = RGBColor(0xF3, 0xE6, 0xC8)
MUTED = RGBColor(0x6F, 0x62, 0x59)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def tb(slide, l, t, w, h, text, size=18, bold=False, color=MAROON, align=PP_ALIGN.LEFT):
    tx = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = "Calibri"
    p.alignment = align
    return tx


def footer(slide, dark=True):
    c = GOLDLT if dark else MUTED
    tb(slide, 0.3, 7.05, 12.73, 0.35,
       f"Sunita Traders • Since 1970 • {ADDR} • {PHONE}",
       size=10, bold=False, color=c, align=PP_ALIGN.CENTER)


def gold_rule(slide, t, color=GOLD):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.15), Inches(t), Inches(1.03), Pt(4))
    shp.fill.solid(); shp.fill.fore_color.rgb = color; shp.line.fill.background()
    return shp


def link_run_to_slide(run, target_slide):
    """Make a text run jump to another slide when clicked in Slide Show."""
    rId = run.part.relate_to(target_slide.part, RT.SLIDE)
    hlink = parse_xml(
        '<a:hlinkClick %s r:id="%s" action="ppaction://hlinksldjump"/>' % (nsdecls("a", "r"), rId))
    run._r.get_or_add_rPr().append(hlink)


def link_box(slide, l, t, w, h, text, size, color, target, align=PP_ALIGN.CENTER, bold=True):
    """Text box whose text jumps to target_slide on click. Returns the run."""
    tx = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    link_run_to_slide(run, target)
    return run


# ---------- COVER ----------
s = prs.slides.add_slide(blank)
bg(s, DARK)
s.shapes.add_picture(str(LOGO), Inches(6.06), Inches(0.35), Inches(1.2), Inches(1.2))
tb(s, 1, 1.7, 11.33, 0.45, "TRIPOLIA BAZAR  •  JAIPUR  •  SINCE 1970", 13, True, GOLD, PP_ALIGN.CENTER)
tb(s, 1, 2.15, 11.33, 1.0, "SUNITA TRADERS", 54, True, WHITE, PP_ALIGN.CENTER)
tb(s, 1, 3.1, 11.33, 0.5, "Premium Carpets & Door Mats — Retail Shop", 20, False, GOLDLT, PP_ALIGN.CENTER)
gold_rule(s, 3.7)
tb(s, 1, 3.95, 11.33, 0.55, f"{len(IMG_C)} Carpet Designs  •  {len(IMG_D)} Door Mat Designs  •  Ready Stock",
   15, True, WHITE, PP_ALIGN.CENTER)
tb(s, 1, 4.6, 11.33, 0.6, f"📞 {PHONE}", 26, True, GOLDLT, PP_ALIGN.CENTER)
tb(s, 1, 5.3, 11.33, 0.5, ADDR, 12, False, CREAMTXT, PP_ALIGN.CENTER)
tb(s, 1, 5.85, 11.33, 0.45, "Best Price  •  Genuine Quality  •  All-India Delivery", 13, True, GOLD, PP_ALIGN.CENTER)
footer(s, True)

# ---------- ABOUT ----------
s = prs.slides.add_slide(blank)
bg(s, CREAM)
tb(s, 0.6, 0.25, 12.1, 0.45, "ABOUT THE SHOP", 13, True, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 0.7, 12.1, 0.8, "A neighbourhood store with event-grade stock", 30, True, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 1.7, 6.0, 4.6,
   "•  Serving customers since 1970, delivering all over India\n"
   "•  Wedding / event red carpets & designer prints\n"
   "•  Home carpets, floral & modern weaves\n"
   "•  Anti-skid, washable door mats\n"
   "•  Bulk orders: weddings, hotels, offices\n"
   f"•  WhatsApp your SKU screenshot to {PHONE}\n\n"
   "Open Daily: 9 AM – 9 PM", 15, False, MAROON, PP_ALIGN.LEFT)
s.shapes.add_picture(str(IMG_C[0]), Inches(7.3), Inches(1.7), Inches(2.55), Inches(2.9))
s.shapes.add_picture(str(IMG_D[0]), Inches(10.1), Inches(1.7), Inches(2.55), Inches(2.9))
tb(s, 7.3, 4.75, 5.33, 0.4, "Real ready-stock photos", 12, True, MAROON, PP_ALIGN.CENTER)
footer(s, False)

# ---------- HOW TO ORDER ----------
s = prs.slides.add_slide(blank)
bg(s, CREAM)
tb(s, 0.6, 0.25, 12.1, 0.45, "HOW TO ORDER ON WHATSAPP", 13, True, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 0.7, 12.1, 0.8, "3 easy steps", 30, True, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 1.8, 12.1, 3.5,
   "1.   Choose a category — Carpets or Door Mats (next slide: tap a button to jump)\n"
   "2.   Note the design code — e.g. ST-C07 or ST-D03\n"
   f"3.   Send it on WhatsApp to {PHONE} — get price & delivery time", 18, False, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 4.6, 12.1, 0.6, "Jaipur same / next-day  •  All-India by transport / courier", 15, True, MAROON, PP_ALIGN.LEFT)
footer(s, False)


# ---------- CHOOSE A CATEGORY (tappable buttons) ----------
cs = prs.slides.add_slide(blank)
bg(cs, CREAM)
tb(cs, 0.6, 0.25, 12.1, 0.45, "FULL CATALOGUE", 13, True, MAROON, PP_ALIGN.LEFT)
tb(cs, 0.6, 0.7, 12.1, 0.8, "Choose a category", 30, True, MAROON, PP_ALIGN.LEFT)
tb(cs, 0.6, 1.5, 12.1, 0.4, "Tap a button — that section opens. (Links work in Slide Show ▶)",
   14, False, MAROON, PP_ALIGN.LEFT)


def cat_card(l, imgfile, title, sub, btn_text):
    card = cs.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               Inches(l), Inches(2.05), Inches(5.9), Inches(4.6))
    card.fill.solid(); card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = GOLD; card.line.width = Pt(2)
    cs.shapes.add_picture(str(imgfile), Inches(l + 0.25), Inches(2.3), Inches(5.4), Inches(2.3))
    tb(cs, l + 0.25, 4.7, 5.4, 0.45, title, 17, True, MAROON, PP_ALIGN.CENTER)
    tb(cs, l + 0.25, 5.15, 5.4, 0.35, sub, 12, False, MAROON, PP_ALIGN.CENTER)
    btn = cs.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                              Inches(l + 1.55), Inches(5.6), Inches(2.8), Inches(0.6))
    btn.fill.solid(); btn.fill.fore_color.rgb = MAROON; btn.line.fill.background()
    tf = btn.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = btn_text
    run.font.size = Pt(14); run.font.bold = True
    run.font.color.rgb = GOLDLT; run.font.name = "Calibri"
    return run


run_carpets = cat_card(0.45, IMG_C[0], f"Carpets — {len(IMG_C)} Designs",
                       "Wedding • Home • Event", "Open Carpets  →")
run_mats = cat_card(6.98, IMG_D[0], f"Door Mats — {len(IMG_D)} Designs",
                    "Anti-skid • Washable", "Open Door Mats  →")
footer(cs, False)


def section_head(kicker, title, sub, back_slide):
    s = prs.slides.add_slide(blank)
    bg(s, DARK)
    s.shapes.add_picture(str(LOGO), Inches(6.26), Inches(0.55), Inches(0.8), Inches(0.8))
    tb(s, 1, 1.5, 11.33, 0.5, kicker, 14, True, GOLD, PP_ALIGN.CENTER)
    tb(s, 1, 2.05, 11.33, 1.1, title, 44, True, WHITE, PP_ALIGN.CENTER)
    gold_rule(s, 3.25)
    tb(s, 1, 3.5, 11.33, 0.6, sub, 16, False, GOLDLT, PP_ALIGN.CENTER)
    tb(s, 1, 4.5, 11.33, 0.55, "Screenshot lekar WhatsApp par bhejein — price turant milega",
       14, False, CREAMTXT, PP_ALIGN.CENTER)
    link_box(s, 1, 5.5, 11.33, 0.5, "← Back to categories", 14, GOLDLT, back_slide)
    footer(s, True)
    return s


def grid_slides(files, prefix, catlabel, section):
    for idx in range(0, len(files), 4):
        chunk = files[idx:idx + 4]
        s = prs.slides.add_slide(blank)
        bg(s, CREAM)
        tb(s, 0.5, 0.15, 12.33, 0.55, f"{section}  ({idx + 1}–{idx + len(chunk)} of {len(files)})",
           17, True, MAROON, PP_ALIGN.LEFT)
        pos = [(0.5, 0.95), (6.92, 0.95), (0.5, 4.0), (6.92, 4.0)]
        for img, (l, t) in zip(chunk, pos):
            s.shapes.add_picture(str(img), Inches(l), Inches(t), Inches(5.91), Inches(2.45))
            n = files.index(img) + 1
            tb(s, l, t + 2.5, 5.91, 0.4, f"{prefix}-{n:02d}   •   {catlabel}   •   {PHONE}",
               11, True, MAROON, PP_ALIGN.CENTER)
        footer(s, False)


carpets_head = section_head("FULL CATALOGUE — CATEGORY 1", "CARPETS",
             f"{len(IMG_C)} Designs  •  Wedding / Home / Event  •  Trusted since 1970", cs)
grid_slides(IMG_C, "ST-C", "Carpet", "Carpets")
mats_head = section_head("FULL CATALOGUE — CATEGORY 2", "DOOR MATS",
             f"{len(IMG_D)} Designs  •  Anti-skid • Washable  •  Trusted since 1970", cs)
grid_slides(IMG_D, "ST-D", "Door Mat", "Door Mats")
link_run_to_slide(run_carpets, carpets_head)
link_run_to_slide(run_mats, mats_head)

# ---------- WHY US + FAQ ----------
s = prs.slides.add_slide(blank)
bg(s, CREAM)
tb(s, 0.6, 0.25, 12.1, 0.45, "WHY BUY FROM US  •  GOOD TO KNOW", 13, True, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 0.7, 12.1, 0.8, "Simple, honest retail", 30, True, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 1.7, 5.9, 2.6,
   "◈  True wholesale pricing — no middlemen\n"
   "▣  Ready stock — 45+ designs in shop\n"
   "✆  WhatsApp ordering — send SKU photo\n"
   "⬣  All-India delivery — homes & events", 15, False, MAROON, PP_ALIGN.LEFT)
tb(s, 6.8, 1.7, 5.9, 2.6,
   "Q: Carpet by the metre for events?\nA: Yes — share length × width.\n\n"
   "Q: All-India delivery?\nA: Yes, transport/courier on actuals.\n\n"
   "Q: Exact colours?\nA: Real-stock photos; slight lot variation.", 13, False, MAROON, PP_ALIGN.LEFT)
tb(s, 0.6, 5.2, 12.1, 0.6, "Open Daily 9 AM – 9 PM  •  Serving Since 1970", 15, True, MAROON, PP_ALIGN.CENTER)
footer(s, False)

# ---------- CONTACT ----------
s = prs.slides.add_slide(blank)
bg(s, DARK)
s.shapes.add_picture(str(LOGO), Inches(6.06), Inches(0.6), Inches(1.2), Inches(1.2))
tb(s, 1, 1.95, 11.33, 0.45, "VISIT  •  CALL  •  WHATSAPP", 13, True, GOLD, PP_ALIGN.CENTER)
tb(s, 1, 2.4, 11.33, 0.9, "Sunita Traders", 44, True, WHITE, PP_ALIGN.CENTER)
gold_rule(s, 3.4)
tb(s, 1, 3.65, 11.33, 0.5, ADDR, 14, False, CREAMTXT, PP_ALIGN.CENTER)
tb(s, 1, 4.35, 11.33, 0.7, f"📞  {PHONE}", 32, True, GOLDLT, PP_ALIGN.CENTER)
tb(s, 1, 5.2, 11.33, 0.5, "WhatsApp: wa.me/917976943373  •  Hours: Mon–Sun, 9 AM – 9 PM",
   14, False, CREAMTXT, PP_ALIGN.CENTER)
tb(s, 1, 5.95, 11.33, 0.45, "Serving Since 1970  •  All-India Delivery  •  Thank You! 🙏",
   13, True, GOLD, PP_ALIGN.CENTER)
footer(s, True)

prs.save(OUT)
print(f"Saved {OUT} — {OUT.stat().st_size / 1024 / 1024:.1f} MB, slides: {len(prs.slides._sldIdLst)}")
