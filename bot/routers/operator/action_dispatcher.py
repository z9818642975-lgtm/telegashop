from aiogram import Router
from aiogram.types import CallbackQuery

from bot.actions.operator import OperatorAction
from bot.constants.action_cb import ActionCB

router = Router(name="operator_action_dispatcher")


# реестр действий
ACTION_HANDLERS = {}


def register(action: OperatorAction):
    def wrapper(func):
        ACTION_HANDLERS[action.value] = func
        return func
    return wrapper


@router.callback_query(ActionCB.filter())
async def dispatch_action(
    cb: CallbackQuery,
    callback_data: ActionCB,
    session,
    user,
    state,
):
    handler = ACTION_HANDLERS.get(callback_data.action)

    if not handler:
        await cb.answer("⛔ Действие не поддерживается", show_alert=True)
        return

    await handler(cb, callback_data, session, user, state)

