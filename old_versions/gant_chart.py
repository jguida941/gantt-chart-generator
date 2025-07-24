import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# ===== DATA DEFINITION SECTION =====
# Purpose: Define the project's tasks with detailed timeline and progress information.
# This structured data represents each phase and task in the software development lifecycle,
# including start and end dates, the phase category, and completion progress percentage.
data = [
    {"Task": "Collect Requirements", "Start": "2023-01-22", "End": "2023-02-04", "Phase": "Planning", "Progress": 100},
    {"Task": "Create Use Case Diagrams", "Start": "2023-02-11", "End": "2023-02-18", "Phase": "Design",
     "Progress": 100},
    {"Task": "Build Activity Diagrams", "Start": "2023-02-15", "End": "2023-03-09", "Phase": "Design", "Progress": 100},
    {"Task": "Research UI Designs", "Start": "2023-02-27", "End": "2023-03-07", "Phase": "Design", "Progress": 100},
    {"Task": "Build Class Diagram", "Start": "2023-03-01", "End": "2023-03-09", "Phase": "Design", "Progress": 100},
    {"Task": "Get Customer Approval", "Start": "2023-03-10", "End": "2023-03-11", "Phase": "Approval", "Progress": 100},
    {"Task": "Build Interface", "Start": "2023-03-12", "End": "2023-03-24", "Phase": "Development", "Progress": 100},
    {"Task": "Link DB to Interface", "Start": "2023-03-24", "End": "2023-04-03", "Phase": "Development",
     "Progress": 100},
    {"Task": "Build Business Logic", "Start": "2023-04-05", "End": "2023-04-27", "Phase": "Development",
     "Progress": 100},
    {"Task": "Test System", "Start": "2023-04-27", "End": "2023-05-07", "Phase": "Testing", "Progress": 100},
    {"Task": "Deliver System", "Start": "2023-05-08", "End": "2023-05-09", "Phase": "Deployment", "Progress": 100},
    {"Task": "Sign-off Meeting", "Start": "2023-05-09", "End": "2023-05-10", "Phase": "Deployment", "Progress": 100},
]

# ===== DATA PREPROCESSING SECTION =====
# Purpose: Transform raw task data into a format suitable for visualization and analysis.
# This includes converting date strings to datetime objects, calculating task durations,
# and preparing detailed hover text for interactive chart tooltips.
df = pd.DataFrame(data)  # Convert list of dictionaries to DataFrame for easier manipulation

# Convert 'Start' and 'End' columns from string to datetime objects to enable time-based calculations
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

# Calculate the duration of each task in days, adding 1 to include both start and end dates
df['Duration'] = (df['End'] - df['Start']).dt.days + 1

# Create a rich HTML-formatted string for hover tooltips, showing task details clearly
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
# Purpose: Define a consistent and meaningful color palette for different project phases.
# This helps visually distinguish phases on the Gantt chart, improving readability and interpretation.
phase_colors = {
    "Planning": "#FF6B6B",  # Red - Represents initial planning phase tasks
    "Design": "#4ECDC4",  # Teal - Tasks related to design and architecture
    "Approval": "#FFE66D",  # Yellow - Milestones involving customer approval
    "Development": "#45B7D1",  # Blue - Core development activities
    "Testing": "#96CEB4",  # Green - Quality assurance and testing tasks
    "Deployment": "#9B59B6"  # Purple - Final deployment and sign-off tasks
}

# Map each task's phase to its corresponding color for use in the chart
df['Color'] = df['Phase'].map(phase_colors)

# ===== GANTT CHART CREATION =====
# Purpose: Generate an interactive Gantt chart visualizing the project timeline using Plotly Express.
# The chart uses start and end dates, task names, and phase colors to display the schedule.
fig = px.timeline(
    df,
    x_start="Start",
    x_end="End",
    y="Task",
    color="Phase",
    color_discrete_map=phase_colors,  # Apply custom phase colors defined earlier
    title="Enhanced Project Gantt Chart - Software Development Lifecycle",
    hover_data={"Hover_Text": True, "Start": False, "End": False, "Phase": False},  # Show only custom hover text
    labels={"Phase": "Project Phase"}  # Rename legend title for clarity
)

# ===== CHART CUSTOMIZATION SECTION =====
# Purpose: Improve chart usability and aesthetics by adjusting axes and hover behavior.
# Reverse y-axis so tasks are listed top-down in chronological order.
fig.update_yaxes(autorange="reversed")

