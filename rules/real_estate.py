"""Real estate restrictive rule."""


class RealEstateRule:
    """Real estate rule class."""

    BASE_PRICE_FOR_1SQM: int = 3000

    def __init__(self, rooms: int, floor: int, square: int):
        self._rooms = rooms
        self._floor = floor
        self._square = square

    def can_be_sold(self) -> bool:
        """Check can we sold property."""
        if self._rooms > 0 and self._floor != 13:
            return True
        return False

    def _calc_average_price(self) -> int:
        return self.BASE_PRICE_FOR_1SQM * self._square

    def is_best_price(self, price: int) -> bool:
        """Price rule."""
        if price == self._calc_average_price():
            return True
        return False
