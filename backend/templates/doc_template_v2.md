<style>
/* Custom CSS for beautiful documentation */
.header-main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.project-overview {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 3px 10px rgba(245, 87, 108, 0.3);
}

.toc-container {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    box-shadow: 0 3px 10px rgba(79, 172, 254, 0.3);
}

.toc-container h2 {
    color: white;
    margin-top: 0;
}

.toc-container ul {
    color: white;
}

.toc-container a {
    color: #ffffff;
    text-decoration: none;
    font-weight: 500;
}

.toc-container a:hover {
    text-decoration: underline;
}

.file-section {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
}

.file-section h3 {
    color: white;
    margin-top: 0;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.class-container {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    padding: 1.2rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 5px solid #667eea;
    box-shadow: 0 2px 8px rgba(168, 237, 234, 0.4);
}

.class-container h5 {
    color: #2d3748;
    margin-top: 0;
}

.function-container {
    background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
    padding: 1.2rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 5px solid #f093fb;
    box-shadow: 0 2px 8px rgba(252, 182, 159, 0.4);
}

.function-container h5 {
    color: #2d3748;
    margin-top: 0;
}

.summary-text {
    background: rgba(255, 255, 255, 0.9);
    padding: 1rem;
    border-radius: 6px;
    color: #2d3748;
    font-style: italic;
    border-left: 4px solid #4facfe;
    margin: 0.5rem 0;
}

.methods-table {
    background: white;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.methods-table table {
    width: 100%;
    border-collapse: collapse;
}

.methods-table th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 12px;
    text-align: left;
}

.methods-table td {
    padding: 12px;
    border-bottom: 1px solid #e2e8f0;
    color: #2d3748;
}

.methods-table tr:nth-child(even) {
    background-color: #f8fafc;
}

.code-block {
    background: #2d3748;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    overflow-x: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    border: 1px solid #4a5568;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 9999px;
    margin-right: 0.5rem;
}

.section-divider {
    height: 3px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border: none;
    border-radius: 2px;
    margin: 2rem 0;
}
</style>

<div class="header-main">
<h1>📚 Codebase Documentation: {{ project_name }}</h1>
</div>

<div class="project-overview">
<h2>🚀 Project Overview</h2>
<div class="summary-text">{{ project_summary }}</div>
</div>

<div class="toc-container">
<h2>📋 Table of Contents</h2>

{% for file_path, content in files.items() %}
- [📄 {{ file_path }}](#{{ file_path | replace('.', '-') | replace('\\', '-') | replace('/', '-') | replace(':', '-') | replace(' ', '-') | lower }})
{% if content.classes %}
{% for class_name, class_details in content.classes.items() %}
  - [🏛️ {{ class_name }}](#{{ class_name | replace(' ', '-') | lower }})
{% endfor %}
{% endif %}
{% endfor %}

</div>

<hr class="section-divider">

<h2>🔍 Codebase Details</h2>

{% for file_path, content in files.items() %}

<div class="file-section">
<h3><a name="{{ file_path | replace('.', '-') | replace('\\', '-') | replace('/', '-') | replace(':', '-') | replace(' ', '-') | lower }}"></a>📄 File: <code>{{ file_path }}</code></h3>

{% if content.classes %}

<h4>🏛️ Classes</h4>

{% for class_name, class_details in content.classes.items() %}

<div class="class-container">
<h5><a name="{{ class_name | replace(' ', '-') | lower }}"></a><span class="badge">CLASS</span>{{ class_name }}</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> {{ class_details.summary }}
</div>

{% if class_details.methods %}
<div class="methods-table">
<table>
<thead>
<tr>
<th>🔧 Method</th>
<th>📝 Summary</th>
</tr>
</thead>
<tbody>
{% for method in class_details.methods %}
<tr>
<td><code>{{ method.method_name }}()</code></td>
<td>{{ method.summary }}</td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
{% endif %}

<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">{{ class_details.source_code }}</code></pre>
</div>

</div>

{% endfor %}
{% endif %}

{% if content.functions %}

<h4>⚙️ Standalone Functions</h4>

{% for func in content.functions %}

<div class="function-container">
<h5><span class="badge">FUNCTION</span>{{ func.function_name }}()</h5>

<div class="summary-text">
<strong>📖 Summary:</strong> {{ func.summary }}
</div>

<strong>💾 Full Source Code:</strong>
<div class="code-block">
<pre><code class="language-python">{{ func.source_code }}</code></pre>
</div>

</div>

{% endfor %}
{% endif %}

</div>

{% endfor %}