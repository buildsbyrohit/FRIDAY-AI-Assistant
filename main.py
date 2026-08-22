"""
FRIDAY - a small voice-command assistant.

Pipeline:
    listen()        -> records audio and returns raw text from Whisper
    clean_command()  -> normalizes raw text (lowercase, strip punctuation/wake words)
    parse_command()  -> turns cleaned text into a structured action (no side effects)
    execute()        -> performs the action (opens apps/sites, runs commands)
    handle_command()  -> glue: parse then execute

main() ties listening -> cleaning -> handling together in a loop.
"""

import datetime as dt
import string
import subprocess
import webbrowser as wb

import sounddevice as sd
from faster_whisper import WhisperModel

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEBUG = True  # set False to silence the RAW/CLEAN/WORDS debug prints

MODEL_SIZE = "tiny"
SAMPLE_RATE = 16000
DURATION = 7  # seconds recorded per listen() call

WAKE_WORDS = {"hello", "hey", "hi", "friday"}

APPLICATIONS = {
    "calculator": r"C:\Windows\System32\calc.exe",
    "notepad": r"C:\Windows\notepad.exe",
}

COMMANDS = {}  # populated below, once the handler functions exist

# Whisper model is loaded lazily so importing this file (e.g. for tests)
# doesn't force a model download/load.
_model = None


def get_model():
    global _model
    if _model is None:
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model


# ---------------------------------------------------------------------------
# Command handler functions (the actions FRIDAY can take)
# ---------------------------------------------------------------------------

def greet():
    print("hello sir")


def status():
    print("all systems are operational")


def shutdown():
    print("shutting down sir")


def date_time():
    current_time = dt.datetime.now()
    print(f"current time is {current_time.strftime('%I:%M %p')}")


def open_website(domain):
    wb.open(f"https://www.{domain}.com/")
    print(f"opened website: {domain}")


def open_application(application):
    path = APPLICATIONS.get(application)
    if path is not None:
        subprocess.run(path)
        print(f"opened application: {application}")
    else:
        print("no path for this yet")


COMMANDS = {
    "hello": greet,
    "status": status,
    "time": date_time,
    "exit": shutdown,
}


# ---------------------------------------------------------------------------
# LISTEN - microphone in, raw text out
# ---------------------------------------------------------------------------

def listen():
    model = get_model()
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    print("rec start")
    sd.wait()
    audio = recording.squeeze()

    segments, info = model.transcribe(audio, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    texts = []
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        texts.append(segment.text)
    return " ".join(texts)


# ---------------------------------------------------------------------------
# PROCESS - raw text -> cleaned text -> structured action (pure, testable)
# ---------------------------------------------------------------------------

def clean_command(text):
    """Lowercase, strip punctuation, and drop wake words like 'hello'/'friday'."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = [w for w in text.split() if w not in WAKE_WORDS]
    return " ".join(words)


def parse_command(cleaned_query):
    """
    Turn a cleaned command string into a structured action.
    Does not execute anything - just decides what should happen.
    Returns a dict with an "action" key, e.g.:
        {"action": "open_app", "target": "calculator"}
        {"action": "open_site", "target": "google"}
        {"action": "command", "target": "time"}
        {"action": "open_missing_target"}
        {"action": "unknown", "raw": "..."}
        {"action": "empty"}
    """
    split_query = cleaned_query.split()

    if not split_query:
        return {"action": "empty"}

    if "open" in split_query:
        open_index = split_query.index("open")
        if open_index + 1 >= len(split_query):
            return {"action": "open_missing_target"}
        target = split_query[open_index + 1]
        if target in APPLICATIONS:
            return {"action": "open_app", "target": target}
        return {"action": "open_site", "target": target}

    for word in split_query:
        if word in COMMANDS:
            return {"action": "command", "target": word}

    return {"action": "unknown", "raw": cleaned_query}


# ---------------------------------------------------------------------------
# EXECUTE - structured action -> real-world side effects
# ---------------------------------------------------------------------------

def execute(action):
    """Perform the action produced by parse_command(). Returns False to stop FRIDAY."""
    kind = action["action"]

    if kind == "empty":
        print("i didn't catch a command")
        return True

    if kind == "open_missing_target":
        print("open what?")
        return True

    if kind == "open_app":
        open_application(action["target"])
        return True

    if kind == "open_site":
        open_website(action["target"])
        return True

    if kind == "command":
        function = COMMANDS[action["target"]]
        function()
        return function is not shutdown

    if kind == "unknown":
        print(f"i don't know the command: '{action['raw']}'")
        return True

    return True


def handle_command(cleaned_query):
    """Glue: parse the cleaned text, then execute it. Returns False to stop FRIDAY."""
    action = parse_command(cleaned_query)
    return execute(action)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    print("FRIDAY IS ONLINE")
    running = True
    while running:
        raw_query = listen()
        cleaned_query = clean_command(raw_query)

        if DEBUG:
            print("RAW:", repr(raw_query))
            print("CLEAN:", repr(cleaned_query))
            print("WORDS:", cleaned_query.split())

        running = handle_command(cleaned_query)


if __name__ == "__main__":
    main()