class Project:
    def __init__(self):
        self.book = None
        self.outputs = None
        self.Substitutions = None

    # todo implement factory method from_json, splits the dict accordingly and
    #      calls book, output and substition factory methods
