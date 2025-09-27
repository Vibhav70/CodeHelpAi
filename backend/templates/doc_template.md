Project Documentation
This document provides a high-level overview of the codebase, generated from AI-powered summaries.

{% for file_path, data in files.items() %}

File: {{ file_path }}
{% if data.get('functions') %}

Standalone Functions
{% for func in data.functions %}

{{ func.function_name }}()
Summary: {{ func.summary }}

python
{{ func.source_code }}
{% endfor %}
{% endif %}

{% if data.get('classes') %}

Classes
{% for class_name, class_data in data.classes.items() %}

class {{ class_name }}
Summary: {{ class_data.summary }}

{% if class_data.get('methods') %} Methods:

{% for method in class_data.methods %}

{{ method.method_name }}(): {{ method.summary }} {% endfor %}
{% endif %} Full Source Code:

python
{{ class_data.source_code }}
{% endfor %}
{% endif %}

{% endfor %}

