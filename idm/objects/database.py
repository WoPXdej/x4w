import os
import json
import traceback

from os.path import join as pjoin
from typing import List

from wtflog import warden

logger = warden.get_boy('База данных')

get_dir = os.path.dirname
core_path = get_dir(get_dir(get_dir(__file__)))
dir_path = pjoin(core_path, 'database')

db_gen: "DB_general"


def read(rel_path: str) -> dict:
    'Возвращает словарь из файла с указанным названием'
    try:
        path = pjoin(core_path, rel_path)
        logger.debug(f'Reading "{path}"')
        with open(path, "r", encoding="utf-8") as file:
            return json.loads(file.read())
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def write(rel_path, data):
    try:
        path = pjoin(core_path, rel_path)
        logger.debug(f'Writing to "{path}"')
        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e



class DB_defaults:

    settings: dict = {
        "silent_deleting": False
    }

    lp_settings: dict = {
        "ignored_users": [],
        "prefixes": [".л", "!л"],
        "binds": {},
        "key": ""
    }

    responses: dict = {
        "del_self": "&#13;",
        "del_process": "Deleting...",
        "del_success": "Deleted",
        "del_err_924": "❗ Не прокатило. Дежурный администратор? 🤔",
        "del_err_vk": "❗ Не прокатило. Ошибка VK:{ошибка}",
        "del_err_not_found": "❗ Не нашел сообщения для удаления 🤷‍♀",
        "del_err_unknown": "❗ Неизвестная ошибка при удалении 👀",
        "chat_subscribe": "Подключено<br>Идентификатор чата<br>{имя}<br>во вселенной ириса: {ид}",
        "chat_bind": "Чат '{имя}' успешно привязан!",
        "user_ret_ban_expired": "💚 Срок бана пользователя {ссылка} истек",
        "user_ret_process": "💚 Добавляю {ссылка}",
        "user_ret_success": "✅ Пользователь {ссылка} добавлен в беседу",
        "user_ret_err_no_access": "❗ Не удалось добавить {ссылка}.<br>Нет доступа.<br> Возможно, он не в моих друзьях или он уже в беседе",
        "user_ret_err_vk": "❗ Не удалось добавить пользователя {ссылка}.<br>Ошибка ВК.<br>",
        "user_ret_err_unknown": "❗ Не удалось добавить пользователя {ссылка}.<br>Произошла неизвестная ошибка",
        "to_group_success": "✅ Запись опубликована",
        "to_group_err_forbidden": "❗ Ошибка при публикации. Публикация запрещена. Превышен лимит на число публикаций в сутки, либо на указанное время уже запланирована другая запись, либо для текущего пользователя недоступно размещение записи на этой стене",
        "to_group_err_recs": "❗ Ошибка при публикации. Слишком много получателей",
        "to_group_err_link": "❗ Ошибка при публикации. Запрещено размещать ссылки",
        "to_group_err_vk": "❗ Ошибка при публикации. Ошибка VK:<br>{ошибка}",
        "to_group_err_unknown": "❗ Ошибка при публикации. Неизвестная ошибка",
        "repeat_forbidden_words": [
            "передать",
            "купить",
            "повысить",
            "завещание",
            "модер"
        ],
        "repeat_if_forbidden": "Я это писать не буду.",
        "ping_duty": "{ответ}<br>Ответ за {время}сек.",
        "ping_myself": "{ответ} CB<br>Получено через {время}сек.<br>ВК ответил за {пингвк}сек.<br>Обработано за {обработано}сек.",
        "ping_lp": "{ответ} LP<br>Получено через {время}сек.<br>Обработано за {обработано}сек.",
        "info_duty": "Информация о дежурном:<br>WoPX Beta v{версия}<br>Владелец: {владелец}<br>Чатов: {чаты}<br><br>Информация о чате:<br>Iris ID: {ид}<br>Имя: {имя}",
        "info_myself": "Информация о дежурном:<br>WoPX Beta v{версия}<br>Владелец: {владелец}<br>Чатов: {чаты}<br><br>Информация о чате:<br>Iris ID: {ид}<br>Имя: {имя}",
        "not_in_trusted": "Я тебе не доверяю 😑",
        "trusted_err_no_reply": "❗ Ошибка при выполнении, необходимо пересланное сообщение",
        "trusted_err_in_tr": "⚠ Пользователь уже в доверенных",
        "trusted_err_not_in_tr": "⚠ Пользователь не находился в доверенных",
        "trusted_success_add": "✅ Пользователь {ссылка} в доверенных",
        "trusted_success_rem": "✅ Пользователь {ссылка} удален из доверенных",
        "trusted_list": "Доверенные пользователи:"
    }

    @staticmethod
    def load_user(instance: "DB" = None) -> dict:
        if not instance:
            instance = DB
        return {
            "owner_id": instance.owner_id,
            "host": instance.host,
            "installed": instance.installed,
            "dc_auth": instance.dc_auth,
            "access_token": instance.access_token,
            "me_token": instance.me_token,
            "secret": instance.secret,
            "responses": instance.responses,
            "lp_settings": instance.lp_settings,
            "settings": instance.settings,
            "trusted_users": instance.trusted_users,
            "chats": instance.chats,
            "templates": instance.templates,
            "voices": instance.voices,
            "anims": instance.anims
        }


class DB_general:
    'костыль, пока нет компа почистить в коде все упоминания'

    owner_id: int = 0
    host: str = ""
    installed: bool = False
    dc_auth: bool = False

    def __init__(self):
        self.__dict__.update(read('database.json'))

    @staticmethod
    def update_general():
        global db_gen
        db_gen = DB_general()

    def set_user(self, user_id: int):
        self.owner_id = user_id
        self.save()
        self.update_general()
        return DB()

    def save(self) -> str:
        db = DB()
        db.owner_id = self.owner_id
        db.host = self.host
        db.installed = self.installed
        db.dc_auth =self.dc_auth
        return db.save()


class DB:
    'Класс, представляющий хранилище данных пользователя'
    gen: DB_general

    owner_id: int = 0
    host: str = ""
    installed: bool = False
    dc_auth: bool = False
    access_token: str = "Не установлен"
    me_token: str = "Не установлен"
    secret: str = ""
    chats: dict = {}
    trusted_users: List[int] = []
    duty_id: int = 0
    templates: List[dict] = []
    anims: List[dict] = []
    voices: List[dict] = []
    responses = DB_defaults.responses

    settings = DB_defaults.settings
    lp_settings = DB_defaults.lp_settings

    def __init__(self):
        self.gen = DB_general()
        self.duty_id = int(db_gen.owner_id)  # crap
        self.host = db_gen.host
        self.installed = db_gen.installed
        self.load_user()

    def load_user(self):
        self.__dict__.update(read('database.json'))

    def save(self) -> str:
        'Сохраняет данные пользователя в файл'
        logger.debug("Сохраняю базу данных")
        write('database.json', DB_defaults.load_user(self))
        return "ok"


def _update():
    # кто до сих пор не обновился с версии июля 2020 года - я не виноват
    gen = read('database/general.json')
    usr = read(f'database/{gen["owner_id"]}.json')
    write('database.json', dict(gen, **usr))


try:
    read('database.json')
except FileNotFoundError:
    write('database.json', DB_defaults.load_user())
    try:
        _update()
    except Exception:
        pass


DB_general.update_general()  # crap
