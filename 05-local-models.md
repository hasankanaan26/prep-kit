# 05 Local models

About 30 minutes, most of it waiting for a download. You'll run a language model on your
own laptop: no key, no account, no internet once it's downloaded, and no bill.

## Why bother

- It's free, so you can make as many calls as you like.
- Nothing leaves your machine. That matters at companies that can't send data to a cloud.
- It shows you what a model is: a big file of numbers and a program that runs it.

The catch is that a model small enough for a laptop is much weaker than the cloud ones.
You'll see that for yourself in step 07.

## Install Ollama

Ollama downloads models and runs them behind the same OpenAI-compatible API you used in
step 04.

1. Download it from <https://ollama.com/download> and install it. On Windows and macOS it
   runs in the background (look for the llama icon).
2. In a terminal:

```powershell
ollama pull llama3.2        # about 2 GB, a 3-billion-parameter model
ollama run llama3.2 "Say hello in five words."
```

Pick by memory (RAM):

| Your laptop has | Try |
| --- | --- |
| 8 GB | `llama3.2` (2 GB) |
| 16 GB or more | `gemma3:4b` (3.3 GB) as well, and compare |

If you pull a different model, set `OLLAMA_MODEL` in `prep-kit/.env` to its name.
`ollama list` shows what you have.

## The same script, now local

```powershell
py code\chat.py --provider ollama "Explain what an API is in one sentence."
```

Same code as step 04. Only the address changed, from Google's servers to
`localhost:11434`. The first call is slow (10 to 20 seconds) because the model is loaded
into memory. Later calls are much faster.

Now turn off Wi-Fi and run it again. It still works.

## If something went wrong

| You see | Try |
| --- | --- |
| `Can't reach Ollama` | Start the Ollama app, or run `ollama serve` in a terminal |
| `Model not found (404)` | `ollama pull llama3.2` (or the name in your `.env`) |
| `Ollama crashed ... (500)`, often mentioning CUDA | Usually an old NVIDIA driver. Update it, or run Ollama on the CPU only (below) |
| Very slow answers | Normal on older laptops. Use the smallest model, or skip to Gemini |

If Ollama crashes with a 500, the best fix is to update your graphics driver
(<https://www.nvidia.com/drivers>), restart, and open the Ollama app again. The model
then runs on the graphics card, which is fast.

If you can't update the driver, run Ollama on the CPU only. Opening the Ollama app
starts it on the graphics card again, so don't use the app for this:

1. Quit the app: right-click the llama icon in the system tray (bottom right, near the
   clock) and choose Quit Ollama.
2. In PowerShell, run this and leave the window open:

   ```powershell
   $env:CUDA_VISIBLE_DEVICES = "-1"; ollama serve
   ```

3. Use a second terminal for the kit's scripts.

The setting lasts only while that window is open. On macOS this problem doesn't come up.

If your laptop can't run a local model at all, that's fine. Skip ahead: Gemini and
OpenRouter cover everything in the next steps.

Next: [06 Tokens and cost](06-tokens-and-cost.md)
