from google import genai
from google.genai import types
# 419152889582 export GOOGLE_APPLICATION_CREDENTIALS="/home/chungtv8/Desktop/eintelligent/eintelligent/src/main/resources/key.json"
# 823956231002 export GOOGLE_APPLICATION_CREDENTIALS="/home/chungtv8/Downloads/vertextai.json"
client = genai.Client(
  vertexai=True, project="823956231002", location="global",
)
# If your image is stored in Google Cloud Storage, you can use the from_uri class method to create a Part object.
IMAGE_URI = "gs://generativeai-downloads/images/scones.jpg"
model = "gemini-2.5-flash"
response = client.models.generate_content(
  model=model,
  contents=[
    "What is shown in this image?",
    types.Part.from_uri(
      file_uri="gs://generativeai-downloads/images/scones.jpg",
      mime_type="image/png",
    ),
  ],
)
print(response.text, end="\n")