from prompt_toolkit.shortcuts import dialogs
from json import loads, dumps
from sys import exit, orig_argv, platform
from colorama import init, deinit, Fore
from hashlib import sha256
from subprocess import run
from getpass import getpass
from os import chdir, listdir, mkdir, rmdir, system, remove
from os.path import isfile, isdir, dirname, exists
from traceback import format_exception
init()
get_exc_data = lambda exc: format_exception(exc)[-1].strip().split(": ")
def shutdown():
    print("Завершение работы NosokOS...")
    print("(при завершении работы все несохранённые данные будут удалены)")
    deinit()
    exit()
def reboot():
    print("Перезагрузка NosokOS...")
    print("(при перезагрузке все несохранённые данные будут удалены)")
    deinit()
    chdir(dirname(__file__))
    run(orig_argv)
    exit()
def nosokos_error(err_type, err_data="(не указано)", exc_type="(не указан)", exc_desc="(не указано)"):
    match err_type:
        case "setting":
            dialogs.message_dialog(
                "Ошибка файла настроек",
                f"Некорректная настройка: {err_data} - {settings[err_data]}"
            ).run()
        case "unknown":
            dialogs.message_dialog(
                "Неизвестная ошибка",
                f"Произошла неизвестная ошибка. Описание ошибки: {err_data}"
            ).run()
        case "critical":
            dialogs.message_dialog(
                "Критическая ошибка",
                "Возникла критическая ошибка в работе системы."
                f"\nТип исключения Python: {exc_type}"
                f"\nОписание исключения Python: {exc_desc}"
            ).run()
        case _:
            dialogs.message_dialog(
                "Косяк разраба",
                "Разрабом системы был допущен косяк. Пожалуйста, напишите ему об этом в телегу:"
                "\n@nosok333yt и предоставьте следующие данные ошибки:"
                f"\nТип ошибки: {err_type}"
                f"\nОписание ошибки: {err_data}"
                f"\nТип исключения Python: {exc_type}"
                f"\nОписание исключения Python: {exc_desc}"
                "\nЭто может помочь."
            ).run()
    restart = dialogs.button_dialog(
        "Выбор действия",
        "Выберите желаемое действие.",
        buttons=[
            (
                "Завершить работу системы",
                "shutdown",
                "[",
                "]",
                0
            ),
            (
                "Перезагрузить систему",
                "reboot",
                "[",
                "]",
                0
            )
        ]
    ).run()
    match restart:
        case "shutdown":
            shutdown()
        case "reboot":
            reboot()
        case _:
            nosokos_error("unknown", "unknown")
def set_setting(name, value):
    settings[name] = value
    settings_ = open("settings.json", "w", encoding="UTF-8")
    settings_.write(dumps(settings, ensure_ascii=False, indent=4))
    settings_.close()
    print(f"Были {Fore.YELLOW}изменены настройки{Fore.RESET}. Для полного принятия изменений рекомендуется {Fore.YELLOW}перезагрузить систему{Fore.RESET}.")
def create_user(name, pass_, lvl):
    new_user = {
        "name": name,
        "pass": sha256(pass_.encode()).hexdigest(),
        "level": lvl
    }
    users.append(new_user)
    users_ = open("users.json", "w", encoding="UTF-8")
    users_.write(dumps(users, ensure_ascii=False, indent=4))
    users_.close()
    print(f"{Fore.LIGHTYELLOW_EX}Создан пользователь{Fore.RESET} под именем {Fore.LIGHTGREEN_EX}{new_user['name']}{Fore.RESET}.")
def initial_setup():
    dialogs.message_dialog(
        "Добро пожаловать в NosokOS",
        "Спасибо за установку NosokOS! Требуется начальная настройка, чтобы пользоваться системой.",
        "Далее"
    ).run()
    default_username = settings["defaults"]["username"]
    username = dialogs.input_dialog(
        "Создание аккаунта администратора",
        f"Начнём с создания аккаунта. Введите имя для него. Если нажмёте Отмена, будет выбрано имя \"{default_username}\".",
        "Далее"
    ).run()
    if username is None:
        username = default_username
    elif not username.strip():
        username = default_username
    else:
        username = username.strip()
    default_password = settings["defaults"]["password"]
    password = dialogs.input_dialog(
        f"Установка пароля для {username}",
        f"Теперь нужно установить пароль. Введите его, и нажмите Далее. При нажатии кнопки Отмена будет выбран пароль \"{default_password}\"",
        "Далее",
        password=True
    ).run()
    if password is None:
        password = default_password
    default_pcname = settings["defaults"]["pcName"]
    pcname = dialogs.input_dialog(
        "Выбор имени компьютера",
        f"Выберем имя для компьютера. Пока оно используется только в декоративных целях. По умолчанию выберется имя \"{default_pcname}\"",
        "Далее"
    ).run()
    if pcname is None:
        pcname = default_pcname
    elif not pcname.strip():
        pcname = default_pcname
    else:
        pcname = pcname.strip()
    lvl = dialogs.button_dialog(
        "Уровень разрешений пользователя",
        "Ах да, чуть не забыл. Нужно настроить уровень разрешений для вашего аккаунта. Выберите один из них, нажав на кнопку ниже.",
        buttons=[
            (
                "Обычный пользователь (0)",
                0,
                "",
                "",
                0
            ),
            (
                "Администратор (1)",
                1,
                "",
                "",
                0
            ),
            (
                "Владелец системы (2)",
                2,
                "",
                "",
                0
            )
        ]
    ).run()
    if lvl == 0:
        msg = [
            "Был выбран режим обычного пользователя. Для первого аккаунта требуется как минимум",
            "уровень 1. Поэтому режим изменён на режим администратора."
        ]
        lvl = 1
        dialogs.message_dialog(
            "Внимание",
            "\n".join(msg),
            "Далее"
        ).run()
    dialogs.message_dialog(
        "Ура!",
        "Первоначальная настройка закончена. Можно смело пользоваться системой!",
        "Перезагрузиться"
    ).run()
    print("Создание пользователя...")
    create_user(username, password, lvl)
    print("Сохранение настроек...")
    set_setting("pcName", pcname)
    set_setting("setup", 1)
    print("Готово.")
    reboot()
