import os
import json
from datetime import datetime

TEMPLATE_PATH = 'blog/blog-template.html'
BLOG_DIR = 'blog'
TOPICS_FILE = 'blog/topics.json'

def generate_blog_post(title, content, date=None):
    if not date:
        date = datetime.now().strftime("%B %d, %Y")
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    
    filename = title.lower().replace(' ', '-').replace('?', '') + '.html'
    
    html = template.replace('{{TITLE}}', title)
    html = html.replace('{{CONTENT}}', content)
    html = html.replace('{{DATE}}', date)
    
    output_path = os.path.join(BLOG_DIR, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated: {output_path}")

def main():
    if not os.path.exists(TOPICS_FILE):
        print(f"No topics found at {TOPICS_FILE}")
        return
        
    with open(TOPICS_FILE, 'r', encoding='utf-8') as f:
        topics = json.load(f)
    
    for topic in topics:
        generate_blog_post(topic['title'], topic['content'])

if __name__ == "__main__":
    main()
