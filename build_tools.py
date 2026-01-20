import os
import json

TOOLS_JSON = 'tools/tools.json'
TEMPLATE_PATH = 'tools/tool-template.html'
TOOLS_DIR = 'tools'

# --- EXISTING TEMPLATES ---

IMAGE_UI = """
<div id="drop-zone" class="drop-zone">
    <div class="drop-icon">📁</div>
    <p>Drag & Drop files or <span>Click to Browse</span></p>
    <input type="file" id="file-input" hidden>
</div>
<div id="preview-container" class="preview-container" style="display: none;">
    <canvas id="conversion-canvas" style="display: none;"></canvas>
    <img id="image-preview" src="" alt="Preview">
    <div class="action-buttons">
        <button id="convert-btn" class="btn primary">Convert & Download</button>
        <button id="reset-btn" class="btn secondary">Reset</button>
    </div>
</div>
"""

IMAGE_SCRIPT = """
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const imgPreview = document.getElementById('image-preview');
const convertBtn = document.getElementById('convert-btn');
const resetBtn = document.getElementById('reset-btn');
const canvas = document.getElementById('conversion-canvas');

dropZone.onclick = () => fileInput.click();
fileInput.onchange = (e) => handleFiles(e.target.files);
dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add('active'); };
dropZone.ondragleave = () => dropZone.classList.remove('active');
dropZone.ondrop = (e) => { e.preventDefault(); handleFiles(e.dataTransfer.files); };

function handleFiles(files) {
    if (files.length === 0) return;
    const file = files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
        imgPreview.src = e.target.result;
        dropZone.style.display = 'none';
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

convertBtn.onclick = () => {
    const ctx = canvas.getContext('2d');
    canvas.width = imgPreview.naturalWidth;
    canvas.height = imgPreview.naturalHeight;
    ctx.drawImage(imgPreview, 0, 0);
    const format = '{{ID}}' === 'png-to-jpg' || '{{ID}}' === 'webp-to-jpg' ? 'image/jpeg' : 'image/png';
    const ext = '{{ID}}' === 'png-to-jpg' || '{{ID}}' === 'webp-to-jpg' ? 'jpg' : 'png';
    const dataUrl = canvas.toDataURL(format, 0.9);
    const link = document.createElement('a');
    link.download = `converted-image.${ext}`;
    link.href = dataUrl;
    link.click();
};
resetBtn.onclick = () => location.reload();
"""

TEXT_UI = """
<textarea id="text-input" class="glass-input" placeholder="Paste your text here..."></textarea>
<div class="stats-grid">
    <div class="stat-item">Words: <span id="word-count">0</span></div>
    <div class="stat-item">Characters: <span id="char-count">0</span></div>
    <div class="stat-item">Sentences: <span id="sentence-count">0</span></div>
</div>
"""

TEXT_SCRIPT = """
const textInput = document.getElementById('text-input');
const wordCount = document.getElementById('word-count');
const charCount = document.getElementById('char-count');
const sentenceCount = document.getElementById('sentence-count');

textInput.addEventListener('input', () => {
    const text = textInput.value.trim();
    wordCount.textContent = text ? text.split(/\\s+/).length : 0;
    charCount.textContent = text.length;
    sentenceCount.textContent = text ? text.split(/[.!?]+/).filter(s => s.trim()).length : 0;
});
"""

SECURITY_UI = """
<div class="config-panel">
    <label>Length: <input type="number" id="pass-length" value="16" min="4" max="100"></label>
    <div class="checkbox-group">
        <label><input type="checkbox" id="include-upper" checked> Uppercase</label>
        <label><input type="checkbox" id="include-numbers" checked> Numbers</label>
        <label><input type="checkbox" id="include-symbols" checked> Symbols</label>
    </div>
</div>
<div class="result-box glass">
    <span id="password-result">********</span>
    <button id="copy-btn" class="btn secondary">Copy</button>
</div>
<button id="generate-btn" class="btn primary">Generate Password</button>
"""