def login():
    name = input("Введите имя: ")
    for user in users:
        if name == user["name"]:
            break
    else:
        print(f"Пользователь {Fore.LIGHTRED_EX}не найден{Fore.RESET}.")
        return login()
    passw = sha256(getpass("Введите пароль: ").encode()).hexdigest()
    if passw == user["pass"]:
        print(f"Выполнен {Fore.LIGHTYELLOW_EX}вход в систему{Fore.RESET} от имени {Fore.LIGHTGREEN_EX}{user["name"]}{Fore.RESET}.")
        return user["name"]
    else:
        print(f"{Fore.LIGHTRED_EX}Неверный{Fore.RESET} пароль.")
        return login()
def get_cwd():
    from os import getcwd
    to_return = getcwd()
    del getcwd
    return to_return
def print_help(what):
    try:
        # источник: Яндекс.Алиса (YandexGPT) (также я отредактировал)
        # (
        list_of_tuples = list(aliases.items())
        for key, value in list_of_tuples:
            if what in value or what in key:
                break
        else:
            key = None
        # )
        if key:
            help_ = helps[key]
        else:
            help_ = helps[what]
        if key == "dir":
            print("\n".join(help_) % (Fore.GREEN, Fore.RESET, Fore.YELLOW, Fore.RESET))
            return
    except KeyError:
        print(f"Помощь для команды {Fore.LIGHTRED_EX}{what}{Fore.RESET} не найдена.")
        return
    print("\n".join(help_))
