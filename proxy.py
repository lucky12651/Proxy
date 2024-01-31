from flask import Flask, request, Response
import requests

app = Flask(__name__)

headers = {
    'Content-Type': 'text/html; charset=utf-8',  # Allow all types of content
    'Access-Control-Allow-Origin': '*'
}

def proxy_request(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.RequestException as e:
        return f"Error: {e}"

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    base_url = request.args.get('url')
    
    if not base_url:
        return "URL parameter is missing", 400

    if request.method == 'GET':
        content = proxy_request(base_url)
        content_with_base_url = add_base_url_to_content(base_url, content)
        return Response(content_with_base_url, headers=headers)

    elif request.method == 'POST':
        url = request.form.get('url')
        response = proxy_request(url)
        content_with_base_url = add_base_url_to_content(url, response)
        return Response(content_with_base_url, headers=headers)

def add_base_url_to_content(base_url, content):
    # Modify content to include the base URL for static assets
    # This assumes that the base URL ends with a '/'
    return content.replace('<head>', f'<head><base href="{base_url}">')

if __name__ == '__main__':
    app.run(debug=True)
