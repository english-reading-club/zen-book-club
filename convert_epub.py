#!/usr/bin/env python3
import zipfile
import os
from pathlib import Path
from html.parser import HTMLParser

class HTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.in_p = False
        
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_p = True
        elif tag == 'h1':
            self.markdown.append('\n# ')
        elif tag == 'h2':
            self.markdown.append('\n## ')
        elif tag == 'h3':
            self.markdown.append('\n### ')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
            
    def handle_endtag(self, tag):
        if tag == 'p':
            self.markdown.append('\n\n')
            self.in_p = False
        elif tag in ['h1', 'h2', 'h3']:
            self.markdown.append('\n')
        elif tag == 'em' or tag == 'i':
            self.markdown.append('*')
        elif tag == 'strong' or tag == 'b':
            self.markdown.append('**')
            
    def handle_data(self, data):
        self.markdown.append(data.strip())
        
    def get_markdown(self):
        return ''.join(self.markdown).strip()

epub_path = "epub/Counterattacks at Thirty.epub"
output_dir = "markdown_chapters"
Path(output_dir).mkdir(exist_ok=True)

with zipfile.ZipFile(epub_path, 'r') as epub:
    for i in range(1, 29):
        chapter_file = f"Chapter_{i}.xhtml"
        try:
            with epub.open(chapter_file) as f:
                html_content = f.read().decode('utf-8')
                parser = HTMLToMarkdown()
                parser.feed(html_content)
                markdown = parser.get_markdown()
                
                output_file = f"{output_dir}/chapter_{i:02d}.md"
                with open(output_file, 'w', encoding='utf-8') as out:
                    out.write(markdown)
                print(f"Converted {chapter_file}")
        except KeyError:
            pass

print(f"\nDone! Chapters saved to {output_dir}/")
