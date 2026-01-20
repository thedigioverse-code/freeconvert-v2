import os
import json

TEMPLATE_PATH = 'blog/blog-template.html'
BLOG_DIR = 'blog/hub-pages'
TOPICS_FILE = 'blog/hub_topics.json'

if not os.path.exists(BLOG_DIR):
    os.makedirs(BLOG_DIR)

def generate_hub_page(topic):
    title = topic['title']
    tool_id = topic['tool_id']
    keywords = topic['keywords']
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # Generate content optimized for Hub Page
    content = f"""
    <p>Are you looking for a way to <strong>{keywords[0]}</strong>? You've come to the right place. Our free online tool makes it easy to {title.lower()} in seconds.</p>
    
    <h2>Why use our {title} tool?</h2>
    <ul>
        <li><strong>Fast & Secure:</strong> All processing happens in your browser.</li>
        <li><strong>Free Forever:</strong> No hidden costs or subscriptions.</li>
        <li><strong>High Quality:</strong> Professional results every time.</li>
    </ul>

    <div class="cta-box" style="background: rgba(255,255,255,0.05); padding: 2rem; border-radius: 1rem; text-align: center; margin: 2rem 0; border: 1px solid rgba(255,255,255,0.1);">
        <h3 style="margin-bottom: 1rem; color: #fff;">Ready to get started?</h3>
        <a href="../../tools/{tool_id}.html" class="btn primary" style="text-decoration: none; display: inline-block; font-size: 1.2rem;">🚀 Open {title} Tool</a>
    </div>

    <h2>How to {keywords[0]}?</h2>
    <p>Using freeconvert.cloud is simple:</p>
    <ol>
        <li>Click the button above to open the tool.</li>
        <li>Follow the on-screen instructions.</li>
        <li>Download your result instantly.</li>
    </ol>
    
    <p>Thousands of users trust us for {keywords[1]} every day. Try it now!</p>
    """
    
    filename = title.lower().replace(' ', '-').replace('?', '') + '.html'
    
    # Template has ../../style.css already, good for blog/hub-pages/
    html = template.replace('{{TITLE}}', title)
    
    # Re-inject title after template replace which might have reset it
    html = html.replace('{{TITLE}}', title)
    html = html.replace('{{CONTENT}}', content)
    html = html.replace('{{DATE}}', "Updated Today")
    
    output_path = os.path.join(BLOG_DIR, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated Hub Page: {output_path}")

def update_sitemap(topics):
    sitemap_path = 'sitemap.xml'
    if not os.path.exists(sitemap_path):
        print("Sitemap not found, skipping update.")
        return

    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove closing tag to append
    content = content.replace('</urlset>', '')
    
    new_urls = ""
    for topic in topics:
        slug = topic['title'].lower().replace(' ', '-').replace('?', '')
        url = f"https://freeconvert.cloud/blog/hub-pages/{slug}.html"
        if url not in content:
            new_urls += f'  <url>\n    <loc>{url}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
            
    content += new_urls + '</urlset>'
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Added {len(topics)} hub pages to sitemap.xml")

def main():
    if not os.path.exists(TOPICS_FILE):
        print(f"No topics found at {TOPICS_FILE}")
        return
        
    with open(TOPICS_FILE, 'r', encoding='utf-8') as f:
        topics = json.load(f)
    
    for topic in topics:
        generate_hub_page(topic)
    
    update_sitemap(topics)

if __name__ == "__main__":
    main()
