class User:
    preferences = []
    visited_canvas = []
    visited_pearls = []
    name = ""
    def __init__(self, name, pref):
        self.name = name
        self.preferences = pref