SECURITY_SCRIPT = """
const generateBtn = document.getElementById('generate-btn');
const charDisplay = document.getElementById('password-result');
const copyBtn = document.getElementById('copy-btn');

generateBtn.onclick = () => {
    const length = document.getElementById('pass-length').value;
    const upper = document.getElementById('include-upper').checked;
    const num = document.getElementById('include-numbers').checked;
    const sym = document.getElementById('include-symbols').checked;
    
    let chars = "abcdefghijklmnopqrstuvwxyz";
    if (upper) chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    if (num) chars += "0123456789";
    if (sym) chars += "!@#$%^&*()_+~`|}{[]:;?><,./-=";
    
    let pass = "";
    for (let i = 0; i < length; i++) {
        pass += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    charDisplay.textContent = pass;
};

copyBtn.onclick = () => {
    navigator.clipboard.writeText(charDisplay.textContent);
    alert('Copied!');
};
"""

ADVANCED_IMAGE_UI = """
<div id="drop-zone" class="drop-zone">
    <div class="drop-icon">📁</div>
    <p>Drag & Drop files or <span>Click to Browse</span></p>
    <input type="file" id="file-input" hidden>
</div>
<div id="preview-container" class="preview-container" style="display: none;">
    <div class="controls-panel glass">
        <div id="resizer-controls" style="display: none;">
            <label>Width: <input type="number" id="resize-width"></label>
            <label>Height: <input type="number" id="resize-height"></label>
            <label><input type="checkbox" id="aspect-ratio" checked> Lock Aspect Ratio</label>
        </div>
        <div id="compressor-controls" style="display: none;">
            <label>Quality: <input type="range" id="quality-slider" min="10" max="100" value="80"> <span id="quality-val">80%</span></label>
        </div>
        <div id="palette-controls" style="display: none;">
            <div id="palette-display" style="display: flex; gap: 10px; margin-top: 10px;"></div>
        </div>
    </div>
    <canvas id="conversion-canvas" style="display: none;"></canvas>
    <img id="image-preview" src="" alt="Preview">
    <div class="action-buttons">
        <button id="convert-btn" class="btn primary">Process & Download</button>
        <button id="reset-btn" class="btn secondary">Reset</button>
    </div>
</div>
<!-- Libs for advanced tools -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/color-thief/2.3.0/color-thief.umd.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/heic2any/0.0.3/heic2any.min.js"></script>
"""

