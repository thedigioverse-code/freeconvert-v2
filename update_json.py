import json
import os

TOOLS_FILE = r'c:\Users\Admin\.gemini\antigravity\scratch\freeconvert-v2\tools\tools.json'

new_tools = [
    {
        "id": "csv-to-json",
        "name": "CSV to JSON",
        "icon": "📑",
        "description": "Convert CSV data to JSON format instantly.",
        "type": "dev_basic",
        "category": "Developer",
        "seo_title": "Free CSV to JSON Converter Online - 100% Secure",
        "seo_desc": "Convert CSV files to JSON format instantly in your browser. Fast, free, and privacy-focused."
    },
    {
        "id": "hash-generator",
        "name": "Hash Generator",
        "icon": "🔐",
        "description": "Generate MD5, SHA1, and SHA256 hashes.",
        "type": "utility",
        "category": "Security",
        "seo_title": "SHA256 & MD5 Hash Generator - Secure Online Tool",
        "seo_desc": "Generate secure cryptographic hashes (MD5, SHA1, SHA256) for your data for free."
    },
    {
        "id": "unicode-converter",
        "name": "Unicode Converter",
        "icon": "🔡",
        "description": "Convert text to Unicode and vice-versa.",
        "type": "dev_basic",
        "category": "Developer",
        "seo_title": "Unicode Text Converter - Encode & Decode Online",
        "seo_desc": "Convert plain text to Unicode and vice-versa. Perfect for developers and internationalization."
    },
    {
        "id": "morse-code",
        "name": "Morse Code Converter",
        "icon": "📟",
        "description": "Translate text to Morse code and back.",
        "type": "utility",
        "category": "Utility",
        "seo_title": "Online Morse Code Translator - Text to Morse",
        "seo_desc": "Translate text to Morse code and back instantly. Accurate, fast, and free to use."
    }
]

with open(TOOLS_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Avoid duplicates if script is re-run
existing_ids = {t['id'] for t in data}
for tool in new_tools:
    if tool['id'] not in existing_ids:
        data.append(tool)

with open(TOOLS_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Successfully updated tools.json")
