import uvicorn
import logging
import traceback
import gradio as gr
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from search_pipeline import SearchDescriptionPipeline


logging.basicConfig(level=logging.INFO)
app = FastAPI()
search_module = SearchDescriptionPipeline()

io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
gradio_app = gr.routes.App.create_app(io)

app.mount('/', gradio_app)

@app.get("/ping")
def ping_response():
    return jsonable_encoder({"status": "Server Running"})


@app.get("/")
def gradio_app():
    return {"message": "This is your main app"}


@app.post("/guess_hero")
async def event_ingestion(request: Request):
    try:
        request_body = await request.json()
        challenge = request_body.get("challenge")
        if challenge:
            return jsonable_encoder({"challenge": challenge})

        superhero_names = search_module.run_pipeline(description_text=request_body.get('description'))
        superhero_names = ",".join(superhero_names)
        return jsonable_encoder({"Superhero_Guess": superhero_names})

    except Exception as e:
        logging.error(f"Error in running the pipeline")
        return jsonable_encoder({"Error": traceback.format_exc()})


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9000)