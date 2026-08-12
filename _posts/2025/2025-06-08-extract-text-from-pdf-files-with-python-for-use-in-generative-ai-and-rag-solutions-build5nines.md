---
layout: post
date: 2025-06-08
title: "Text is the new gold."
type: linked
cited: Build5Nines
link: https://build5nines.com/extract-text-from-pdf-files-with-python-for-use-in-generative-ai-and-rag-solutions/
seo: "Text is the new gold"
---

Plain text, or perhaps markdown is the new gold, especially in the context of Generative AI. Extracting text from PDF files is a common task that can be accomplished using Python libraries like `pdfplumber`. Microsoft released `MarkItDown` a python library to extract LLM ready text format.

Nothing beats a folder of markdown files with some front matter that an LLM or SSG (Like this site's use of Jekyll) can use to generate content or format it for human consumption.

> Extracting Text from PDFs
> Extracting text from PDFs involves reading the document and parsing its content. With `pdfplumber`, this process is straightforward:​

```python
    import pdfplumber

    def extract_text_from_pdf(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            all_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
        return '\n'.join(all_text)

    pdf_path = 'sample.pdf'
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)
```

> In this function:
>
> The PDF is opened using pdfplumber.open().
> Each page is iterated over, and extract_text() retrieves the textual content.
> The extracted text from all pages is combined into a single string.
