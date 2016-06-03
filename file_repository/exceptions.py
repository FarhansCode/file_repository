class Not200Response(Exception):
    def __init__(self, value):
        code, msg = value
    def __str__(self):
        return "file_repository responded with %s, %s" % (self.code, self.msg)
