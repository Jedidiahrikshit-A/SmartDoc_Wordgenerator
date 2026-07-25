from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


def create_document(title, sections, contents, filename):

    document = Document()

    # ----------------------------
    # Page Margins (1 inch)
    # ----------------------------
    section = document.sections[0]

    section.top_margin = Pt(72)
    section.bottom_margin = Pt(72)
    section.left_margin = Pt(72)
    section.right_margin = Pt(72)

    # ----------------------------
    # Title
    # ----------------------------
    title_para = document.add_heading(level=0)
    title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER

    title_run = title_para.add_run(title)

    title_run.bold = True
    title_run.font.name = "Times New Roman"
    title_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    title_run.font.size = Pt(22)
    title_run.font.color.rgb = RGBColor(0, 0, 0)

    document.add_paragraph()

    # ----------------------------
    # Sections
    # ----------------------------
    for i in range(len(sections)):

        # Section Heading
        heading = document.add_heading(level=1)

        heading.alignment = WD_ALIGN_PARAGRAPH.LEFT

        heading_run = heading.add_run(sections[i].upper())

        heading_run.bold = True
        heading_run.font.name = "Times New Roman"
        heading_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
        heading_run.font.size = Pt(16)
        heading_run.font.color.rgb = RGBColor(0, 0, 0)

        # Content
        paragraph = document.add_paragraph()

        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        paragraph.paragraph_format.line_spacing = 1.5
        paragraph.paragraph_format.first_line_indent = Pt(24)
        paragraph.paragraph_format.space_after = Pt(12)

        content_run = paragraph.add_run(contents[i])

        content_run.bold = False
        content_run.font.name = "Times New Roman"
        content_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
        content_run.font.size = Pt(12)
        content_run.font.color.rgb = RGBColor(0, 0, 0)

        # Every section except the last starts on a new page
        if i < len(sections) - 1:
            document.add_page_break()

    document.save(filename)