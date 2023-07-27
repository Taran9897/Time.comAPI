import http.server
import http.client
import json
import re

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/getTimeStories":
            html_content = self.fetch_stories()
            if html_content:
                headlines, links = self.extract_stories(html_content)
                formatted_output = self.format_output(headlines, links)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(formatted_output.encode())
            else:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_message = {"error": "Failed to fetch data from Time.com."}
                self.wfile.write(json.dumps(error_message).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def fetch_stories(self):
        connection = http.client.HTTPSConnection("time.com")
        connection.request("GET", "/")
        response = connection.getresponse()

        if response.status != 200:
            return None

        data = response.read().decode("utf-8")
        connection.close()
        return data

    def extract_stories(self, html_content):
        headline_pattern = r'<h3 class="title">(.+?)<\/h3>'
        link_pattern = r'<a href="(\/[^"]+)">'

        headlines = re.findall(headline_pattern, html_content)[:7]
        links = re.findall(link_pattern, html_content)[:7]

        return headlines, links

        # headline_pattern = r'<h3 class="title">(.+?)<\/h3>'
        # link_pattern = r'<a href="(\/[^"]+)">'

        # headlines = re.findall(headline_pattern, html_content)[:6]
        # links = re.findall(link_pattern, html_content)[:6]

        # return headlines, links



    def format_output(self, headlines, links):
        output = "["
        for i in range(len(headlines)):
            output += f'\n{{\n"title": "{headlines[i].strip()}", "link": "https://time.com{links[i]}"\n}},'
        output = output.rstrip(',') + "\n]"
        return output

if __name__ == "__main__":
    http.server.HTTPServer(("localhost", 80), SimpleHTTPRequestHandler).serve_forever()
