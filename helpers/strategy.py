"""Basic strategy lies here."""
import typing

import pydantic


GENERIC_INPUT_TYPE = typing.TypeVar("GENERIC_INPUT_TYPE")
GENERIC_OUTPUT_TYPE = typing.TypeVar("GENERIC_OUTPUT_TYPE")


class BaseStrategy(typing.Generic[GENERIC_INPUT_TYPE, GENERIC_OUTPUT_TYPE]):
    """Base strategy parent."""

    INPUT_MODEL: pydantic.BaseModel
    OUTPUT_MODEL: pydantic.BaseModel
    _inner_result_buf: dict

    def __init__(self, payload: dict):
        self._payload: dict = payload

    def prepare(self) -> "BaseStrategy":
        """Basic prepare for every strategy."""
        self._prepared_payload: GENERIC_INPUT_TYPE = self.INPUT_MODEL(**self._payload)
        return self

    def finalize(self) -> GENERIC_OUTPUT_TYPE:
        """Finalize output for our fancy strategy."""
        return self.OUTPUT_MODEL(**self._inner_result_buf)


class GenericStrategyProtocol(typing.Protocol):
    def prepare(self) -> "GenericStrategyProtocol":
        ...

    def finalize(self) -> "GenericStrategyProtocol":
        ...

    def run_strategy(self) -> "GenericStrategyProtocol":
        ...


class StrategyGenericException(Exception):
    """Our fancy generic error."""
