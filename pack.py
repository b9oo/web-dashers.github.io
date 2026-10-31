import os, re, base64

input_file, output_file = "index.html", "web_dashers_complete.html"

def to_b64(path, mime):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return path

with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

# Inline CSS & JS
for css in re.findall(r'<link[^>]+href=["\']([^"\']+\.css)["\']', html):
    if os.path.exists(css):
        with open(css, "r", encoding="utf-8") as f: html = html.replace(f'<link rel="stylesheet" href="{css}">', f'<style>{f.read()}</style>')

for js in re.findall(r'<script[^>]+src=["\']([^"\']+\.js)["\']', html):
    if os.path.exists(js):
        with open(js, "r", encoding="utf-8") as f: html = html.replace(f'<script src="{js}"></script>', f'<script>{f.read()}</script>')

# Deep-scan and convert all images/assets found in the directory
extensions = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.mp3': 'audio/mpeg', '.ogg': 'audio/ogg', '.json': 'application/json'}
for root, _, files in os.walk("."):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in extensions:
            rel_path = os.path.relpath(os.path.join(root, file), ".").replace("\\", "/")
            # Replaces text references inside JS/HTML with the heavy Base64 data string
            b64_str = to_b64(rel_path, extensions[ext])
            html = html.replace(f'"{rel_path}"', f'"{b64_str}"').replace(f"'{rel_path}'", f"'{b64_str}'")

with open(output_file, "w", encoding="utf-8") as f: f.write(html)
print("Finished compiling complete game file!")
