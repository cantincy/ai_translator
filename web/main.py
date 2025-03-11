from fastapi import FastAPI, Form, File, UploadFile
from ai_translator.web.translator import Translator
import uvicorn

file_size_limit = 1024


def main():
    app = FastAPI()

    translator = Translator()

    @app.post("/translate_text")
    def translate_text(original_language=Form(...), target_language=Form(...), original_text=Form(...)):
        return {
            "translated_text": translator.translate(original_language, target_language, original_text)
        }

    @app.post("/translate_file")
    async def translate_file(file: UploadFile = File(...), original_language=Form(...), target_language=Form(...)):
        if file.content_type != "text/plain":
            return {
                "message": "File type not supported"
            }

        if file.size > file_size_limit:
            return {
                "message": "File size exceeds the limit"
            }

        data = await file.read()
        original_text = data.decode("utf-8")

        return {
            "translated_text": translator.translate(original_language, target_language, original_text)
        }

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
