import requests
import json
from sanic import Sanic
from sanic.response import json as js

# Create a Sanic app instance
app = Sanic("prompting")

@app.route("/prompting", methods=["POST"])
async def prompting(request):
    """
    A function that sends the prompts to an LLM

    Parameters:
    - JSON object from request body:
      {
          "model_endpoint": string,
          "token": string,
          "prompts": [string],
          "tags": {
              "prefix": string,
              "suffix": string
          }
          # tags are optional
      }

    Return:
    - JSON response from model
    - OR returns an error in case the URL is wrong
    """

    try:
        # importing data from request as JSON and storing in the appropriate variables
        data = request.json
        url = data.get("model_endpoint")
        token = data.get("token")
        prompts = data.get("prompts", [])

        prompt_output = []

        for prompt in prompts:
            # Construct the prompt with optional prefix and suffix

            payload = json.dumps({
                "inputs": prompt
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            # Send the request to the external model endpoint
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code in [200, 201]:
                # Extract the generated text from the response
                generated_text = response.json().get("generated_text", "")
            else:
                # Return the error message if the request fails
                return js({"error": response.text}, status=response.status_code)
            # prompt_output.append("output of "+prompt)

        return js({"results": prompt_output}, status=200)

    except Exception as e:
        # Handle errors and return a JSON error response
        return js({"error": str(e)}, status=400)

# Run the Sanic server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
