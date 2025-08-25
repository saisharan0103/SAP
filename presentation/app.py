import os
from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = "dev"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(ROOT, "docs")

def markdown_to_html(text: str) -> str:
    """Minimal Markdown renderer supporting headings and paragraphs."""
    lines = text.splitlines()
    html_lines = []
    for line in lines:
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        else:
            html_lines.append(f"<p>{line}</p>")
    return "\n".join(html_lines)

@app.route("/")
def dashboard():
    kpis = {"cash": 1000, "receivables": 500, "payables": 300, "stock": 150}
    return render_template("dashboard.html", kpis=kpis)

@app.route("/help/<doc>")
def help_page(doc: str):
    filename = doc if doc.endswith(".md") else f"{doc}.md"
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    with open(path, "r", encoding="utf-8") as f:
        html = markdown_to_html(f.read())
    return render_template("help.html", content=html)

@app.route("/invoice", methods=["GET", "POST"])
def invoice():
    step = int(request.args.get("step", 1))
    if request.method == "POST":
        if step == 1:
            session["invoice"] = {
                "customer": request.form.get("customer", ""),
                "amount": request.form.get("amount", ""),
            }
            return redirect(url_for("invoice", step=2))
        else:
            data = session.pop("invoice", {})
            return render_template("invoice_done.html", data=data)
    data = session.get("invoice", {})
    return render_template(f"invoice_step{step}.html", data=data)

@app.route("/stock-transfer", methods=["GET", "POST"])
def stock_transfer():
    step = int(request.args.get("step", 1))
    if request.method == "POST":
        if step == 1:
            session["transfer"] = {
                "item": request.form.get("item", ""),
                "quantity": request.form.get("quantity", ""),
                "from_location": request.form.get("from_location", ""),
                "to_location": request.form.get("to_location", ""),
            }
            return redirect(url_for("stock_transfer", step=2))
        else:
            data = session.pop("transfer", {})
            return render_template("stock_transfer_done.html", data=data)
    data = session.get("transfer", {})
    return render_template(f"stock_transfer_step{step}.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
