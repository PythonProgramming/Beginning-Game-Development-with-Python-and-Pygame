class StateMachine(object):

  def __init__(self):

      self.states = {} 	# Stores the states
      self.active_state = None  # The currently active state

  def add_state(self, state):

      # Add a state to the internal dictionary
      self.states[state.name] = state

  def think(self):

     # Only continue if there is an active state
     if self.active_state is None:
         return

     # Perform the actions of the active state, and check conditions
     self.active_state.do_actions()

     new_state_name = self.active_state.check_conditions()
     if new_state_name is not None:
         self.set_state(new_state_name)
 
  def set_state(self, new_state_name):

      # Change states and perform any exit / entry actions
      if self.active_state is not None:
          self.active_state.exit_actions()

      self.active_state = self.states[new_state_name]
      self.active_state.entry_actions()