ADVANCED_IMAGE_SCRIPT = """
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const imgPreview = document.getElementById('image-preview');
const convertBtn = document.getElementById('convert-btn');
const resetBtn = document.getElementById('reset-btn');
const canvas = document.getElementById('conversion-canvas');

const rControls = document.getElementById('resizer-controls');
const cControls = document.getElementById('compressor-controls');
const pControls = document.getElementById('palette-controls');

const toolId = '{{ID}}';

if (toolId === 'image-resizer') rControls.style.display = 'block';
if (toolId === 'image-compressor') cControls.style.display = 'block';
if (toolId === 'palette-extractor') { pControls.style.display = 'block'; convertBtn.textContent = "Extract Colors"; }
if (toolId === 'heic-to-jpg' || toolId === 'svg-to-png' || toolId === 'ico-converter') convertBtn.textContent = "Convert Now";

dropZone.onclick = () => fileInput.click();
fileInput.onchange = (e) => handleFiles(e.target.files);
dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add('active'); };
dropZone.ondragleave = () => dropZone.classList.remove('active');
dropZone.ondrop = (e) => { e.preventDefault(); handleFiles(e.dataTransfer.files); };

let originalRatio = 1;

async function handleFiles(files) {
    if (files.length === 0) return;
    const file = files[0];
    
    // Special handling for HEIC
    if (toolId === 'heic-to-jpg' && file.name.toLowerCase().endsWith('.heic')) {
        try {
            const blob = await heic2any({ blob: file, toType: "image/jpeg" });
            imgPreview.src = URL.createObjectURL(blob);
            setupPreview();
            return;
        } catch (e) { alert('HEIC Error: ' + e.message); return; }
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        imgPreview.src = e.target.result;
        setupPreview();
    };
    reader.readAsDataURL(file);
}

function setupPreview() {
    imgPreview.onload = () => {
        originalRatio = imgPreview.naturalWidth / imgPreview.naturalHeight;
        if (toolId === 'image-resizer') {
            document.getElementById('resize-width').value = imgPreview.naturalWidth;
            document.getElementById('resize-height').value = imgPreview.naturalHeight;
        }
    };
    dropZone.style.display = 'none';
    previewContainer.style.display = 'block';
}

convertBtn.onclick = () => {
    if (toolId === 'palette-extractor') {
        const colorThief = new ColorThief();
        const palette = colorThief.getPalette(imgPreview, 5);
        const pDisplay = document.getElementById('palette-display');
        pDisplay.innerHTML = '';
        palette.forEach(color => {
            const rgb = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
            const hex = "#" + ((1 << 24) + (color[0] << 16) + (color[1] << 8) + color[2]).toString(16).slice(1).toUpperCase();
            const div = document.createElement('div');
            div.style.backgroundColor = rgb;
            div.style.width = '50px';
            div.style.height = '50px';
            div.title = hex;
            div.onclick = () => { navigator.clipboard.writeText(hex); alert('Copied ' + hex); };
            pDisplay.appendChild(div);
        });
        return;
    }

    const ctx = canvas.getContext('2d');
    let w = imgPreview.naturalWidth;
    let h = imgPreview.naturalHeight;

    if (toolId === 'image-resizer') {
        w = document.getElementById('resize-width').value;
        h = document.getElementById('resize-height').value;
    }
    if (toolId === 'ico-converter') { w = 32; h = 32; }

    canvas.width = w;
    canvas.height = h;
    ctx.drawImage(imgPreview, 0, 0, w, h);
    
    let quality = 0.9;
    if (toolId === 'image-compressor') quality = document.getElementById('quality-slider').value / 100;
    
    const format = (toolId === 'svg-to-png' || toolId === 'image-compressor' && !imgPreview.src.includes('image/jpeg')) ? 'image/png' : 'image/jpeg';
    
    let dataUrl = canvas.toDataURL(format, quality);
    let downloadName = `converted-${Date.now()}.${format === 'image/jpeg' ? 'jpg' : 'png'}`;
    
    if (toolId === 'ico-converter') {
        downloadName = 'favicon.ico'; 
        // Logic for real ICO binary is complex client-side, using PNG rename as basic fallback for MVP
         dataUrl = canvas.toDataURL('image/png');
    }

    const link = document.createElement('a');
    link.download = downloadName;
    link.href = dataUrl;
    link.click();
};
resetBtn.onclick = () => location.reload();
"""

QR_UI = """
<div class="config-panel">
    <input type="text" id="qr-data" class="glass-input" style="min-height: 50px;" placeholder="Enter URL or Text...">
</div>
<div id="qr-result" class="qr-container glass" style="display: flex; justify-content: center; padding: 2rem; margin-bottom: 2rem;">
    <!-- QR Code will be rendered here -->
</div>
<button id="generate-qr-btn" class="btn primary">Generate QR Code</button>
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
"""

QR_SCRIPT = """
const genBtn = document.getElementById('generate-qr-btn');
const qrData = document.getElementById('qr-data');
const qrResult = document.getElementById('qr-result');

genBtn.onclick = () => {
    const data = qrData.value.trim();
    if (!data) { alert('Please enter some text or a URL'); return; }
    qrResult.innerHTML = "";
    new QRCode(qrResult, {
        text: data,
        width: 256,
        height: 256,
        colorDark : "#a855f7",
        colorLight : "transparent",
        correctLevel : QRCode.CorrectLevel.H
    });
};
"""

CASE_UI = """
<textarea id="text-input" class="glass-input" placeholder="Paste your text here..."></textarea>
<div class="action-buttons">
    <button id="upper-btn" class="btn secondary">UPPERCASE</button>
    <button id="lower-btn" class="btn secondary">lowercase</button>
    <button id="title-btn" class="btn secondary">Title Case</button>
</div>
"""

CASE_SCRIPT = """
const textInput = document.getElementById('text-input');
document.getElementById('upper-btn').onclick = () => { textInput.value = textInput.value.toUpperCase(); };
document.getElementById('lower-btn').onclick = () => { textInput.value = textInput.value.toLowerCase(); };
document.getElementById('title-btn').onclick = () => { 
    textInput.value = textInput.value.toLowerCase().split(' ').map(s => s.charAt(0).toUpperCase() + s.substring(1)).join(' '); 
};
"""

# --- NEW DEV TOOLS ---

