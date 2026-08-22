import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel


model_size = "tiny"
sample_rate = 16000
duration = 7

model = WhisperModel(
    model_size,
    device="cpu",
    compute_type="int8"
)

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
text = listen()
print("friday heard : ", text)