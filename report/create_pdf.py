from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


input_file = "scouting_report.md"
output_file = "scouting_report.pdf"


with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()


doc = SimpleDocTemplate(output_file)

styles = getSampleStyleSheet()

story = []

for line in text.split("\n"):

    if line.startswith("#"):
        story.append(
            Paragraph(
                line.replace("#", ""),
                styles["Heading2"]
            )
        )
    else:
        story.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 12))


doc.build(story)

print("PDF created:", output_file)