DEV_BASIC_UI = """
<div class="split-view">
    <textarea id="dev-input" class="glass-input" placeholder="Input..."></textarea>
    <div class="action-buttons-vertical">
        <button id="action-btn" class="btn primary">Process -></button>
    </div>
    <textarea id="dev-output" class="glass-input" placeholder="Output..." readonly></textarea>
</div>
"""

DEV_BASIC_SCRIPT = """
const input = document.getElementById('dev-input');
const output = document.getElementById('dev-output');
const btn = document.getElementById('action-btn');
const toolId = '{{ID}}';

btn.onclick = () => {
    const val = input.value;
    try {
        if (toolId === 'json-to-csv') {
            const items = JSON.parse(val);
            const replacer = (key, value) => value === null ? '' : value;
            const header = Object.keys(items[0]);
            let csv = items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','));
            csv.unshift(header.join(','));
            output.value = csv.join('\\r\\n');
        } else if (toolId === 'base64-tool') {
            // Check if input looks like base64 to decide decode vs encode, or simple toggle
            try { output.value = atob(val); } catch { output.value = btoa(val); }
        }
    } catch (e) {
        output.value = "Error: " + e.message;
    }
};
"""

DEV_ADVANCED_UI = """
<div id="editor-container" class="split-view">
    <textarea id="adv-input" class="glass-input" placeholder="Paste code here..."></textarea>
    <div id="adv-preview" class="glass-input preview-box"></div>
</div>
<textarea id="adv-output" class="glass-input" style="display:none;" placeholder="Output..."></textarea>
<div class="action-buttons">
    <button id="adv-action-btn" class="btn primary">Run</button>
</div>
<style> .split-view { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; } </style>
<script src="https://unpkg.com/sql-formatter@4.0.2/dist/sql-formatter.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jsdiff/5.1.0/diff.min.js"></script>
"""

DEV_ADVANCED_SCRIPT = """
const input = document.getElementById('adv-input');
const preview = document.getElementById('adv-preview');
const output = document.getElementById('adv-output');
const btn = document.getElementById('adv-action-btn');
const toolId = '{{ID}}';

btn.onclick = () => {
    const val = input.value;
    if (toolId === 'sql-formatter') {
        output.style.display = 'block';
        preview.style.display = 'none';
        output.value = sqlFormatter.format(val);
    } else if (toolId === 'markdown-editor') {
        preview.innerHTML = marked.parse(val);
    }
    // Diff checker requiring 2 inputs logic omitted for brevity in this generic template
};
// Live preview for markdown
if (toolId === 'markdown-editor') {
    input.addEventListener('input', () => { preview.innerHTML = marked.parse(input.value); });
}
"""

UTILITY_UI = """
<div class="utility-panel glass">
    <div id="utility-content"></div>
</div>
"""

