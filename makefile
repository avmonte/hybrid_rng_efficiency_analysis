# Variables
NOTEBOOK = research.ipynb
MARKDOWN = research.md
PDF = research.pdf

# Default target
all: $(PDF)

# Convert Jupyter Notebook to Markdown
$(MARKDOWN): $(NOTEBOOK)
	jupyter nbconvert --to markdown $(NOTEBOOK)

# Convert Markdown to PDF
$(PDF): $(MARKDOWN)
	pandoc $(MARKDOWN) -o $(PDF) --pdf-engine=xelatex

# Clean up intermediate files
clean:
	rm -f $(MARKDOWN) $(PDF)
