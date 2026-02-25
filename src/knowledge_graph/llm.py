import requests
import json
import re

def extract_json_from_text(text):
    # This is the missing tool that cleans up the AI response
    try:
        # 1. Try to read it directly
        return json.loads(text)
    except:
        pass

    # 2. Look for json inside code blocks
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except:
            pass
            
    # 3. Look for the first { and last }
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except:
        return {}

def call_llm(model, user_prompt, api_key, system_prompt, max_tokens, temperature, base_url):
    # 1. CLEAN THE URL
    clean_base = base_url.rstrip("/")
    if "chat/completions" not in clean_base:
        url = f"{clean_base}/chat/completions"
    else:
        url = clean_base

    # 2. PREPARE HEADERS
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 3. PREPARE PAYLOAD
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    print(f"\n📡 CONNECTING TO: {url}")
    print(f"🤖 MODEL: {model}")

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            print(f"\n❌ CRITICAL ERROR {response.status_code}")
            print(f"RESPONSE: {response.text}")
            raise Exception(f"Google Refused Connection: {response.status_code}")

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"\n💥 NETWORK CRASH: {e}")
        raise e
