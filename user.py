class User:
    id = 0


    def __init__(self, name, pref, route, color):
        self.name = name
        self.preferences = pref
        self.id += 1
        self.canvas_in_pearl_counter = []
        self.visited_canvas = [] 
        self.preferences = []
        self.visited_canvas = []
        self.visited_pearls = []
        self.awareness = []
        self.satisfaction = []
        self.change_pearl_satisfaction_value = []
        self.change_pearl_counter = 0
        self.color = color
        
        for i in range(len(route)):
            self.canvas_in_pearl_counter.append(int(0))
