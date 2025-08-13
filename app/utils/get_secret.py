import os
from decouple import config
from pydantic import SecretStr
import getpass


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


def get_secret(name: str) -> SecretStr:
    DOTENV_PATH = os.path.join(BASE_DIR, ".env")

    env_secret = os.environ.get(name, None)
    if env_secret:
        return SecretStr(env_secret)

    file_secret = config(  # type: ignore
        name, default=None, cast=str, repository=DOTENV_PATH
    )
    if file_secret:
        return SecretStr(file_secret)  # type: ignore

    cli_secret = getpass.getpass(f"Secret [{name}]: ")
    if cli_secret:
        return SecretStr(cli_secret)

    raise Exception(
        f"Couldn't get secrect named {name}! "
        "Tried system env variables, .env file and prompting user for secret. "
        f"\nUser prompted invalid secret: {cli_secret}"
    )
