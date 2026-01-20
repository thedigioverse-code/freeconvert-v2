document.addEventListener('DOMContentLoaded', async () => {
    // Mobile Menu Toggle
    const mobileToggle = document.getElementById('mobile-toggle') || document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            mobileToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }

    // Close menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileToggle.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // Tool Search
    const searchInput = document.getElementById('tool-search');
    const toolGrid = document.querySelector('.tool-grid');

    async function loadTools() {
        if (window.TOOLS_DATA) {
            renderTools(window.TOOLS_DATA);
            return window.TOOLS_DATA;
        }

        // Fallback for server environment if needed
        try {
            const response = await fetch('tools/tools.json');
            const tools = await response.json();
            renderTools(tools);
            return tools;
        } catch (e) {
            console.error("Failed to load tools", e);
            document.querySelector('.tool-grid').innerHTML = '<p style="color:red; text-align:center; grid-column: 1/-1;">Error loading tools. Please use a web server or check tools-data.js.</p>';
            return [];
        }
    }

    function renderTools(tools) {
        toolGrid.innerHTML = tools.map(tool => `
            <a href="tools/${tool.id}.html" class="tool-card glass">
                <div class="tool-icon">${tool.icon}</div>
                <h3>${tool.name}</h3>
                <p>${tool.description}</p>
            </a>
        `).join('');
    }

    const allTools = await loadTools();

    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = allTools.filter(tool =>
            tool.name.toLowerCase().includes(term) ||
            tool.description.toLowerCase().includes(term)
        );
        renderTools(filtered);
    });
});
