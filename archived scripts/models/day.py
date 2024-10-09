# the basic day class
class Day():
    def __init__(self, date, entry = None, goals = None, entry_id = None):
        self.date = date
        self.entry = entry
        self.goals = goals if goals is not None else {}
        self.day_num = self.get_day_num()
        self.entry_id = entry_id

    # sets the entry text for the day
    def set_entry(self, entry):
        self.entry = entry

    #returns the number of the day
    def get_day_num(self):
        day_num = self.date.day
        return day_num
    
    # adds the parts of the goals list to the goals dictionary, key = goal id, values = [goal description, state]
    def add_goals(self, goals_list):
        for goal in goals_list:
            id, description, state = goal
            self.goals[id] = [description, state]
