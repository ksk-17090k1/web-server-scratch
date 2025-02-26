class HttpServlet:
    def do_get(self, req, resp):
        pass

    def do_post(self, req, resp):
        pass

    def service(self, req, resp):
        if req.get_method() == "GET":
            self.do_get(req, resp)
        elif req.get_method() == "POST":
            self.do_post(req, resp)
