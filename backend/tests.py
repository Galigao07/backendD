from django.test import TestCase
from reportlab.lib.units import mm,cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas

data = [
    "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."
      "This is line 1 with more than 40 characters, so it will be split into multiple lines.",
    "Line 2 is shorter, but it still might need splitting.",
    "Line 3 is even shorter."

]

# Define the line of hyphens
hyphen_line = "-" * 55  # 55 hyphens in a row

# Determine the width and height based on the data length
line_height = 0.5 * cm
margin = 0.1 * cm  # Adjust margins as needed
width = 79 * mm  # Width adjusted for 79 mm roll paper
# Set the initial height for the first page

# Calculate the required height based on the data length
height = (len(data) + 3) * line_height + 2 * margin  # Adding 3 for header, footer, and hyphen lines

# Create a canvas with calculated size
c = canvas.Canvas("dynamic_poster.pdf", pagesize=(width, height))

# Set up a font and size
c.setFont("Helvetica-Bold", 8.5)

# Calculate x-coordinate for center alignment of "SALES INVOICE"
text_width = c.stringWidth("SALES INVOICE", "Helvetica-Bold", 10)
x_center = (width - text_width) / 2

# Initial y position
y_position = height - margin - line_height  # Adjust y position as needed

# Draw "SALES INVOICE" centered horizontally on the page
c.drawString(x_center, y_position, "SALES INVOICE")
y_position -= line_height

# Draw hyphen line before data
c.drawString(10 * mm, y_position, hyphen_line)  # Adjust x position as needed
y_position -= line_height

# Draw data lines
for line in data:
    # Split line into chunks of 40 characters
    chunks = [line[i:i+40] for i in range(0, len(line), 40)]
    for chunk in chunks:
        c.setFillColor(colors.red)
        c.drawString(10 * mm, y_position, chunk)
        y_position -= line_height

# Draw hyphen line after data
c.drawString(10 * mm, y_position, hyphen_line)  # Adjust x position as needed

# Save the PDF
c.save()
