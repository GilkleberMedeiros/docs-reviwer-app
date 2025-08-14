from typing import Callable, Any, TypedDict, TypeVar
from datetime import datetime, timedelta
import functools


class RegistryData(TypedDict):
    last_call: datetime  # last_call timestamp
    left_time: timedelta  # left time from previous calls
    tokens: int


T = TypeVar("T")

# Bucket limiter calls registry
__REGISTRIES: dict[str, RegistryData] = {}


def __get_key(callable: Callable[..., T]) -> str:
    return callable.__qualname__ + ".." + str(callable.__annotations__)


def bucket_limiter(
    func: Callable[..., T] | None = None,
    /,
    *,
    interval: int = 120,
    earn_tokens: int = 2,
    bucket_size: int = 2,
) -> Any:
    registries = __REGISTRIES

    def internal(func: Callable[..., T], /) -> Any:
        @functools.wraps(func)
        def wrapper(*args: tuple[Any], **kwargs: dict[Any, Any]) -> Any:
            key = __get_key(func)
            was_in_registries = True

            # Registry resource in registry to keep track of their tokens and calls
            if key not in registries:
                was_in_registries = False
                registries[key] = {
                    "last_call": datetime.now(),
                    "left_time": timedelta(),  # left time from previous calls
                    "tokens": earn_tokens,
                }

            # If this is the first resource call (resource was just added to registry in above statement)
            if not was_in_registries:
                remains = registries[key]["tokens"]
                if remains > 0:
                    registries[key]["tokens"] -= 1

                    return func(*args, **kwargs)

                raise Exception(
                    f"RATE LIMITER: Resource {func.__qualname__} ran out of tokens."
                )

            last_call = registries[key]["last_call"]
            left_time = registries[key]["left_time"]
            now = datetime.now()

            # get time_passed including time left over from previous calls
            time_passed = (now - last_call) + left_time
            tspan = timedelta(seconds=interval)  # get interval as timedelta
            intervals_passed = (
                time_passed // tspan
            )  # get int number of intervals passed
            new_left_time = time_passed % tspan  # get new left time

            tokens = registries[key]["tokens"]
            # get new number of tokens or max tokens given bucket_size param
            registries[key]["tokens"] = min(
                tokens + (intervals_passed * earn_tokens), bucket_size
            )
            registries[key]["last_call"] = now
            registries[key]["left_time"] = new_left_time

            # verify left tokens and subtract if accepted
            if registries[key]["tokens"] > 0:
                registries[key]["tokens"] -= 1
                return func(*args, **kwargs)

            raise Exception(
                f"RATE LIMITER: Resource {func.__qualname__} ran out of tokens."
            )

        return wrapper

    return internal if func is None else internal(func)


def tokens_left(callable: Callable[..., T]) -> int:
    """
    Get number of tokens left for a [callable]. Returns 0 if [callable]
    is not registered/was never called through the decorator.
    """
    key = __get_key(callable)

    if not __REGISTRIES.get(key):
        return 0

    return __REGISTRIES[key]["tokens"]