def main():
    global settings, users, helps, aliases
    print("Запуск NosokOS...")
    settings = loads(open("settings.json", encoding="UTF-8").read())
    users = loads(open("users.json", encoding="UTF-8").read())
    helps = loads(open("helps.json", encoding="UTF-8").read())
    aliases = loads(open("aliases.json", encoding="UTF-8").read())
    match settings["setup"]:
        case 0:
            initial_setup()
        case 1:
            pass
        case _:
            nosokos_error("setting", "setup")
    username = login()
    while True:
        cwd = get_cwd()
        cmd = input(f"{Fore.LIGHTGREEN_EX}{username}{Fore.WHITE}@{Fore.YELLOW}{settings["pcName"]}{Fore.WHITE}:{Fore.LIGHTMAGENTA_EX}{cwd}{Fore.WHITE} & {Fore.RESET}")
        cmd_argv = cmd.split(" ")
        if cmd_argv[0] not in settings["single_cmds"] and len(cmd_argv) == 1 and cmd_argv[0] in helps.keys():
            print_help(cmd_argv[0])
            continue
        match cmd_argv[0]:
            case "shutdown":
                shutdown_mode = cmd_argv[1]
                match shutdown_mode:
                    case "s":
                        shutdown()
                    case "r":
                        reboot()
                    case _:
                        print(f"{Fore.LIGHTRED_EX}Неверный{Fore.RESET} режим завершения работы: {Fore.YELLOW}{shutdown_mode}{Fore.RESET}")
                        print_help("shutdown")
            case "help":
                help_cmd = cmd_argv[1]
                print_help(help_cmd)
            case "cd":
                path = cmd.partition(" ")[2]
                try:
                    chdir(path)
                except FileNotFoundError:
                    print(f"Не найден файл или папка: {Fore.LIGHTYELLOW_EX}{path}{Fore.RESET}.")
            case "dir" | "ls" | "lf":
                files = listdir()
                for file in files:
                    if isfile(file):
                        print(Fore.GREEN + file)
                    elif isdir(file):
                        print(Fore.YELLOW + file)
                    else:
                        print(Fore.WHITE + file)
                print(Fore.RESET, end="")
            case "poweroff" | "exit":
                shutdown()
            case "reboot" | "restart":
                reboot()
            case "mkfile" | "touch":
                files = cmd_argv[1:]
                if len(files) == 0:
                    print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: не дан список файлов для создания.")
                    print(f"Помощь по созданию файлов: {Fore.LIGHTYELLOW_EX}help mkfile{Fore.RESET}")
                    continue
                mk = []
                for file in files:
                    if not exists(file):
                        try:
                            open(file, "w", encoding="UTF-8").close()
                            mk.append(file)
                        except PermissionError:
                            print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: недостаточно прав для создания файла ({file}).")
                    else:
                        print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: файл ({file}) уже существует.")
                print(f"Создан(-ы) файл(-ы) ({len(mk)}): {", ".join(mk)}")
            case "mkdir":
                dirs = cmd_argv[1:]
                if len(dirs) == 0:
                    print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: не дан список папок для создания.")
                    print(f"Помощь по созданию папок: {Fore.LIGHTYELLOW_EX}help mkdir{Fore.RESET}")
                    continue
                mk_ = []
                for dir_ in dirs:
                    try:
                        mkdir(f"{get_cwd()}\\{dir_}")
                        mk_.append(dir_)
                    except FileExistsError:
                        print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: папка ({dir_}) уже существует.")
                print(f"Создан(-а/ы) папк(-а/и) ({len(mk_)}): {", ".join(mk_)}")
            case "rmdir":
                dirs = cmd_argv[1:]
                if len(dirs) == 0:
                    print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: не дан список папок для удаления.")
                    print(f"Помощь по удалению папок: {Fore.LIGHTYELLOW_EX}help rmdir{Fore.RESET}")
                    continue
                rm = []
                for dir_ in dirs:
                    try:
                        rmdir(dir_)
                        rm.append(dir_)
                    except FileNotFoundError:
                        print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: папка ({dir_}) не найдена.")
                    except OSError:
                        if not isdir(dir_):
                            print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: {Fore.GREEN}{dir_}{Fore.RESET} не является папкой.")
                        else:
                            print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: папка ({dir_}) не пуста.")
                print(f"Удален(-а/ы) папк(-а/и) ({len(rm)}): {", ".join(rm)}")
            case "cmd" | "wincmd" | "cmdwin" | "win":
                system("cmd")
            case "sfc":
                file_ = cmd_argv[1]
                fc = open(file_, encoding="UTF-8").read()
                print(f"Контент файла {file_}:\n{fc}")
            case "pfc":
                file__ = cmd_argv[1]
                if len(cmd_argv) == 3:
                    limit = int(cmd_argv[2])
                else:
                    limit = 1000
                content = []
                content_ = open(file__, encoding="UTF-8").read()
                lenfile = len(open(file__, encoding="UTF-8").read())
                if limit < lenfile:
                    for i in range(limit):
                        symb = content_[i]
                        content.append(symb)
                    print(f"Контент файла {file__} ({limit}):\n{"".join(content)}\n...")
                else:
                    print(f"Контент файла {file__}:\n{open(file__, encoding="UTF-8").read()}")
            case "rm" | "del" | "remove" | "delete" | "rmfile":
                files_ = cmd_argv[1:]
                if len(files_) == 0:
                    print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: не дан список файлов для удаления.")
                    print(f"Помощь по удалению файлов: {Fore.LIGHTYELLOW_EX}help del{Fore.RESET}")
                    continue
                rm_ = []
                for _file_ in files_:
                    try:
                        if isdir(_file_):
                            list_dir_files = listdir(_file_)
                            for dir_file in list_dir_files:
                                remove(dir_file)
                            rmdir(_file_)
                            rm_.append(_file_)
                        else:
                            remove(_file_)
                            rm_.append(_file_)
                    except FileNotFoundError:
                        print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: файл ({_file_}) не найден.")
                    except PermissionError:
                        print(f"{Fore.LIGHTRED_EX}ОШИБКА{Fore.RESET}: недостаточно прав для удаления файла ({_file_}).")
                    print(f"Удал(-ён/ены) файл(-ы) ({len(rm_)}): {", ".join(rm_)}")
            case _:
                if isfile(f"{get_cwd()}\\{cmd_argv[0]}"):
                    if cmd_argv[1:]:
                        system(f"{cmd_argv[0]} " + " ".join([arg for arg in cmd_argv[1:]]))
                    else:
                        system(cmd_argv[0])
                else:
                    print(f"{Fore.LIGHTRED_EX}{cmd_argv[0]}{Fore.RESET} не является верной командой или исполняемым файлом.")
if __name__ == "__main__":
    if platform != "win32":
        print("NosokOS доступен только под управлением Windows.")
        input("Нажмите Enter чтобы выйти.")
        exit()
    try:
        main()
    except SystemExit:
        exit()
    except (KeyboardInterrupt, EOFError) as e:
        dialogs.yes_no_dialog(
            "Экстренное выключение",
            "Вы уверены, что хотите выключить компьютер?",
            no_text="Да"
        ).run()
        print("\n" if type(e) == KeyboardInterrupt else "", end="")
        print("Экстренное выключение...")
        exit()
    except BaseException as e:
        exc_data = get_exc_data(e)
        nosokos_error("critical", exc_type=exc_data[0], exc_desc=exc_data[1])