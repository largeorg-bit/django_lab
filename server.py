import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


HOST = "127.0.0.1"
PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES = {
    "/": "index.html",
    "/index": "index.html",
    "/index.html": "index.html",
    "/catalog": "catalog.html",
    "/catalog.html": "catalog.html",
    "/category": "category.html",
    "/category.html": "category.html",
    "/contacts": "contacts.html",
    "/contacts.html": "contacts.html",
    "/orders": "orders.html",
    "/orders.html": "orders.html",
}


class HttpHandler(BaseHTTPRequestHandler):
    """Обрабатывает GET и POST без фреймворков."""

    def do_GET(self):
        """Отдаёт запрошенную HTML-страницу."""
        filename = self.get_page_filename()
        if filename is None:
            self.send_html_page("404.html", status=404)
            return
        self.send_html_page(filename)

    def do_POST(self):
        """Принимает данные формы и печатает их в консоль."""
        length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(length)
        body = raw_body.decode("utf-8")

        print("Получен POST-запрос", flush=True)
        print(f"Путь: {self.path}", flush=True)
        print(f"Сырые данные: {body}", flush=True)

        parsed_data = parse_qs(body, keep_blank_values=True)
        if parsed_data:
            print("Разобранные поля:", flush=True)
            for field, values in parsed_data.items():
                print(f"{field}: {', '.join(values)}", flush=True)
        else:
            print("Поля формы отсутствуют", flush=True)

        filename = self.get_page_filename() or "contacts.html"
        self.send_html_page(filename)

    def get_page_filename(self):
        """Возвращает имя HTML-файла по пути запроса."""
        path = urlparse(self.path).path
        return PAGES.get(path)

    def send_html_page(self, filename, status=200):
        """Читает HTML-файл и отправляет его клиенту."""
        filepath = os.path.join(BASE_DIR, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as html_file:
                content = html_file.read()
        except FileNotFoundError:
            if filename != "404.html":
                self.send_html_page("404.html", status=404)
            else:
                self.send_error(404, "Страница не найдена")
            return
        except OSError:
            if filename != "500.html":
                self.send_html_page("500.html", status=500)
            else:
                self.send_error(500, "Внутренняя ошибка сервера")
            return

        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def run(server_class=HTTPServer, handler_class=HttpHandler):
    """Запускает HTTP-сервер."""
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен: http://{HOST}:{PORT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
