#!/bin/bash

# Generate PDF using Chrome headless mode
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if [ -f "$CHROME" ]; then
        echo "Generating PDF using Chrome headless mode..."
        "$CHROME" --headless --disable-gpu --print-to-pdf=gantt_chart_chrome.pdf gantt_chart_pdf_ready.html
        echo "PDF generated: gantt_chart_chrome.pdf"
    else
        echo "Google Chrome not found. Please install Chrome or use the browser's Print to PDF feature."
    fi
else
    # Linux
    if command -v google-chrome &> /dev/null; then
        echo "Generating PDF using Chrome headless mode..."
        google-chrome --headless --disable-gpu --print-to-pdf=gantt_chart_chrome.pdf gantt_chart_pdf_ready.html
        echo "PDF generated: gantt_chart_chrome.pdf"
    else
        echo "Google Chrome not found. Please install Chrome or use the browser's Print to PDF feature."
    fi
fi