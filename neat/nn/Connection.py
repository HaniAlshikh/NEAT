class Connection:
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to
        self.weight = 0
        self.enabled = True
