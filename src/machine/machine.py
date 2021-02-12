from typing import Any, Callable, Dict, List


class MachineError(Exception):
    """Intended to be raised if the current state of the machine cannot transition to another state requested by the trigger"""


class InvalidMachine(Exception):
    """Intended to be raised if the state machine would be infeasible"""


class Machine(object):
    """State Machine Implementation"""

    def __init__(
        self,
        model: object,
        transitions: List[Dict[str, Any]],
        initial_state: Any,
        skip_optional_validation: bool = True,
        add_is_state: bool = False,
    ):
        self.state = initial_state
        self.transitions = transitions
        self.model = model

        self.__validate_state_machine(skip_optional_validation)
        self.__wrap_triggers()

        if add_is_state:
            self.__add_is_state()

    def __add_is_state(self) -> None:
        """Utility method that adds multiple @property type methods to the given model class.
            The methods will be 'is_{state}' such as - is_stopped when one of the states
            supplied in either the sources or destinations is 'stopped'
        """
        states = set()
        for transition in self.transitions:
            states.add(transition["source"])
            states.add(transition["dest"])
        for state in list(states):
            setattr(self.model, f"is_{state}", lambda self: self.state == state)

    def __validate_state_machine(self, skip_optional_validation: bool) -> None:
        """Validates that the given transition list can produce a feasible state machine

        Args:
            skip_optional_validation (bool): Whether you want to skip the optional validations - eg you are doing lazy loading of methods etc

        Raises:
            InvalidMachine: If the state machine would be infeasible
        """
        triggers = set()
        sources = set()
        dests = set()

        # Checking structure of the transitions
        for transition in self.transitions:
            if not isinstance(transition, dict):
                raise InvalidMachine
            if not set(["trigger", "source", "dest"]) - set(transition.keys()) == set():
                raise InvalidMachine
            triggers.add(transition["trigger"])
            sources.add(transition["source"])
            dests.add(transition["dest"])

        # Check initial state is in the source
        if not (self.state in sources):
            raise InvalidMachine("Initial state is not in the 'source' value from the list of transitions")

        # Checking that there arent duplicate destinations for same trigger/source combo
        for trigger in list(triggers):
            available_transitions = list(filter(lambda t: (t["trigger"] == trigger), self.transitions))
            available_sources = set([t["source"] for t in available_transitions])
            for source in available_sources:
                available_transitions_from_source = list(
                    filter(lambda t: (t["source"] == source), available_transitions)
                )
                if len(available_transitions_from_source) != 1:
                    raise InvalidMachine(
                        f"Undetermined state change - cannot have multiple options for state change.\nChoose from: {available_transitions_from_source}"
                    )

        # Checking the model object has all triggers available
        for transition in self.transitions:
            if not hasattr(self.model, transition["trigger"]):
                raise InvalidMachine(f'Method trigger missing on model: {transition["trigger"]}')
        # Optional validation
        if not skip_optional_validation:
            # TODO: Optionally check we can return from all nodes?

            # Check we can get between all states - no nodes with zero order
            if dests != sources:
                raise InvalidMachine("Destination nodes != Source nodes")

    def __wrap_triggers(self) -> None:
        """Wraps all of the given triggers with the __wrapper functionality"""
        triggers = list(set([t["trigger"] for t in self.transitions]))
        for trigger in triggers:
            setattr(self.model, trigger, self.__wrapper(getattr(self.model, trigger)))

    def __wrapper(self, func: Callable) -> Callable:
        """Wrapper to wrap trigger functions with wrapped function"""

        def wrapped(*args, **kwargs):  # type: ignore
            """wrapped function that modifies the state of the machone based on the transitions

            Raises:
                MachineError: If the trigger tries to run functionality that it cannot escape due to state macchines transition setup
            """
            available_transitions = list(
                filter(lambda t: (t["trigger"] == func.__name__) and (t["source"] == self.state), self.transitions)
            )
            if len(available_transitions) == 0:
                raise MachineError(f"Cannot change state from: {self.state} using trigger {func.__name__}")
            self.state = available_transitions[0]["dest"]
            func(*args, **kwargs)

        return wrapped
