Demo dynamic strategies and rules
==

#### Quickstart
1. Prepare python environment via this guide https://confluence.raiffeisen.ru/display/PC/Quickstart
1. Pull this repo
1. Run `poetry install`
1. Run `poetry shell`
1. Run `uvicorn main:WEB_APP --reload`
1. Then run this request via raw curl or via postman (just import this code and press «send»):
    ```bash
    curl --location --request POST 'http://127.0.0.1:8000/api/run-strategy/cashout/' \
    --header 'Accept: application/json' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "cash_in_your_hands": 10,
        "age": 30,
        "salary": 50001,
        "floor": 23,
        "rooms": 2,
        "square": 60
    }'
    ```
