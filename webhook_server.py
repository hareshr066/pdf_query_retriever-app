from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("Webhook Data Received:", data)

    # TODO: process data here
    # Example: Save to DB, send to Streamlit, etc.

    return {"status": "success", "message": "Webhook received successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
