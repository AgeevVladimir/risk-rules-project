"""Important strategy."""
import logging
import typing

import pydantic

from helpers import strategy as strategy_helpers
from rules.real_estate import RealEstateRule
from rules.salary import SalaryRule


LOGGER_OBJ: typing.Final[logging.Logger] = logging.getLogger(__file__)


class InputModel(pydantic.BaseModel):
    """Base input model."""

    cash_in_your_hands: int
    age: int
    salary: int
    square: int
    floor: int
    rooms: int


class OutputModel(pydantic.BaseModel):
    """Base output model."""

    average_score: float
    client_rate: int


class CurrentStrategy(strategy_helpers.BaseStrategy[InputModel, OutputModel]):
    """Basic strategy for every startup."""

    INPUT_MODEL: typing.Type[InputModel] = InputModel
    OUTPUT_MODEL: typing.Type[OutputModel] = OutputModel
    _inner_result_buf: dict[str, int | float] = {}

    def check_mortgage_state(self) -> "CurrentStrategy":
        """Process via salary rule."""
        if not SalaryRule(self._prepared_payload.age, self._prepared_payload.salary).is_good_for_mortgage():
            raise strategy_helpers.StrategyGenericException("Salary/mortgage rule breaks")
        self._inner_result_buf["client_rate"] = 10
        return self

    def check_is_ok_for_cashout(self) -> "CurrentStrategy":
        """Main method for every startuper."""
        rule_prepared: RealEstateRule = RealEstateRule(
            self._prepared_payload.rooms, self._prepared_payload.floor, self._prepared_payload.square
        )
        if not rule_prepared.can_be_sold():
            raise strategy_helpers.StrategyGenericException(
                "Possibly current real estate is not aproppriate for this user"
            )
        if not rule_prepared.is_best_price(self._prepared_payload.cash_in_your_hands):
            LOGGER_OBJ.error("There is no money on your account, but this is not blocker for our decisions")
        self._inner_result_buf["average_score"] = 1.1
        return self

    def run_strategy(self) -> "CurrentStrategy":
        """Main entry point for strategy.

        Must be in the protocol?
        """
        self.check_mortgage_state().check_is_ok_for_cashout()
        return self
