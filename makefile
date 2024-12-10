# Variables
NOTEBOOK = research.ipynb
MARKDOWN = research.md
PDF = CS226_ResearchPaper_GevorgNersesian.pdf

# Default target
all: $(PDF)

# Convert Jupyter Notebook to Markdown
$(MARKDOWN): $(NOTEBOOK)
	jupyter nbconvert --to markdown $(NOTEBOOK)

# Convert Markdown to PDF
$(PDF): $(MARKDOWN)
	pandoc $(MARKDOWN) -o $(PDF) --pdf-engine=xelatex --metadata linkcolor=blue

# Clean up intermediate files
clean:
	rm -f $(MARKDOWN) $(PDF)
