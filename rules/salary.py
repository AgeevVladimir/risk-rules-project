"""Simple salary restrictive rule."""


class SalaryRule:
    """Salary rule class."""

    def __init__(self, user_age: int, user_salary: int):
        self._user_age = user_age
        self._user_salary = user_salary

    def is_good_for_mortgage(self):
        """Check is user ok for mortgage."""
        if (self._user_age < 65 and self._user_age > 18) and (self._user_salary > 50000):
            return True
        return False
