class User:
    
    preferences = []
    canvas_in_pearl_counter = []
    visited_canvas = []
    visited_pearls = []
    name = ""
    total_awareness = 0
    
    def __init__(self, name, pref, route):
        self.name = name
        self.preferences = pref

        for i in range(len(route)):
            self.canvas_in_pearl_counter.append(int(0))

