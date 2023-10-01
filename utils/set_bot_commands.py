from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота'),
            types.BotCommand('help', 'Отримати список команд'),
            types.BotCommand('get_user_by_id', 'Знайти користувача по ID'),
            types.BotCommand('get_user_by_name', 'Знайти користувача по імені'),
            types.BotCommand('add_me', 'Додати мене у список користувачів'),
            types.BotCommand('remove_me', 'Видалити мене зі списку користувачів'),
            types.BotCommand('update_user', 'Оновити дані про користувача')
        ]
    )
