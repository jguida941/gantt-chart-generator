import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import webbrowser
import base64

# ===== DATA DEFINITION SECTION =====
data = [
    {"Task": "Collect Requirements", "Start": "2023-01-22", "End": "2023-02-04", "Phase": "Planning", "Progress": 100},
    {"Task": "Create Use Case Diagrams", "Start": "2023-02-11", "End": "2023-02-18", "Phase": "Design", "Progress": 100},
    {"Task": "Build Activity Diagrams", "Start": "2023-02-15", "End": "2023-03-09", "Phase": "Design", "Progress": 100},
    {"Task": "Research UI Designs", "Start": "2023-02-27", "End": "2023-03-07", "Phase": "Design", "Progress": 100},
    {"Task": "Build Class Diagram", "Start": "2023-03-01", "End": "2023-03-09", "Phase": "Design", "Progress": 100},
    {"Task": "Get Customer Approval", "Start": "2023-03-10", "End": "2023-03-11", "Phase": "Approval", "Progress": 100},
    {"Task": "Build Interface", "Start": "2023-03-12", "End": "2023-03-24", "Phase": "Development", "Progress": 100},
    {"Task": "Link DB to Interface", "Start": "2023-03-24", "End": "2023-04-03", "Phase": "Development", "Progress": 100},
    {"Task": "Build Business Logic", "Start": "2023-04-05", "End": "2023-04-27", "Phase": "Development", "Progress": 100},
    {"Task": "Test System", "Start": "2023-04-27", "End": "2023-05-07", "Phase": "Testing", "Progress": 100},
    {"Task": "Deliver System", "Start": "2023-05-08", "End": "2023-05-09", "Phase": "Deployment", "Progress": 100},
    {"Task": "Sign-off Meeting", "Start": "2023-05-09", "End": "2023-05-10", "Phase": "Deployment", "Progress": 100},
]

# ===== DATA PREPROCESSING SECTION =====
df = pd.DataFrame(data)
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])
df['Duration'] = (df['End'] - df['Start']).dt.days + 1

df['Hover_Text'] = df.apply(lambda row:
                            f"<b>{row['Task']}</b><br>" +
                            f"Phase: {row['Phase']}<br>" +
                            f"Start: {row['Start'].strftime('%B %d, %Y')}<br>" +
                            f"End: {row['End'].strftime('%B %d, %Y')}<br>" +
                            f"Duration: {row['Duration']} days<br>" +
                            f"Progress: {row['Progress']}%",
                            axis=1
                            )

# ===== COLOR SCHEME DEFINITION =====
phase_colors = {
    "Planning": "#FF6B6B",
    "Design": "#4ECDC4",
    "Approval": "#FFE66D",
    "Development": "#45B7D1",
    "Testing": "#96CEB4",
    "Deployment": "#9B59B6"
}

df['Color'] = df['Phase'].map(phase_colors)

# ===== CREATE INTERACTIVE GANTT CHART =====
fig = px.timeline(
    df,
    x_start="Start",
    x_end="End",
    y="Task",
    color="Phase",
    color_discrete_map=phase_colors,
    title="Enhanced Project Gantt Chart - Software Development Lifecycle",
    hover_data={"Hover_Text": True, "Start": False, "End": False, "Phase": False},
    labels={"Phase": "Project Phase"}
)

fig.update_yaxes(autorange="reversed")

fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>",
    textposition="inside",
    insidetextanchor="middle"
)

fig.update_layout(
    height=600,
    width=1200,
    title={
        'text': "Enhanced Project Gantt Chart - Software Development Lifecycle",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#2C3E50'}
    },
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='white',
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#2C3E50"
    ),
    margin=dict(l=200, r=50, t=100, b=50),
    legend=dict(
        title="Project Phases",
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#CCCCCC",
        borderwidth=1
    ),
    xaxis=dict(
        rangeslider=dict(visible=True),
        type="date",
        tickformat="%b %d\n%Y",
        showgrid=True,
        gridcolor='#E0E0E0'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        tickfont=dict(size=11)
    )
)

# ===== ADD MILESTONE MARKERS =====
milestones = [
    {"date": "2023-03-11", "label": "Customer Approval", "color": "#E74C3C"},
    {"date": "2023-05-10", "label": "Project Complete", "color": "#27AE60"}
]

for milestone in milestones:
    fig.add_vline(
        x=pd.to_datetime(milestone["date"]).timestamp() * 1000,
        line_dash="dash",
        line_color=milestone["color"],
        annotation_text=milestone["label"],
        annotation_position="top",
        annotation_font_color=milestone["color"],
        annotation_font_size=10
    )

# ===== EXPORT HIGH-QUALITY IMAGE FOR PDF =====
print("Generating high-quality PNG for PDF...")
try:
    fig.write_image("gantt_chart_hq.png", width=1200, height=800, scale=3)
    print("✓ High-quality PNG saved successfully!")
    
    # Read the PNG and encode it for embedding
    with open("gantt_chart_hq.png", "rb") as img_file:
        png_base64 = base64.b64encode(img_file.read()).decode('utf-8')
