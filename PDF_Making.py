import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Register a custom font (e.g., Arial)
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

import math
def format_stats_text(stats_text, layer_number):
    """Format region statistics with configurable column widths per statistic type"""
    regions = []
    current_region = []
    total_regions = ""
    region_stats = []  # To store complete stats for each region
    
    # Extract regions from text
    for line in stats_text.splitlines():
        line = line.strip()
        
        if line.startswith("Total regions detected:"):
            total_regions = line
            continue
            
        # Skip headers and separators
        if any(s in line for s in ["Region Statistics", "===", "---"]) or not line:
            continue
            
        if line.startswith("Region details:"):
            continue
            
        if line.startswith("Region"):
            if current_region:
                regions.append(current_region)
            current_region = [line.split(":")[0].strip()]
        elif current_region:
            if ":" in line:
                key, value = line.split(":", 1)
                current_region.append((key.strip(), value.strip()))
    
    if current_region:
        regions.append(current_region)

    # Extract all stats for each region
    for region in regions:
        region_name = region[0]
        mean_val = 0
        std_dev = 0
        area = 0
        
        for key, value in region[1:]:
            if key == "Mean value":
                mean_val = int(round(float(value)))
            elif key == "Variance":
                std_dev = int(round(math.sqrt(float(value))))
            elif key == "Area (pixels)":
                area = int(round(float(value)))
                
        region_stats.append((region_name, mean_val, std_dev, area))

    # Configurable column widths for different statistics
    HEADER_COL_WIDTH = 48   # Width for region header columns
    MEAN_COL_WIDTH = 37     # Width for mean value columns
    STD_DEV_COL_WIDTH = 34  # Width for standard deviation columns
    AREA_COL_WIDTH = 47     # Width for area columns

    formatted = []
    # Add layer number information at the top
    formatted.append(f"Layer Number: {layer_number}")
    formatted.append("")
    
    if total_regions:
        formatted.append(total_regions)
        formatted.append("")

    # Process regions in groups of 3
    for i in range(0, len(regions), 3):
        group = regions[i:i+3]
        
        # Create headers row
        header_line = ""
        for region in group:
            header_line += f"{region[0]}".ljust(HEADER_COL_WIDTH)
        formatted.append(header_line)
        
        # Create mean values row with integer conversion
        mean_line = ""
        for region in group:
            for key, value in region[1:]:
                if key == "Mean value":
                    # Convert to float, round to integer, then convert to string
                    int_value = int(round(float(value)))
                    mean_line += f"Mean value: {int_value} GV".ljust(MEAN_COL_WIDTH)
                    break
        formatted.append(mean_line)
        
        # Create standard deviation row (square root of variance)
        std_dev_line = ""
        for region in group:
            for key, value in region[1:]:
                if key == "Variance":
                    # Convert variance to standard deviation (sqrt of variance)
                    std_dev = math.sqrt(float(value))
                    # Round to integer
                    int_std_dev = int(round(std_dev))
                    std_dev_line += f"Standard Deviation: {int_std_dev} GV".ljust(STD_DEV_COL_WIDTH)
                    break
        formatted.append(std_dev_line)
        
        # Create area row with integer conversion
        area_line = ""
        for region in group:
            for key, value in region[1:]:
                if key == "Area (pixels)":
                    # Convert to float, round to integer, then convert to string
                    int_value = int(round(float(value)))
                    area_line += f"Area: {int_value} px".ljust(AREA_COL_WIDTH)
                    break
        formatted.append(area_line)
        
        formatted.append("")  # Empty line between groups
    
    # Add enhanced overall analysis with comprehensive region statistics
    formatted.append("Overall Analysis:")
    for region_name, mean_val, std_dev, area in region_stats:
        if(std_dev<500):
            if(area>0):
               formatted.append(f"  {region_name}: Indicates unsafe Thermal condition-")
               formatted.append(f"                   The melt pool is overly heated and stable, which is not ideal")
            else:
                formatted.append(f"  {region_name}: No considerable defect")
        elif(std_dev>3000):
            if(area>20):
                formatted.append(f"  {region_name}: Indicates Lack of fusion")
            else:
                formatted.append(f"  {region_name}: No considerable defect")
        else :
            formatted.append(f"  {region_name}: No considerable defect")
        
    formatted.append("")  # Empty line after overall analysis

    return formatted

