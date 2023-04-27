import anthropic
import openai
from helm.common.authentication import Authentication
from helm.common.request import Request, RequestResult
from helm.proxy.accounts import Account
from helm.proxy.services.remote_service import RemoteService
from functools import partial

# CRFM API: https://github.com/stanford-crfm/helm/blob/main/demo.py
try:
    auth = Authentication(api_key=open("crfm_api_key.txt").read().strip())
    service = RemoteService("https://crfm-models.stanford.edu")
    account: Account = service.get_account(auth)
except:
    print("Warning: CRFM API key not found. Please add your API key to crfm_api_key.txt if you want to use the CRFM API.")
def complete_text_crfm(prompt, stop_sequences = None, model="openai/gpt-4-0314",  max_tokens_to_sample=2000, temperature = 0.2, **kwargs):

    request = Request(
            prompt=prompt, 
            model=model, 
            stop_sequences=stop_sequences,
            temperature = temperature,
            max_tokens = max_tokens_to_sample,
        )
    request_result: RequestResult = service.make_request(auth, request)
    completion = request_result.completions[0].text
    return completion

# anthropic API:
try:
    c = anthropic.Client(open("anthropic_api_key.txt").read().strip())
except:
    print("Warning: Anthropic API key not found. Please add your API key to anthropic_api_key.txt if you want to use the Anthropic API.")
def complete_text_claude(prompt, stop_sequences=[anthropic.HUMAN_PROMPT], model="claude-v1", max_tokens_to_sample =  2000, temperature=0.2,**kwargs):
    resp = c.completion(
        prompt=f"{anthropic.HUMAN_PROMPT} {prompt} {anthropic.AI_PROMPT}",
        a=stop_sequences,
        model=model,
        temperature1=temperature,
        max_tokens_to_sample=max_tokens_to_sample,
        **kwargs
    )   
    completion = resp["completion"]
    return completion

# openai API:
try:
    openai.api_key = open("openai_api_key.txt").read().strip()
except:
    print("Warning: OpenAI API key not found. Please add your API key to openai_api_key.txt if you want to use the OpenAI API.")
def complete_text_openai(prompt, stop_sequences=None, model="text-davinci-003", max_tokens_to_sample = 2000, temperature=0.2, **kwargs):
    completion = openai.Completion.create(
        prompt=prompt,
        stop=stop_sequences,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens_to_sample,
        **kwargs
    )
    return completion["choices"][0]["text"]

complete_text_fast = complete_text_claude
complete_text_slow = complete_text_crfm
