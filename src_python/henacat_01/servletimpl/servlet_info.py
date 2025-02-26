class ServletInfo:
    def __init__(self, web_app, url_pattern, servlet_class_name):
        self.webApp = web_app
        self.urlPattern = url_pattern
        self.servletClassName = servlet_class_name
        self.servlet = None