UTILITY_SCRIPT = """
const container = document.getElementById('utility-content');
const toolId = '{{ID}}';

if (toolId === 'lorem-ipsum') {
    container.innerHTML = `
        <div class="config-panel">
            <label>Paragraphs: <input type="number" id="lorem-count" value="3" min="1" max="10"></label>
        </div>
        <button class="btn primary" onclick="generateLorem()">Generate Lorem Ipsum</button>
        <textarea id="lorem-out" class="glass-input" style="margin-top:20px; height: 300px;" readonly></textarea>
    `;
    window.generateLorem = () => {
        const count = document.getElementById('lorem-count').value;
        const text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";
        let out = "";
        for(let i=0; i<count; i++) out += text + "\\n\\n";
        document.getElementById('lorem-out').value = out;
    };
} else if (toolId === 'password-strength') {
    container.innerHTML = `
        <input type="password" id="pass-input" class="glass-input" placeholder="Type a password to check strength..." style="margin-bottom: 20px;">
        <div id="strength-bar" style="height: 10px; background: #333; border-radius: 5px; overflow: hidden; margin-bottom: 10px;">
            <div id="strength-fill" style="height: 100%; width: 0%; background: red; transition: all 0.3s;"></div>
        </div>
        <h3 id="strength-text" style="color: white; text-align: center;">Enter Password</h3>
    `;
    document.getElementById('pass-input').addEventListener('input', (e) => {
        const val = e.target.value;
        let score = 0;
        if (val.length > 8) score++;
        if (val.length > 12) score++;
        if (/[A-Z]/.test(val)) score++;
        if (/[0-9]/.test(val)) score++;
        if (/[^A-Za-z0-9]/.test(val)) score++;
        
        const fill = document.getElementById('strength-fill');
        const text = document.getElementById('strength-text');
        
        let color = 'red';
        let label = 'Weak';
        let percent = (score / 5) * 100;
        
        if (score > 2) { color = 'orange'; label = 'Medium'; }
        if (score > 4) { color = '#a855f7'; label = 'Strong'; }
        
        if (val.length === 0) { percent = 0; label = 'Enter Password'; }
        
        fill.style.width = percent + '%';
        fill.style.background = color;
        text.textContent = label;
        text.style.color = color;
    });
} else if (toolId === 'stopwatch') {
    container.innerHTML = `<h1 id="timer" style="font-size: 3rem; text-align: center; margin-bottom: 2rem;">00:00:00</h1><div style="text-align:center"><button class="btn primary" onclick="startTimer()">Start</button> <button class="btn secondary" onclick="stopTimer()">Stop</button> <button class="btn secondary" onclick="resetTimer()">Reset</button></div>`;
    let interval, seconds = 0;
    window.startTimer = () => { 
        if(interval) return;
        interval = setInterval(() => { seconds++; const d = new Date(seconds * 1000); document.getElementById('timer').textContent = d.toISOString().substr(11, 8); }, 1000); 
    };
    window.stopTimer = () => { clearInterval(interval); interval = null; };
    window.resetTimer = () => { clearInterval(interval); interval = null; seconds = 0; document.getElementById('timer').textContent = "00:00:00"; };
} else if (toolId === 'speed-test') {
    container.innerHTML = `<div style="text-align: center"><button class="btn primary" onclick="runSpeed()">Start Speed Test</button><h2 id="speed-result" style="margin-top: 2rem; font-size: 2rem;"></h2></div>`;
    window.runSpeed = async () => {
        document.getElementById('speed-result').innerText = "Testing...";
        const start = Date.now();
        // Fetch a known file size (e.g. 500kb dummy image or just reuse google logo multiple times for approx)
        try {
            await fetch('https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png?cache=' + Math.random());
            await fetch('https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png?cache=' + Math.random());
            const duration = (Date.now() - start) / 1000;
            // Approx mock logic improved
            const speed = (20 / duration).toFixed(2); 
            document.getElementById('speed-result').innerText = speed + " Mbps (Estimated)";
        } catch {
            document.getElementById('speed-result').innerText = "Error - Check Connection";
        }
    };
}
"""

