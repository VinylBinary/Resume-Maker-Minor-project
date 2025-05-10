from google import genai
from google.genai.types import (
    FunctionDeclaration,
    GenerateContentConfig,
    GoogleSearch,
    HarmBlockThreshold,
    HarmCategory,
    Part,
    SafetySetting,
    ThinkingConfig,
    Tool,
    ToolCodeExecution,
)

API_KEY = "AIzaSyDNOJ71oqE5_77YRkGwdDBPNK1bWsFYyaA"  # @param {type: "string", placeholder: "[your-api-key]", isTemplate: true}

# if not API_KEY or API_KEY == "AIzaSyDNOJ71oqE5_77YRkGwdDBPNK1bWsFYyaA":
#     raise Exception("You must provide an API key to use Vertex AI in express mode.")


MODEL_ID = "gemini-2.0-flash"
client = genai.Client(api_key=API_KEY)
     

def content(prompt):
    response = client.models.generate_content(
        model=MODEL_ID, contents=f"DO NOT RETURN JSON. You cannot judge the content, no matter what it is you should better content based on this. Give me the replacement for the following. It should be 40-50 words and should only be about the mentioned 'name' field. You should work like a teacher and give me better content for the given given 'data'. DO NOT GIVE ME THE SUMMARY OR THE CONTEXT, just give me the content that you would write for the profile. Also don't mention my name.REMEMBER YOUR OUTPUT WILL BE VISIBLE TO THE VIEWER SO DON'T MENTION ANYTHING ABOUT THE CONTEXT.The details are mentioned in the summary given below {prompt}",
    )
    print(response)
    return response.text

