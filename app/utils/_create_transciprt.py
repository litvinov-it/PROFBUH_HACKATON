import whisper


def get_text(path):

    model = whisper.load_model("base")

    # verbose=True - отображение процесса в реальном времени
    result = model.transcribe(f"downloads/{path}.mp4", fp16=False, verbose=True)

    # # Сохраняем результат в файл
    # with open("downloads/transcript.txt", "w") as file:
    #     file.write(result["text"])

    transcription = []

    for segment in result["segments"]:
        transcription.append({
            "start": segment["start"],
            "text": segment["text"]
        })

    return transcription

# for segment in result["segments"]:
#     # print(f"{segment=}")
#     print(segment["start"], segment["end"], segment["text"])
