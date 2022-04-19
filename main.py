"""Main entrypoint."""
import importlib
import logging
import typing

import fastapi
import pydantic

import settings
from helpers import generic as generic_helpers
from helpers import strategy as strategy_helpers


LOGGER_OBJ: typing.Final[logging.Logger] = logging.getLogger(__file__)
WEB_APP: typing.Final[fastapi.FastAPI] = fastapi.FastAPI()
STRATEGY_LIST: typing.Final[list[str]] = generic_helpers.fetch_all_file_names_from_project_dir(settings.STRATEGIES_DIR)
LOGGER_OBJ.warning(f"Available strategies is: {STRATEGY_LIST}")


@WEB_APP.post("/api/run-strategy/{strategy_name}/")
def run_strategy_dynamic_view(strategy_name: str, strategy_payload: dict = fastapi.Body(...)):
    if strategy_name not in STRATEGY_LIST:
        LOGGER_OBJ.error(f"Strategy name {strategy_name} does not exist")
        raise fastapi.HTTPException(status_code=404)

    try:
        strategy_module: typing.Any = importlib.import_module(f"strategies.{strategy_name}")
    except ModuleNotFoundError as exc:
        LOGGER_OBJ.error(f"This possibly may never happens, but never say never: {exc}")
        raise fastapi.HTTPException(status_code=500)

    try:
        real_strategy: strategy_helpers.GenericStrategyProtocol = strategy_module.CurrentStrategy(strategy_payload)
        return real_strategy.prepare().run_strategy().finalize()
    except pydantic.ValidationError as exc:
        LOGGER_OBJ.error(f"Payload for strategy is mailformed: {exc}")
        raise fastapi.HTTPException(status_code=400)
    except strategy_helpers.StrategyGenericException as exc:
        LOGGER_OBJ.error(f"Strategy fail reason: {exc}")
        raise fastapi.HTTPException(status_code=500)
