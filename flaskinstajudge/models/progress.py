class ExecutionRecoder():

    can_show_progress = False
    index = 0


    def __init__(self, state_list):
            self.states = state_list
            self.length = len(states)

    def open(self):
        self.can_show_progress = True



    def close(self):
        self.can_show_progress = False
        self.index = 0

    def update_state(self):
        if self.index < self.length:
            self.index += 1

    def skip_to_end(self):
        self.index = self.length

    def get_update(self):
        update = { 
            "current": None,
            "done": [],
            "left": []
        }

        for i,state in enumerate(self.states):
            if i < self.index:
                update["done"].append(state)
            elif i > self.index:
                update["left"].append(state)
            else:
                update["current"] = state

        return update


    