except Exception as e:
    print(f"Warning: Could not generate PNG (install kaleido if needed): {e}")
    png_base64 = None

# ===== CREATE COMPREHENSIVE HTML WITH BOTH INTERACTIVE CHART AND PDF DOWNLOAD =====
html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Project Gantt Chart</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        h1 {{
            color: #2C3E50;
            margin-bottom: 10px;
        }}
        .download-section {{
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .download-btn {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #45B7D1;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
            margin: 0 10px;
        }}
        .download-btn:hover {{
            background-color: #357a9a;
        }}
        .download-btn.secondary {{
            background-color: #96CEB4;
        }}
        .download-btn.secondary:hover {{
            background-color: #7ab09a;
        }}
        .info {{
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f4f8;
            border-left: 4px solid #45B7D1;
            border-radius: 0 5px 5px 0;
        }}
        .chart-container {{
            margin: 30px 0;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }}
        @media print {{
            body {{
                margin: 0;
                padding: 0;
            }}
            .download-section {{
                display: none;
            }}
            .container {{
                box-shadow: none;
                border-radius: 0;
            }}
        }}
        .pdf-preview {{
            margin: 20px 0;
            text-align: center;
        }}
        .pdf-preview img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script>
        function downloadPDF() {{
            const {{ jsPDF }} = window.jspdf;
            const doc = new jsPDF({{
                orientation: 'landscape',
                unit: 'mm',
                format: 'a4'
            }});
            
            // Add title
            doc.setFontSize(20);
            doc.text('Project Gantt Chart - Software Development Lifecycle', 150, 20, {{ align: 'center' }});
            
            // Add project info
            doc.setFontSize(12);
            doc.text('Project Duration: January 22, 2023 - May 10, 2023', 20, 35);
            doc.text('Total Tasks: 12', 20, 42);
            doc.text('Key Milestones: Customer Approval (March 11), Project Complete (May 10)', 20, 49);
            
            {png_section}
            
            doc.save('gantt_chart.pdf');
        }}
        
        function printChart() {{
            window.print();
        }}
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Project Gantt Chart</h1>
            <p>Software Development Lifecycle Timeline</p>
        </div>
        
        <div class="download-section">
            <h3>Download Options</h3>
            <button class="download-btn" onclick="downloadPDF()">📥 Download as PDF</button>
            <button class="download-btn secondary" onclick="printChart()">🖨️ Print / Save as PDF</button>
        </div>
        
        <div class="info">
            <strong>Project Summary:</strong>
            <ul>
                <li>Duration: January 22, 2023 - May 10, 2023</li>
                <li>Total Tasks: 12</li>
                <li>Phases: Planning, Design, Approval, Development, Testing, Deployment</li>
                <li>Key Milestones: Customer Approval (March 11), Project Complete (May 10)</li>
            </ul>
        </div>
        
        <div class="chart-container">
            {chart_div}
        </div>
        
        {pdf_preview_section}
    </div>
</body>
</html>
"""

# Generate the interactive chart HTML
chart_html = fig.to_html(include_plotlyjs='cdn', div_id="gantt-chart")

# Extract just the div from the chart HTML
import re
chart_div_match = re.search(r'<div id="gantt-chart".*?</script>\s*</div>', chart_html, re.DOTALL)
chart_div = chart_div_match.group() if chart_div_match else chart_html

# Prepare the PNG section for PDF generation
if png_base64:
    png_section = f"""
            // Add the Gantt chart image
            const imgData = 'data:image/png;base64,{png_base64}';
            doc.addImage(imgData, 'PNG', 10, 60, 277, 130);
    """
    pdf_preview_section = f"""
        <div class="pdf-preview">
            <h3>PDF Preview</h3>
            <img src="data:image/png;base64,{png_base64}" alt="Gantt Chart">
        </div>
    """
else:
    png_section = """
            // PNG image not available
            doc.text('Chart image not available. Please use Print option for visual chart.', 150, 100, { align: 'center' });
    """
    pdf_preview_section = ""

# Create the final HTML
final_html = html_template.format(
    chart_div=chart_div,
    png_section=png_section,
    pdf_preview_section=pdf_preview_section
)

# Save the HTML file
with open("gantt_chart_complete.html", "w", encoding='utf-8') as f:
    f.write(final_html)

print("\n✓ Complete Gantt chart saved to 'gantt_chart_complete.html'")
print("\nFeatures:")
print("- Interactive chart with zoom, pan, and hover")
print("- Download as PDF button (with embedded chart image)")
print("- Print/Save as PDF option (browser native)")
print("\nOpening in browser...")

# Open in browser
import os
file_path = os.path.abspath("gantt_chart_complete.html")
webbrowser.open(f"file://{file_path}")