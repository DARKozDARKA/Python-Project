# Starts the game by creating the service container and state machine.

from infrastructure.all_services import AllServices
from infrastructure.game_state_machine import GameStateMachine
from infrastructure.states.bootstrap.bootstrap_state import BootstrapState

def main():
    services = AllServices.container()
    state_machine = GameStateMachine(services)
    state_machine.enter(BootstrapState)


if __name__ == "__main__":
    main()
