class FSMController:
    def __init__(self, state):
        self.state = state

    async def finish(self):
        await self.state.clear()

    async def reset_and_start(self, new_state):
        await self.state.clear()
        await self.state.set_state(new_state)

