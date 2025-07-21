import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, green, blue, black, yellow, lightgrey, darkblue
from reportlab.lib.units import inch

explanations = {
    "SQL Injection": "SQL Injection occurs when input is improperly sanitized, allowing attackers to execute SQL commands.",
    "XSS": "Cross-site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by others.",
    "Path Traversal": "Path Traversal exploits allow attackers to access files outside the web root directory.",
    "Directory Listing": "If enabled, it exposes all files in a directory, aiding attackers in reconnaissance."
}

def draw_section(c, y, title):
    c.setFillColor(lightgrey)
    c.rect(40, y - 5, 520, 20, fill=1, stroke=0)
    c.setFillColor(darkblue)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, title)
    return y - 25

def draw_text(c, y, msg, level):
    col = {'info': blue, 'error': red, 'warning': yellow}.get(level, black)
    c.setFont("Helvetica", 10)
    c.setFillColor(col)
    c.drawString(60, y, f"[{level.upper()}] {msg}")
    return y - 15

def generate_pdf(data, path, logo_path=None):
    c = canvas.Canvas(path, pagesize=letter)
    w, h = letter
    y = h - inch

    if logo_path and os.path.exists(logo_path):
        c.drawImage(logo_path, 400, y, width=150, height=40, mask='auto')
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(green)
    c.drawString(50, y, "Vulnerability Scan Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.setFillColor(black)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, y, f"Scan Timestamp: {timestamp}")
    y -= 30

    for section, findings in data.items():
        title = section.replace('_', ' ').title()
        y = draw_section(c, y, title)
        if title in explanations:
            c.setFont("Helvetica-Oblique", 9)
            c.setFillColor(black)
            c.drawString(60, y, "ℹ " + explanations[title])
            y -= 15
        for level, msg in findings:
            if y < 80:
                c.showPage()
                y = h - inch
            y = draw_text(c, y, msg, level)
        y -= 20

    c.save()
    return path
