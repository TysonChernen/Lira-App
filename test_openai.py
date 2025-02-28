import openai

# Set your OpenAI API Key manually for testing

try:
    response = openai.models.list()  # ✅ Correct method for OpenAI >= 1.0
    print("✅ OpenAI API Key is VALID!")
except openai.AuthenticationError as e:  # ✅ Fix error handling
    print("❌ OpenAI Authentication Error:", e)
except openai.OpenAIError as e:  # ✅ General OpenAI API errors
    print("❌ OpenAI API Error:", e)
except Exception as e:
    print("❌ Another Error:", e)
