import os
from decouple import config
from pydantic import SecretStr
import getpass

from services.logging import Log, LEVEL


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
REL_LOG_ORIGIN = "utils.get_secret"


def get_secret(name: str) -> SecretStr:
    DOTENV_PATH = os.path.join(BASE_DIR, ".env")
    LOG_ORIGIN = REL_LOG_ORIGIN + ".get_secret"

    log1 = Log(
        LEVEL.INFO,
        f"Trying to get secret {name} from os system env variables.",
        LOG_ORIGIN,
    )
    print(log1)

    env_secret = os.environ.get(name, None)
    if env_secret:
        log4 = Log(
            LEVEL.SUCCESS,
            f"Successful retrived secret {name} from os system env variables!",
            LOG_ORIGIN,
        )
        print(log4)

        return SecretStr(env_secret)

    log2 = Log(LEVEL.INFO, f"Trying to get secret {name} from dotenv file.", LOG_ORIGIN)
    print(log2)

    file_secret = config(  # type: ignore
        name, default=None, cast=str, repository=DOTENV_PATH
    )
    if file_secret:
        log5 = Log(
            LEVEL.SUCCESS,
            f"Successful retrived secret {name} from dotenv file!",
            LOG_ORIGIN,
        )
        print(log5)

        return SecretStr(file_secret)  # type: ignore

    log3 = Log(
        LEVEL.INFO,
        f"Trying to get secret {name} from terminal by prompting user.",
        LOG_ORIGIN,
    )
    print(log3)

    cli_secret = getpass.getpass(f"Secret [{name}]: ")
    if cli_secret:
        log6 = Log(
            LEVEL.SUCCESS,
            f"Successful retrived secret {name} from terminal by prompting user!",
            LOG_ORIGIN,
        )
        print(log6)

        return SecretStr(cli_secret)

    raise Exception(
        f"Couldn't get secrect named {name}! "
        "Tried system env variables, .env file and prompting user for secret. "
        f"\nUser prompted invalid secret: {cli_secret}"
    )
