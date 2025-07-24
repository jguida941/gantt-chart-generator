# Gantt Chart Generator - System Architecture & Flow Diagrams

## Table of Contents
1. [System Overview](#system-overview)
2. [Data Flow Architecture](#data-flow-architecture)
3. [Component Architecture](#component-architecture)
4. [User Interaction Flow](#user-interaction-flow)
5. [PDF Export Process](#pdf-export-process)
6. [Technical Stack](#technical-stack)

## System Overview

```mermaid
graph TB
    subgraph "Input Layer"
        A[Task Data] --> B[Python Script]
        C[Configuration] --> B
    end
    
    subgraph "Processing Layer"
        B --> D[Pandas DataFrame]
        D --> E[Data Transformation]
        E --> F[Plotly Chart Engine]
        F --> G[HTML Generation]
    end
    
    subgraph "Styling Layer"
        H[CSS Glassmorphism] --> G
        I[JetBrains Mono Font] --> G
        J[Responsive Design] --> G
    end
    
    subgraph "Output Layer"
        G --> K[Interactive HTML]
        K --> L[Browser Display]
        K --> M[PDF Export]
        M --> N[Print-Optimized CSS]
    end
    
    style A fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style B fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style F fill:#45B7D1,stroke:#333,stroke-width:2px,color:#fff
    style K fill:#9B59B6,stroke:#333,stroke-width:2px,color:#fff
```

## Data Flow Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant P as Python Script
    participant D as Data Layer
    participant PL as Plotly
    participant H as HTML Generator
    participant B as Browser
    participant PDF as PDF Engine
    
    U->>P: Execute Script
    P->>D: Load Task Data
    D->>D: Create DataFrame
    D->>D: Calculate Durations
    D->>D: Add Hover Text
    P->>PL: Initialize Timeline Chart
    PL->>PL: Apply Color Mapping
    PL->>PL: Configure Layout
    PL->>PL: Add Milestones
    P->>H: Generate HTML Structure
    H->>H: Inject Plotly Chart
    H->>H: Add CSS Styles
    H->>H: Create Task Table
    H->>B: Save & Open HTML
    B->>U: Display Interactive Chart
    U->>B: Click Export PDF
    B->>PDF: Trigger Print Dialog
    PDF->>PDF: Apply Print CSS
    PDF->>U: Generate PDF File
```

## Component Architecture

```mermaid
graph LR
    subgraph "Core Components"
        A[gantt_chart_final_fixed.py] --> B[Main Execution]
        B --> C[Data Definition]
        B --> D[Chart Creation]
        B --> E[HTML Generation]
    end
    
    subgraph "Data Processing"
        C --> F[Task Dictionary]
        F --> G[Pandas DataFrame]
        G --> H[Date Calculations]
        H --> I[Progress Tracking]
    end
    
    subgraph "Visualization"
        D --> J[Plotly Timeline]
        J --> K[Phase Colors]
        J --> L[Hover Details]
        J --> M[Milestones]
        J --> N[Range Slider]
    end
    
    subgraph "Styling System"
        E --> O[Glassmorphism CSS]
        E --> P[Print CSS]
        E --> Q[Responsive Design]
        E --> R[Dark Theme]
    end
    
    style A fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style J fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style O fill:#45B7D1,stroke:#333,stroke-width:2px,color:#fff
```

## User Interaction Flow

```mermaid
stateDiagram-v2
    [*] --> Loading: Open HTML File
    Loading --> Interactive: Page Loaded
    
    Interactive --> Hovering: Mouse Over Task
    Hovering --> ShowTooltip: Display Details
    ShowTooltip --> Interactive: Mouse Out
    
    Interactive --> Sliding: Use Range Slider
    Sliding --> UpdateView: Adjust Timeline
    UpdateView --> Interactive: Release Slider
    
    Interactive --> Zooming: Scroll/Pinch
    Zooming --> ZoomedView: Update Scale
    ZoomedView --> Interactive: Stop Zoom
    
    Interactive --> Exporting: Click Export PDF
    Exporting --> PrintDialog: Browser Print
    PrintDialog --> ApplyPrintCSS: User Confirms
    ApplyPrintCSS --> GeneratePDF: Create File
    GeneratePDF --> [*]: Download PDF
    
    note right of Hovering: Shows task details,\nduration, progress
    note right of Sliding: Filters visible\ndate range
    note right of ApplyPrintCSS: Removes slider,\nadjusts colors
```

## PDF Export Process

```mermaid
flowchart TD
    A[User Clicks Export PDF] --> B{Browser Type?}
    B -->|Chrome/Edge| C[Native Print Dialog]
    B -->|Firefox| D[Print Preview]
    B -->|Safari| E[PDF Options]
    
    C --> F[Print CSS Applied]
    D --> F
    E --> F
    
    F --> G[Hide Interactive Elements]
    G --> H[Apply High Contrast]
    H --> I[Set Fixed Dimensions]
    I --> J[Landscape Orientation]
    J --> K[Generate PDF]
    
    K --> L{Quality Check}
    L -->|Pass| M[Save PDF File]
    L -->|Fail| N[Adjust Settings]
    N --> C
    
    subgraph "Print CSS Transformations"
        G --> O[Hide Range Slider]
        G --> P[Remove Animations]
        H --> Q[Black Text on White]
        H --> R[Solid Color Badges]
        I --> S[A4 Landscape Size]
        I --> T[Fixed Margins 10mm]
    end
    
    style A fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style F fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style K fill:#45B7D1,stroke:#333,stroke-width:2px,color:#fff
    style M fill:#96CEB4,stroke:#333,stroke-width:2px,color:#fff
```

## Technical Stack

```mermaid
mindmap
  root((Gantt Chart<br/>Generator))
    Python Stack
      Pandas 2.x
        DataFrame Operations
        Date/Time Handling
      Plotly 5.x
        Timeline Charts
        Interactive Features
        HTML Export
      Standard Library
        datetime
        webbrowser
        os module
    Frontend Stack
      HTML5
        Semantic Structure
        Meta Tags
      CSS3
        Glassmorphism
        Grid/Flexbox
        Media Queries
        Print Styles
      JavaScript
        Plotly.js
        Event Handlers
    Design System
      Typography
        JetBrains Mono
        Inter Font
      Color Palette
        Planning: #FF6B6B
        Design: #4ECDC4
        Approval: #FFE66D
        Development: #45B7D1
        Testing: #96CEB4
        Deployment: #9B59B6
      Effects
        Backdrop Blur
        Gradients
        Animations
        Shadows
    Export Features
      PDF Generation
        Print CSS
        A4 Landscape
        High Contrast
      Image Export
        PNG Format
        High Resolution
        Kaleido Backend
```

## Data Model

```mermaid
classDiagram
    class Task {
        +String name
        +Date startDate
        +Date endDate
        +String phase
        +Int progress
        +Int duration
        +String hoverText
        +String color
    }
    
    class Phase {
        +String name
        +String color
        +List~Task~ tasks
    }
    
    class Milestone {
        +Date date
        +String label
        +String color
    }
    
    class GanttChart {
        +List~Task~ tasks
        +List~Phase~ phases
        +List~Milestone~ milestones
        +DataFrame dataFrame
        +Figure plotlyFigure
        +String htmlOutput
        +generateChart()
        +addMilestone()
        +exportHTML()
        +exportPDF()
    }
    
    class HTMLGenerator {
        +String template
        +String cssStyles
        +String plotlyChart
        +String taskTable
        +generate()
        +injectStyles()
        +addPrintCSS()
    }
    
    Task "1..*" --> "1" Phase
    GanttChart "1" --> "*" Task
    GanttChart "1" --> "*" Phase
    GanttChart "1" --> "*" Milestone
    GanttChart "1" --> "1" HTMLGenerator
```

## File Structure

```mermaid
graph TD
    A[gantt_chart/] --> B[src/]
    A --> C[output/]
    A --> D[docs/]
    A --> E[tutorials/]
    A --> F[old_versions/]
    
    B --> G[gantt_chart_final_fixed.py]
    B --> H[gantt_chart_modern.py]
    
    C --> I[gantt_chart_final.html]
    C --> J[gantt_chart.pdf]
    C --> K[gantt_chart_for_pdf.png]
    
    D --> L[README.md]
    D --> M[ARCHITECTURE.md]
    D --> N[FLOWCHARTS.md]
    D --> O[CLAUDE.md]
    
    E --> P[gantt_chart_tutorial.ipynb]
    
    F --> Q[Previous Versions...]
    
    style A fill:#2C3E50,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#FF6B6B,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#4ECDC4,stroke:#333,stroke-width:2px,color:#fff
    style D fill:#45B7D1,stroke:#333,stroke-width:2px,color:#fff
    style E fill:#96CEB4,stroke:#333,stroke-width:2px,color:#fff
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Start Script] --> B{Check Dependencies}
    B -->|Missing| C[Display Error Message]
    C --> D[Suggest pip install]
    D --> E[Exit]
    
    B -->|Present| F[Load Data]
    F --> G{Data Valid?}
    G -->|No| H[Log Error]
    H --> E
    
    G -->|Yes| I[Generate Chart]
    I --> J{Plotly Success?}
    J -->|No| K[Fallback to Basic]
    K --> L[Continue with Warning]
    
    J -->|Yes| M[Create HTML]
    M --> N{File Write OK?}
    N -->|No| O[Permission Error]
    O --> E
    
    N -->|Yes| P[Open Browser]
    P --> Q{Browser Found?}
    Q -->|No| R[Display File Path]
    R --> S[End]
    
    Q -->|Yes| T[Display Chart]
    T --> S
    
    style A fill:#27AE60,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#E74C3C,stroke:#333,stroke-width:2px,color:#fff
    style T fill:#3498DB,stroke:#333,stroke-width:2px,color:#fff
```

## Performance Optimization

```mermaid
graph LR
    subgraph "Optimization Strategies"
        A[Data Loading] --> B[Lazy Loading]
        A --> C[Caching]
        
        D[Rendering] --> E[Virtual DOM]
        D --> F[WebGL Acceleration]
        
        G[Export] --> H[Async Processing]
        G --> I[Image Compression]
        
        J[CSS] --> K[Minification]
        J --> L[Critical CSS]
    end
    
    subgraph "Performance Metrics"
        M[Load Time < 2s]
        N[Interactive in < 100ms]
        O[Export in < 5s]
        P[60 FPS Animations]
    end
    
    B --> M
    F --> N
    H --> O
    E --> P
```

---

## Usage Instructions

These diagrams can be rendered using any Mermaid-compatible viewer:
- GitHub (automatic rendering in markdown)
- VS Code with Mermaid extension
- Online editors like mermaid.live
- Documentation tools like MkDocs or Docusaurus

For best results, view these diagrams in a tool that supports Mermaid's latest features including mindmaps and state diagrams.