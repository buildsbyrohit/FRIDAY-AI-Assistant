import datetime as dt
import webbrowser as wb
import subprocess
import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

print("FRIDAY IS ONLINE")

model_size = "tiny"
sample_rate = 16000
duration = 7

model = WhisperModel(
    model_size,
    device="cpu",
    compute_type="int8"
)

def greet():
    print("hello sir")
def status():
    print("all systems are operational")
def shutdown():
    print("shutting down sir")
def open_website(domain):
    wb.open(f"https://www.{domain}.com/")
    print("browser opened")
def date_time():
    current_time = dt.datetime.now()
    format_time = current_time.strftime("%I:%M %p")
    print(f"current time is {format_time}")

def open_application(application):
    process = applications.get(application)
    if process is not None:

        subprocess.run(process)
    else:
        print("no path for this yet")

def clean_command(text):
    lowers = text.lower()
    remover = lowers.replace("hello, friday,", " ")
    remover2 = remover.replace(".", "")
    striper = remover2.strip()
    return striper

def listen():
    my_recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1)
    print("rec start")
    sd.wait()
    rec_squeeze = my_recording.squeeze()
    segments, info = model.transcribe(rec_squeeze, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    texts = []
    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        texts.append(segment.text)
    joined = " ".join(texts)
    return joined


commands = {
    "hello": greet,
    "status":status, 
    "time": date_time, 
    "exit": shutdown,
    }

applications = {
    "calculator": r"C:\Windows\System32\calc.exe",
    "notepad": r"C:\Windows\notepad.exe"
}

while True:

    query = listen()
    print("friday heard : ", query)
    cleaned_query = clean_command(query)
    split_query = cleaned_query.split()
         
    
    if "open" in split_query:
        open_index = split_query.index("open")
        if open_index + 1 < len(split_query):
            target = split_query[open_index + 1]
            if target in applications:
                open_application(target)
            else:
                open_website(target)
            continue

    functions = None
    for word in split_query:
        if word in commands:
            functions = commands[word]
            break

    if functions is not None:
        functions()
        if functions == shutdown:
            break
    else:
        print("i dont know this cmd yet")