# Customize hover display to show our detailed hover text and position text inside bars.
fig.update_traces(
    hovertemplate="%{customdata[0]}<extra></extra>",  # Use custom hover text without extra info
    textposition="inside",
    insidetextanchor="middle"
)

# ===== LAYOUT ENHANCEMENTS =====
# Purpose: Refine the overall chart layout including size, fonts, colors, margins, and legend for better readability.
fig.update_layout(
    height=600,  # Set chart height for clear visibility
    width=1200,  # Set chart width to accommodate all tasks and legend

    # Customize the chart title with centered alignment and specific font styling
    title={
        'text': "Enhanced Project Gantt Chart - Software Development Lifecycle",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 24, 'color': '#2C3E50'}
    },

    # Set background colors to a light theme for visual comfort
    plot_bgcolor='#F8F9FA',
    paper_bgcolor='white',

    # Define the font family, size, and color for all text elements
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="#2C3E50"
    ),

    # Add margins around the chart to prevent clipping of labels and legend
    margin=dict(l=200, r=50, t=100, b=50),

    # Customize the legend appearance and positioning to the right side of the chart
    legend=dict(
        title="Project Phases",
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02,
        bgcolor="rgba(255, 255, 255, 0.8)",  # Slightly transparent white background
        bordercolor="#CCCCCC",
        borderwidth=1
    ),

    # Enable and customize the x-axis range slider for zooming and panning through dates
    xaxis=dict(
        rangeslider=dict(visible=True),
        type="date",
        tickformat="%b %d\n%Y",  # Format ticks as 'Month Day Year' on two lines
        showgrid=True,
        gridcolor='#E0E0E0'  # Light gray grid lines for readability
    ),

    # Customize y-axis grid lines and tick font for clarity
    yaxis=dict(
        showgrid=True,
        gridcolor='#E0E0E0',
        tickfont=dict(size=11)
    )
)

# ===== ADD MILESTONE MARKERS =====
# Purpose: Visually highlight key project milestones with vertical dashed lines and labels on the timeline.
milestones = [
    {"date": "2023-03-11", "label": "Customer Approval", "color": "#E74C3C"},  # Important approval milestone in red
    {"date": "2023-05-10", "label": "Project Complete", "color": "#27AE60"}  # Project completion milestone in green
]

for milestone in milestones:
    fig.add_vline(
        # Convert milestone date to timestamp in milliseconds, required by Plotly's add_vline
        x=pd.to_datetime(milestone["date"]).timestamp() * 1000,
        line_dash="dash",  # Use dashed line style for milestones
        line_color=milestone["color"],
        annotation_text=milestone["label"],  # Label the milestone line
        annotation_position="top",
        annotation_font_color=milestone["color"],  # Match annotation color to line color
        annotation_font_size=10
    )

# ===== ADD TODAY'S DATE MARKER (if within project timeline) =====
# Purpose: Show a vertical line indicating the current date if it falls within the project duration,
# helping viewers understand current progress relative to the schedule.
today = datetime.now()
project_start = df['Start'].min()
project_end = df['End'].max()

if project_start <= today <= project_end:
    fig.add_vline(
        # Convert current datetime to timestamp in milliseconds for Plotly
        x=pd.to_datetime(today).timestamp() * 1000,
        line_dash="solid",  # Solid line to differentiate from milestones
        line_color="#FF6B6B",  # Use red color consistent with planning phase
        line_width=2,
        annotation_text="Today",  # Label the vertical line as 'Today'
        annotation_position="top",
        annotation_font_color="#FF6B6B"
    )

# ===== DISPLAY THE CHART =====
# Purpose: Render the interactive Gantt chart in the output environment (e.g., Jupyter notebook or browser).
fig.show()

# ===== OPTIONAL: SAVE THE CHART =====
# Purpose: Provide options to save the chart in various formats for sharing or embedding.
# Uncomment these lines to export the chart as needed.
# fig.write_html("gantt_chart.html")  # Save as interactive HTML file for web use
# fig.write_image("gantt_chart.png")  # Save as static PNG image (requires kaleido package)
# fig.write_json("gantt_chart.json")  # Save chart data in JSON format for reuse or analysis


# ===== EXPORT INTERACTIVE HTML AND AUTO-LAUNCH =====
# Save the chart as a full HTML file and open it in the default web browser
# From there, use File → Print → Save as PDF for best visual fidelity
import webbrowser

fig.write_html("gantt_chart_full.html")
webbrowser.open("gantt_chart_full.html")