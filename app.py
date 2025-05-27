from flask import Flask, render_template_string
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('rent_data.json', 'r') as f:
        rent_data = json.load(f)
    results = []
    for zip_code, data in rent_data.items():
        avg_rent = data.get('summary', {}).get('avg_rent')
        if avg_rent and avg_rent > 3000:
            results.append({'zip': zip_code, 'avg_rent': avg_rent})
    html_template = """
    <html>
    <head><title>High Rent ZIP Codes</title></head>
    <body>
        <h1>ZIP Codes with Avg Rent Over $3,000</h1>
        <table border="1">
            <tr><th>ZIP Code</th><th>Avg Rent</th></tr>
            {% for item in results %}
            <tr><td>{{ item.zip }}</td><td>${{ "{:,.2f}".format(item.avg_rent) }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, results=results)

if __name__ == '__main__':
    app.run(debug=True)