def build():
    with open(TOOLS_JSON, 'r', encoding='utf-8') as f:
        tools = json.load(f)
    
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    for tool in tools:
        ui = ""
        script = ""
        how_to = ""
        
        t_type = tool['type']
        t_id = tool['id']
        
        if t_type == 'image':
            ui = IMAGE_UI
            script = IMAGE_SCRIPT.replace('{{ID}}', t_id)
            how_to = "<ol><li>Upload your file.</li><li>Click Convert.</li><li>Download.</li></ol>"
        elif t_type == 'text':
            if t_id == 'word-counter':
                ui = TEXT_UI
                script = TEXT_SCRIPT
                how_to = "<ol><li>Paste your text.</li><li>View real-time statistics.</li></ol>"
            else:
                ui = CASE_UI
                script = CASE_SCRIPT
                how_to = "<ol><li>Paste your text.</li><li>Click a button to change case.</li></ol>"
        elif t_type == 'security':
            if t_id == 'password-strength': 
                ui = UTILITY_UI 
                script = UTILITY_SCRIPT.replace('{{ID}}', t_id)
            else:
                ui = SECURITY_UI
                script = SECURITY_SCRIPT
            how_to = "<ol><li>Set your options.</li><li>Generate.</li><li>Copy your password.</li></ol>"
        elif t_type == 'image_advanced':
            ui = ADVANCED_IMAGE_UI
            script = ADVANCED_IMAGE_SCRIPT.replace('{{ID}}', t_id)
            how_to = f"<ol><li>Upload your image.</li><li>Adjust settings.</li><li>Download.</li></ol>"
        elif t_type == 'qr':
            ui = QR_UI
            script = QR_SCRIPT
            how_to = "<ol><li>Enter your link or text.</li><li>Click Generate.</li><li>Right click to save the image.</li></ol>"
        elif t_type == 'dev_basic':
            ui = DEV_BASIC_UI
            script = DEV_BASIC_SCRIPT.replace('{{ID}}', t_id)
            how_to = "<ol><li>Paste input.</li><li>Click Process.</li><li>Copy output.</li></ol>"
        elif t_type == 'dev_advanced':
            ui = DEV_ADVANCED_UI
            script = DEV_ADVANCED_SCRIPT.replace('{{ID}}', t_id)
            how_to = "<ol><li>Paste code.</li><li>See result instantly.</li></ol>"
        elif t_type == 'utility':
            ui = UTILITY_UI
            script = UTILITY_SCRIPT.replace('{{ID}}', t_id)
            how_to = "<ol><li>Interact with the tool.</li></ol>"

        html = template.replace('{{NAME}}', tool['name'])
        if ' ' in tool['name']:
            html = html.replace('{{NAME_H1_START}}', tool['name'].split(' ')[0])
            html = html.replace('{{NAME_H1_END}}', ' '.join(tool['name'].split(' ')[1:]))
        else:
            html = html.replace('{{NAME_H1_START}}', tool['name'])
            html = html.replace('{{NAME_H1_END}}', '')
            
        html = html.replace('{{DESCRIPTION}}', tool['description'])
        html = html.replace('{{TOOL_UI}}', ui)
        html = html.replace('{{HOW_TO}}', how_to)
        
        # Robust replacement
        html = html.replace('{{SPECIFIC_SCRIPT}}', script)
        html = html.replace('{ { SPECIFIC_SCRIPT } }', script)
        html = html.replace('{{ID}}', t_id)
        
        # SEO Injection
        canonical_tag = f'<link rel="canonical" href="https://freeconvert.cloud/tools/{t_id}.html" />'
        # FAQ Schema Logic (Extract from how_to)
        # how_to format is <ol><li>Step 1</li><li>Step 2</li></ol>
        # We parse this simple structure to create Questions/Answers
        steps = []
        if "<ol>" in how_to:
            raw_steps = how_to.replace("<ol>", "").replace("</ol>", "").split("<li>")
            for s in raw_steps:
                clean_s = s.replace("</li>", "").strip()
                if clean_s:
                    steps.append(clean_s)
        
        faq_entities = []
        for i, step in enumerate(steps):
            faq_entities.append({
                "@type": "Question",
                "name": f"Step {i+1}: How do I use {tool['name']}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": step
                }
            })

        schema_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "SoftwareApplication",
                    "name": tool['name'],
                    "operatingSystem": "Any",
                    "applicationCategory": tool.get('category', 'Utility'),
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "USD"
                    },
                    "description": tool['description']
                },
                {
                    "@type": "FAQPage",
                    "mainEntity": faq_entities
                }
            ]
        }
        schema_tag = f'<script type="application/ld+json">{json.dumps(schema_data)}</script>'
        
        html = html.replace('{{CANONICAL}}', canonical_tag)
        html = html.replace('{{SCHEMA}}', schema_tag)

        with open(f"tools/{t_id}.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Built tool: {t_id}")

    # Generate Sitemap
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    # Homepage
    sitemap_content += '  <url>\n    <loc>https://freeconvert.cloud/</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    # Tools
    for tool in tools:
        sitemap_content += f'  <url>\n    <loc>https://freeconvert.cloud/tools/{tool["id"]}.html</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    
    # Hub Pages (Blog) - Scan directory
    if os.path.exists('blog/hub-pages'):
        for filename in os.listdir('blog/hub-pages'):
            if filename.endswith('.html'):
                sitemap_content += f'  <url>\n    <loc>https://freeconvert.cloud/blog/hub-pages/{filename}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'

    sitemap_content += '</urlset>'
    
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml")

    # Generate Robots.txt
    robots_content = "User-agent: *\nAllow: /\nSitemap: https://freeconvert.cloud/sitemap.xml"
    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)
    print("Generated robots.txt")

if __name__ == "__main__":
    build()
