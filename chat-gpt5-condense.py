# pip install reportlab pillow
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageOps
import os, math

# ======= CONFIG =======
INPUT_FOLDER   = "signatures"     # PNG/JPG/WEBP images go here
OUTPUT_PDF     = "all_signatures_packet.pdf"
PAGE_SIZE      = letter           # or A4
LANDSCAPE      = True             # True packs more per page on Letter/A4
MARGIN_INCH    = 0.5              # outer page margin
GUTTER_INCH    = 0.20             # spacing between cells (both directions)
TARGET_CELL_W  = 2.4              # target cell width (inches) — adjust to pack more/less
TARGET_CELL_H  = 1.2              # target cell height (inches)
DRAW_CELL_BOX  = False            # show faint boxes around cells
SHOW_CAPTION   = False            # print filename (minus extension) under signature
CAPTION_PT     = 9
ORDER_BY       = "name"           # "name" or "mtime"
# ======================

def list_images(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(
        (".png",".jpg",".jpeg",".webp",".bmp",".tif",".tiff"))]
    if ORDER_BY == "name":
        files.sort(key=lambda x: x.lower())
    elif ORDER_BY == "mtime":
        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    return [os.path.join(folder, f) for f in files]

def compute_grid(page_w, page_h, margin, gutter, target_w, target_h):
    # compute how many cells fit across/down given target cell size
    avail_w = page_w - 2*margin
    avail_h = page_h - 2*margin
    # include gutter between cells: N cells => N-1 gutters
    cols = max(1, int((avail_w + gutter) // (target_w + gutter)))
    rows = max(1, int((avail_h + gutter) // (target_h + gutter)))
    # recompute actual cell size to evenly distribute space (nice packing)
    cell_w = (avail_w - (cols-1)*gutter) / cols
    cell_h = (avail_h - (rows-1)*gutter) / rows
    return cols, rows, cell_w, cell_h

def fit_within(img_w, img_h, box_w, box_h, caption_h=0):
    # keep aspect; leave room for caption if present
    if caption_h:
        box_h = max(1, box_h - caption_h)
    scale = min(box_w / img_w, box_h / img_h)
    return img_w*scale, img_h*scale

def signature_name(path):
    base = os.path.splitext(os.path.basename(path))[0]
    return base.replace("_", " ").strip()

def load_image_pil(path):
    # Convert to RGB with white background if needed (handles transparency gracefully)
    im = Image.open(path)
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGBA", im.size, (255, 255, 255, 0))
        bg.paste(im, mask=im.split()[-1])
        im = bg.convert("RGB")  # flatten alpha onto white; ReportLab handles mask='auto' too, but PIL resizes nicer
    else:
        im = im.convert("RGB")
    # Trim extra whitespace-like borders (optional but helps consistency)
    im = ImageOps.exif_transpose(im)  # respect orientation
    im = ImageOps.expand(im, border=0)
    return im

def main():
    paths = list_images(INPUT_FOLDER)
    if not paths:
        raise SystemExit("No images found in the 'signatures' folder.")

    page = landscape(PAGE_SIZE) if LANDSCAPE else PAGE_SIZE
    page_w, page_h = page
    margin = MARGIN_INCH * inch
    gutter = GUTTER_INCH * inch
    target_w = TARGET_CELL_W * inch
    target_h = TARGET_CELL_H * inch

    cols, rows, cell_w, cell_h = compute_grid(page_w, page_h, margin, gutter, target_w, target_h)
    cells_per_page = cols * rows

    c = canvas.Canvas(OUTPUT_PDF, pagesize=page)
    c.setTitle("All Signatures Packet")

    for page_index in range(math.ceil(len(paths) / cells_per_page)):
        start = page_index * cells_per_page
        chunk = paths[start:start+cells_per_page]

        # draw each cell
        for idx, path in enumerate(chunk):
            r = idx // cols
            q = idx % cols
            # top-left origin -> we calculate from margins
            x = margin + q * (cell_w + gutter)
            # draw top-to-bottom rows
            y_top = page_h - margin - r * (cell_w*0 + cell_h + gutter)  # not using cell_w; just cell_h
            y = y_top - cell_h

            # optional cell box
            if DRAW_CELL_BOX:
                c.setLineWidth(0.25)
                c.setDash(3,2)
                c.rect(x, y, cell_w, cell_h)

            # caption reserved space
            caption_h = 0
            label = ""
            if SHOW_CAPTION:
                label = signature_name(path)
                caption_h = 0.22 * inch

            # load and size image
            try:
                im = load_image_pil(path)
                img_w, img_h = im.size
                fit_w, fit_h = fit_within(img_w, img_h, cell_w, cell_h, caption_h)
                # center within cell
                img_x = x + (cell_w - fit_w)/2
                img_y = y + (cell_h - caption_h - fit_h)/2 + caption_h
                c.drawInlineImage(im, img_x, img_y, width=fit_w, height=fit_h)
            except Exception as e:
                # fallback: show filename if image fails
                c.setFont("Helvetica-Oblique", 8)
                c.drawString(x+4, y+cell_h/2, f"[Unreadable: {os.path.basename(path)}]")

            # caption (if enabled)
            if SHOW_CAPTION and label:
                c.setFont("Helvetica", CAPTION_PT)
                text_w = c.stringWidth(label, "Helvetica", CAPTION_PT)
                c.drawString(x + (cell_w - text_w)/2, y + 2, label)

        c.showPage()

    c.save()
    print(f"Packed {len(paths)} signatures into {OUTPUT_PDF} using {rows}x{cols} grid ({cells_per_page}/page).")

if __name__ == "__main__":
    main()