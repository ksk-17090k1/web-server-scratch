class ServletException(Exception):
    def __init__(self, message=None, root_cause=None):
        super().__init__(message)
        self.root_cause = root_cause
