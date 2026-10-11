"""Module 02: talk to a real (local) API with Python.

First start the mock Nimbus order API in its own terminal and leave it running.
From prep-kit/:

    uvicorn app:app --app-dir mock_api --port 9000

Then, in a second terminal, also from prep-kit/:

    py code\\hello_api.py

Five requests, five lessons. Nothing here touches the internet or costs money.
"""
from __future__ import annotations

import json
import os
import uuid

import httpx

BASE_URL = os.getenv("MOCK_ORDER_API_URL", "http://localhost:9000")


def show(title: str, response: httpx.Response) -> None:
    print(f"\n=== {title}")
    print(f"{response.request.method} {response.request.url}")
    print(f"-> status {response.status_code} {response.reason_phrase}")
    try:
        print(json.dumps(response.json(), indent=2))
    except ValueError:
        print(response.text)


def main() -> None:
    with httpx.Client(base_url=BASE_URL, timeout=5) as api:
        try:
            api.get("/docs")
        except httpx.ConnectError:
            print(f"Nothing is listening at {BASE_URL}.")
            print("Start the mock API first (see the top of this file), then run me again.")
            return

        # 1. GET reads something. 200 means "here it is".
        show("1. Read an order that exists", api.get("/orders/O-48291"))

        # 2. A 404 is not a crash: the server answered, the thing just isn't there.
        show("2. Read an order that doesn't exist", api.get("/orders/O-00000"))

        # 3. POST changes something. A refund is money leaving the store, so the API demands an
        #    Idempotency-Key: a unique id for "this one refund", chosen by the caller.
        key = f"prep-kit-{uuid.uuid4().hex[:8]}"
        body = {"order_id": "O-48291", "amount_usd": 79.99}
        show("3. Issue a refund", api.post("/refunds", json=body, headers={"Idempotency-Key": key}))

        # 4. Send the exact same request again (as a retry would). Same key -> same refund_id,
        #    so the customer is refunded once, not twice.
        show("4. Retry with the SAME key", api.post("/refunds", json=body,
                                                    headers={"Idempotency-Key": key}))

        # 5. Real APIs fail. The mock can fail on purpose: the X-Chaos header asks it to.
        show("5. Ask the server to fail (500)", api.get("/orders/O-48291",
                                                        headers={"X-Chaos": "error"}))

    print("\nCompare refund_id in steps 3 and 4: identical. That is idempotency.")
    print(f"Now open {BASE_URL}/docs in your browser: every endpoint, with a 'Try it out' button.")


if __name__ == "__main__":
    main()
