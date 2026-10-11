# 02 APIs

About 30 minutes. An LLM is something you talk to through an API, so it's worth five
minutes on what an API call is before we make one to a model.

## The idea

An API is a menu that another program offers you. You send a request ("give me order
O-48291") and get back a response, usually as JSON. Every request has:

- a method: `GET` to read something, `POST` to create or change something
- a URL: where to send it, for example `http://localhost:9000/orders/O-48291`
- headers: extra notes on the envelope, such as your API key or an id for the request
- sometimes a body: the data you're sending, as JSON

Every response has a status code. You need four of them:

| Code | Meaning | In plain words |
| --- | --- | --- |
| 200 | OK | Here's what you asked for |
| 404 | Not found | I understood you, but that thing doesn't exist |
| 429 | Too many requests | Slow down (you'll meet this with free LLM tiers) |
| 500 | Server error | Something broke on my side, not yours |

JSON is just text that looks like a Python dict:

```json
{"order_id": "O-48291", "total_usd": 79.99, "status": "delivered"}
```

## A real API on your laptop

The kit comes with a small fake version of the Nimbus order system, in `mock_api/`. The
course uses the same one all month. Start it in its own terminal (activate the venv there
first) and leave it running:

```powershell
# from prep-kit/
uvicorn app:app --app-dir mock_api --port 9000
```

`uvicorn` is a small web server, `--app-dir mock_api` tells it which folder the code is in,
and `--port 9000` is the address on your laptop it listens on.

Now open <http://localhost:9000/docs> in your browser. That page is generated from the code
and lists every endpoint. Click `GET /orders/{order_id}`, then "Try it out", type `O-48291`
and press Execute. You just made an API call.

## The same thing from the terminal

```powershell
# Windows PowerShell
Invoke-RestMethod http://localhost:9000/orders/O-48291
```

```bash
# macOS / Linux (or curl.exe on Windows)
curl http://localhost:9000/orders/O-48291
```

## And from Python

In a second terminal, from `prep-kit/`:

```powershell
py code\hello_api.py
```

It sends five requests and prints each one with its status code:

1. Read an order that exists: 200.
2. Read one that doesn't: 404. The server answered fine. A 404 is information, not a crash.
3. Issue a refund with `POST`. The API insists on an `Idempotency-Key` header: an id for
   "this one refund" that the caller chooses.
4. Send the exact same refund again, as a retry after a timeout would. You get the same
   `refund_id` back, so the customer is refunded once, not twice. That property is called
   idempotency, and Session 6 is built on it.
5. Ask the server to fail on purpose with the `X-Chaos: error` header: 500. Real APIs fail,
   and the course makes them fail on purpose so you can practise handling it.

Open `code/hello_api.py` and read it. It's about 60 lines, and each request is one line of
`httpx`, a common Python HTTP library.

## Try this

- Change step 1 to order `O-77201`. What does that customer have?
- Remove the `Idempotency-Key` header from step 3. What status code comes back, and why?
- Run `hello_api.py` twice. Step 3 gets a new `refund_id` each run, but steps 3 and 4
  always match each other. Look at how the script makes the key to see why.

Next: [03 Secrets and .env](03-secrets-and-env.md)