def create_pdf_report(image_folder, stats_folder, output_pdf, logo_path,layer_counter):
    page_width, page_height = A4
    margin = 40
    header_margin = 80  # Increased margin for header section to accommodate logo
    avail_width = page_width - 2 * margin
    avail_height = page_height - header_margin - margin  # Adjusted available height

    # Define a 1x3 grid (3 blocks per page)
    cell_height = avail_height / 3
    img_sub_width = avail_width * 0.35  # 35% width for images
    text_sub_width = avail_width * 0.65  # 65% width for text

    padding_between_blocks = 15
    padding_image_text = 15

    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.setTitle("Quality Report")

    # Load logo image
    logo_img = None
    logo_width = 40  # Adjust the logo width as needed
    logo_height = 40  # Adjust the logo height as needed
    
    try:
        logo_img = ImageReader(logo_path)
        # Get actual logo dimensions
        lw, lh = logo_img.getSize()
        # Calculate scaling to maintain aspect ratio
        logo_scale = min(logo_width / lw, logo_height / lh)
        logo_width = lw * logo_scale
        logo_height = lh * logo_scale
    except Exception as e:
        print(f"Could not load logo image: {e}")

    valid_extensions = ('.png', '.jpg', '.jpeg', '.tif', '.tiff')
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)])
    
    total_pages = (len(image_files) + 2) // 3

    for idx, img_file in enumerate(image_files):
        if idx % 3 == 0:
            if idx != 0:
                c.showPage()
            
            # Add sky blue background to the page
            c.setFillColorRGB(0.9, 0.9, 1)  # Light blue color
            c.rect(0, 0, page_width, page_height, fill=True)

            # Add the logo in the top right corner (adjusted position)
            if logo_img:
                logo_x = page_width - margin - logo_width
                logo_y = page_height - margin - logo_height + 30
                c.drawImage(logo_img, logo_x, logo_y, width=logo_width, height=logo_height,
                            preserveAspectRatio=True, mask='auto')

            # Add header with horizontal line below it (adjusted position)
            c.setFillColorRGB(0, 0, 0)  # Reset text color to black
            c.setFont("Helvetica-Bold", 23)
            header_y = page_height - header_margin + 20 - (logo_height / 2) - 10
            c.drawString(margin, header_y + 50, "Quality-Report")
            c.line(margin, header_y +25, page_width - margin, header_y +25)

            # Add footer with centered text and horizontal line above it
            footer_text_y_position = margin - 20
            c.setFont("Helvetica", 12)
            c.drawCentredString(page_width / 2, footer_text_y_position+10, "Mechanical Department, IIT-BHU")
            c.line(margin, footer_text_y_position+5, page_width - margin, footer_text_y_position+5)

            # Add page number below the footer line
            c.setFont("Helvetica", 10)
            c.drawString(margin, footer_text_y_position - 10, f"Page {idx // 3 + 1} of {total_pages}")

        cell_index = idx % 3
        y_cell_start = margin + (2 - cell_index) * cell_height + padding_between_blocks * cell_index

        # Draw image (35% width)
        image_path = os.path.join(image_folder, img_file)
        try:
            img = ImageReader(image_path)
            iw, ih = img.getSize()
            scale = min(img_sub_width / iw, cell_height / ih)
            new_w, new_h = iw * scale, ih * scale
            x_img = margin
            y_img = y_cell_start + (cell_height - new_h) / 2
            c.drawImage(img, x_img, y_img, width=new_w, height=new_h,
                        preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print(f"Could not load image {img_file}: {e}")

        # Process and draw stats (65% width)
        base_name = os.path.splitext(img_file)[0]
        stats_file = os.path.join(stats_folder, base_name + ".txt")
        stats_text = ""
        if os.path.exists(stats_file):
            with open(stats_file, "r") as f:
                stats_text = f.read()

        # For each image you process:
        filtered_lines = format_stats_text(stats_text, layer_counter)
        layer_counter += 1  # Increment for the next image

        x_text_start = margin + img_sub_width + padding_image_text
        y_text_start = y_cell_start + cell_height - margin

        text_obj = c.beginText()
        text_obj.setTextOrigin(x_text_start, y_text_start)
        text_obj.setFont("Arial", 8)  
        text_obj.setLeading(9)       

        for line in filtered_lines:
            text_obj.textLine(line)

        c.drawText(text_obj)

    c.save()
    print(f"PDF report created: {output_pdf}")

if __name__ == "__main__":
    image_folder = "Processed_Images"
    stats_folder = "Processed_Stats"
    output_pdf = "Data_Report.pdf"
    # logo_path = "Logic_Magic.png"  
    logo_path = "IIT_BHU_Logo.png"  
    # In your main function or loop where you're processing multiple images:
    layer_counter = 1
    create_pdf_report(image_folder, stats_folder, output_pdf, logo_path,layer_counter)
