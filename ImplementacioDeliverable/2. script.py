import requests
import csv
import glob
import lxml.etree as ET
import re
import pandas as pd

file_name = 'data'
def write_to_csv(data):
    with open(f'{file_name}.csv', 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(data)

if f'{file_name}.csv' not in glob.glob("*.csv"):
    columns  = [
        'product_name',
        'product_descripion',
        'descripiton',
        'Extra_informatie',
        'Kenmerken',
        'Ingrediënten',
        'Allergie_informatie_Bevat',
        'Allergie_informatie_kan_bevatten',
        'Energie',
        'Vet',
        'waarvan_verzadigd',
        'waarvan_onverzadigd',
        'Koolhydraten',
        'waarvan_suikers',
        'Voedingsvezel',
        'Eiwitten',
        'Zout',
        'url',
        'id'
    ]

    write_to_csv(columns)

with open('urls.txt', 'r') as file:
    ids = file.read().splitlines()

for id in ids:
    url = "https://www.ah.nl/producten/product/" + str(id)

    payload = {}
    cookies = {
    'SSLB': '1',
    'i18next': 'nl-nl',
    '_gcl_au': '1.1.995323013.1742853205',
    '_fbp': 'fb.1.1742853205832.515714387209595176',
    '_pin_unauth': 'dWlkPVlqazNOV0ZtT0dZdE1qTmhNeTAwTkRnd0xUaG1OakF0TURabVptSmpOekV3WlRBeg',
    '_ga': 'GA1.1.607116770.1742853498',
    'FPID': 'FPID2.2.HOQTdKBm%2Bh%2Fi7SEvJAtJ9KJswHubYnXxkQfLMxNAuws%3D.1742853498',
    '_ga_83SGEDKVY7': 'GS1.1.1742853498.1.0.1742853501.0.0.1189860878',
    '_uetvid': '9facdf7008fa11f0985f63d5f7f1b401',
    'SSOC': '48405168c1c06e3476961fdd60f89739458fd189e4ad02fcb57b7e6a150edaba',
    'RCC': 'P1-a63c109c-e1e7-47f1-b442-2b31fdeb2f2b',
    'consentBeta': 'eyJjb25zZW50RGF0ZSI6IjIwMjUwNDEwIiwiY29uc2VudFZlcnNpb24iOiI0LjEiLCJndG1Db250YWluZXJWZXJzaW9uIjoiMTI2MiIsImNvbnNlbnRTdGF0dXMiOiJhY2NlcHRlZCIsImNvbnNlbnRDYXRlZ29yaWVzIjp7Im1hcmtldGluZ0FIIjp0cnVlLCJtYXJrZXRpbmczUCI6dHJ1ZSwiYW5hbHl0aWNzUEEiOnRydWUsIm5lY2Vzc2FyeSI6dHJ1ZX0sImNvbnNlbnRIb3N0IjoiLmFoLm5sIn0=',
    'cookie-consent': '{%22consent%22:%22yes%22%2C%22version%22:%224.1%22%2C%22gtmContainerVersion%22:%221262%22%2C%22date%22:%2220250410%22%2C%22host%22:%22.ah.nl%22%2C%22social%22:%224.1%22%2C%22ad%22:%224.1%22}',
    'bm_ss': 'ab8e18ef4e',
    '_abck': 'A0D00C43F60448EF2DA32982AD1AA207~-1~YAAQDxjdWHX/rxeWAQAAzwxFJQ1Sr47lCP5P54XXhANIVRR24eSXPqfb1LWifbSyBmsDJoaGmkgiR2uKf4jCOZuBLq2dHq+EA8+EQwzeBD77c+AG91//DGUUxkOO+vifChfRjhRgJWz8r9ou7EcDZOCbmscUBOWewbNFXH+hmI5CAmHP4RonR4FBY1wU53JoKjPzXdv98p4/pHsc+7zIg173YW1lx7GMhmSjQYBuA2VoDgmtnO3mi/tegZ2aMq62Eb8WqMerAY1fxqPMPZUiivepAUYXT8Utc65bH7KjNEfypcz/Fem35f6UQ2FAdgP8I8Dexvo5wRFE0j00m95+Jzqb6e+cIqojzJIhNWri0eCVt6CzOcPF2BoY/bkxIagAeO+K+SidZ9XQio851NhWKSO1nasJ405jLLhyim5Lb4OTz27MOceGSDHK4fyEQ7MNJeWNVBijw4SJEvAWiweW6hbPVQXwQieYPSps0+8kXJN2yFAdZrdV4UCqjOioWNrbMVsVczIGHtSvWcu8DII2DD6J/0oGr8S5dZB08XgoEHEvBW87bFJTEZj7lwSilPyeYA5KoFUKQP8vKSHsQB6WWVRP2mhYiKPOxrlYiryLuJLzhCwAv087GQTADAprmQN0/XYQJa/r1wEFZmWggvxxpe/herNtEeO56n2djNID9C1toJBjS4ozpLJjJMzLfnYPksyl9iKEP6Dy~-1~-1~-1',
    'bm_sz': '1A471A9F60146EC72511A5E848D6EA03~YAAQDxjdWHf/rxeWAQAAzwxFJRt6gDS6spFYq/HPcRyNFats60CZ3jpQNEGkmwVaNRIzHC6B0RE56XxRsrS9NPyJidEFbscXSj3fwVKDfzTDzbFoXHIbWuUTM2DiGBd+EAg9dPTeBQSn3UZxxAIn8VzIqPStTdO7OvqL+w68s9MO+kHqGy0Dr+MjaWum8W+8sV/thpAMhF5QePd34vpfTgj0/caLPABCzWy9J7dNGYeKq+BXBv+jIn6ACLUz+5t745SWJxj1FCONy+XwnwfgQiB6MikR4ZbPdasnEixcWqxagMDz9tBmexQ2mBqGdcqSeZF5gFbawYWdEx3CgRVk/ltHIv+/6h5SzuFvFCZ5kynu6GEn+A==~3160134~3355700',
    'SSSC': '4.G7485497495737433114.7|3242.59013:3264.59385:3275.59486:3308.60134:3320.60242:3321.60267:3326.60302:3327.60307:3338.60397:3348.60456:3351.60480:3355.60506:3357.60519:3366.60608',
    'ASC': 'P1-eb5f3f37-b767-44c8-a6df-77017e5e46fb',
    '_csrf': 'wBY3OfR__JJ9DydMQiShuUoR',
    'Ahonlnl-Prd-01-DigitalDev-F1': '!iqneWymL9ozb+I8Eqm88LdtY5yE1NNn29lUdS91r5HCE0FfI7hFcxrpjjbCT/6W+OI+szu33szrNt4Q=',
    'bm_mi': '452E9169B17885FB2295AC2DA45966CB~YAAQYgcQAofL2R2WAQAAA2hXJRuYOJQTqLrWK6NAx+1TFakXe+RKIl/gF03kWRfNYo8JSUcEhMmJs9ZFI75p1MMErjrYI3OBOOK00YoIp1epKwIBBNMu1d2v/lopDBXQ1+iNxWSeVWbu00nqPfZpONCTfZ+I30YPRaHZ3JXS5Vl1R1Cobla21PqmZVUK/TUkXWApYX9cA6AO67WoV9JsxR1JAGC4CEWYsRo8HkKwOeFjq9CPH/UceEfgp6/vqmpTPQEpU2jlv1l53aqf8VYPgSMiRloygYq9B8/J+XZ/o1oaD8L+khxiD9adlXnyH+PLpt/BPVDEj+aa6AiAxvR8jw==~1',
    'SSID': 'CQDsWx3EAAgAAABQ1OFnGnyBAFDU4WcHAAAAAAB8PKRrMSj5ZwBUmv4MAAGO6wAAMSj5ZwEA7AwAAebqAAAxKPlnAQAdDQABZ-wAADEo-WcBABcNAANA7AAAMSj5ZwEA_wwAAZPrAAAxKPlnAQAbDQABWuwAADEo-WcBAMAMAAP55wAAUNThZwcAqgwAA4XmAABQ1OFnBwAKDQAB7esAADEo-WcBAPgMAANS6wAAUNThZwcA-QwAA2vrAABQ1OFnBwAUDQABKOwAADEo-WcBACYNAAHA7AAAMSj5ZwEAywwAAV7oAAAxKPlnAQDwDAAABQ0AAA',
    'ak_bmsc': '9B3FA4FEBC15A18B0EF7BB88072D5D4D~000000000000000000000000000000~YAAQVQcQAhAIJCOWAQAAnKVXJRsf8/c/Dg/ZvDJ9SOC+anBbbOTF3q3QG7PI36seO/W/GqnLaXC5KJiBQJDM+8CX/CiNNflsdbLRd3a2gTCXHRmYiRnJ+mzYOrhEBFoN+lc9LvMXVUCysnBGqFlTb4SKpPvybjhrPcgFVf30SvFMymlAt8Nw9zFKboz4X82FRLq/XzqXe1xl7Ls6rDp3pzm2I4NJICsn4diPBl8QJk5GyqsyiXTI4nOqoPXscVXpsAIG90+3xqN+e3i1ATpURxX79CIf7D3qqvUT1NE3BxWhtgafCRWGV9e9DJjzr3ZU6dGw5ndcS4m4Z9z5gP0eGGbKVDrQALTw2mWbV+5gPg0ulpTe0XAz1dl67MdYRecHXeIHROHc6QwxnbfIkepwRHTVZWV3Iw0oou91YtvmynXt4OfOnoX1jCy9h19rKXxRA96G4DycH6tW7XQwu7wniX99A4o28WJab+mun7GI8/f9TSSIEh79o4yNaPc=',
    'bm_sv': '9CDBF30CD6C0EBC97DB9FF2944A291C1~YAAQVQcQArsJJCOWAQAAbKhXJRsocYw8dV0cjpjmAA8lQ5EXtxow+6UKQY1alzRS3Qx7yrFSntP1DKP5Q85QR8en9sSIgif+TspPKPaOSQYcwhkEZlMnySwQ7hsay4UccihsAFT8X8f8pjkJCA0kIF5gb9VSSa71h0pt3miEzstS2d7mhti/Kj3xJT9efrvw/bCGxj3DGKWdHEStVnr4HffPZJ487vazyOaDrIjqE4l53KNBpGbRDeGvq2yWYGvZ~1',
    'bm_so': '7EDE0C2DF65C1EC8A122EE89D9463AC0A1AFAADEB4C4EEBF803BD2A6597BDB84~YAAQVQcQAqh8JyOWAQAApnNdJQPBwLrVsgTKrueK3QiazUBetz/HY5Twsv4RqWSdt8o7pV7tn0ZeR+iH0L5XIp7Q6LHVU3NwE00oD3ZmvkJjw9NK1mEHz5ttB6bqgrEuiYvyJPebCLIWofxEyk4FLff7LtF57G20ghofeH3nlHMtz9KEIPkHtBupVF68owlHK6eJXb44NxbwXGEtmmbnZA4ceDztrQrdvWIhLR5C7wtu07r0g8GGkwqLSzktIkRoaURbSuhjIItWkDLbpIyLuhVev0RItFQq4+kb/MloAVSttIZsi28xn4Hu3h1MvZwJotqzeSxVf3vNVHZHmfXoMFoYjLmUzBsGaGPp6DKXbcCI8fckrVJ8c2tiJYogaJcIP18oWFSyFWA1IPxbktcy86IEGDOyXluC3vEknX5uZYVETVwFwHaYl4cCUBHiCtx/h05qFrQ/V+KQbw==',
    'bm_s': 'YAAQVQcQAk9+JyOWAQAAK3ZdJQPKf7iSNJM2WFhage4myvA+pl0y0lDQHzl8dqM5VbiXvsGVb/8YIE+jjdIzjcc1Ik/9lS3hTK7sHcQ/hlfp7gfeK8HauPBTuD0s5MlahI8VFRwdmbWlc+1Z2pHg/fM5VjXH9vaMw8y98rWj5WTQLp9PPwH2JPAWFcrv2amKtB/ZpeVRAh3wFajlTduHXGfKWD3Ufun5jZCMzHmlFYw2Hxcw4PKreWfie5fhsl1CMaKqbbUGqAt8X0yf/LfU4RZAGjuWTI2grYI8jU6HFHA5c17pLphlcKaFXp5nG4TWo4krEw2CuiEqUx7Rsx/604wzKSxi/U8hScg/IdyP3UJr2LqKSec6kFC/defjKqPdI1jrx+XOOaReQAB37809bsZ44NCdrTP7OjR/EBB3HDPxok3CjhM6nyarVzA1u3W7pYppySuQY2X0DDPBp5NpLCLPEu4p',
    'bm_lso': '7EDE0C2DF65C1EC8A122EE89D9463AC0A1AFAADEB4C4EEBF803BD2A6597BDB84~YAAQVQcQAqh8JyOWAQAApnNdJQPBwLrVsgTKrueK3QiazUBetz/HY5Twsv4RqWSdt8o7pV7tn0ZeR+iH0L5XIp7Q6LHVU3NwE00oD3ZmvkJjw9NK1mEHz5ttB6bqgrEuiYvyJPebCLIWofxEyk4FLff7LtF57G20ghofeH3nlHMtz9KEIPkHtBupVF68owlHK6eJXb44NxbwXGEtmmbnZA4ceDztrQrdvWIhLR5C7wtu07r0g8GGkwqLSzktIkRoaURbSuhjIItWkDLbpIyLuhVev0RItFQq4+kb/MloAVSttIZsi28xn4Hu3h1MvZwJotqzeSxVf3vNVHZHmfXoMFoYjLmUzBsGaGPp6DKXbcCI8fckrVJ8c2tiJYogaJcIP18oWFSyFWA1IPxbktcy86IEGDOyXluC3vEknX5uZYVETVwFwHaYl4cCUBHiCtx/h05qFrQ/V+KQbw==^1744383604849',
    'SSRT': 'eS75ZwIDAA',
    'SSPV': '-poAAAAAAAAAaAAAAAAAAAAAAAcAAAAAAAAAAAAA',
    'Ahonlnl-Prd-01-DigitalDev-B2': '!TUuwbNhv3isnPsH9WY2Hw9/zqHtxXm+gDA6UEoZj0cAfHzAalra5ag6RUb3na51iRgd0PDFTuFPdAA==',
    'ah_cid_cs': '%7B%22sct%22%3A6%2C%22cid%22%3A%22ah.1.1742853202772.2691968525%22%2C%22cid_t%22%3A1742853202772%2C%22sid%22%3A1744382005525%2C%22sid_t%22%3A1744383613903%2C%22pct%22%3A6%2C%22seg%22%3A1%7D',
}
    

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'es-ES,es;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'SSLB=1; i18next=nl-nl; _gcl_au=1.1.995323013.1742853205; _fbp=fb.1.1742853205832.515714387209595176; _pin_unauth=dWlkPVlqazNOV0ZtT0dZdE1qTmhNeTAwTkRnd0xUaG1OakF0TURabVptSmpOekV3WlRBeg; _ga=GA1.1.607116770.1742853498; FPID=FPID2.2.HOQTdKBm%2Bh%2Fi7SEvJAtJ9KJswHubYnXxkQfLMxNAuws%3D.1742853498; _ga_83SGEDKVY7=GS1.1.1742853498.1.0.1742853501.0.0.1189860878; _uetvid=9facdf7008fa11f0985f63d5f7f1b401; SSOC=48405168c1c06e3476961fdd60f89739458fd189e4ad02fcb57b7e6a150edaba; RCC=P1-a63c109c-e1e7-47f1-b442-2b31fdeb2f2b; consentBeta=eyJjb25zZW50RGF0ZSI6IjIwMjUwNDEwIiwiY29uc2VudFZlcnNpb24iOiI0LjEiLCJndG1Db250YWluZXJWZXJzaW9uIjoiMTI2MiIsImNvbnNlbnRTdGF0dXMiOiJhY2NlcHRlZCIsImNvbnNlbnRDYXRlZ29yaWVzIjp7Im1hcmtldGluZ0FIIjp0cnVlLCJtYXJrZXRpbmczUCI6dHJ1ZSwiYW5hbHl0aWNzUEEiOnRydWUsIm5lY2Vzc2FyeSI6dHJ1ZX0sImNvbnNlbnRIb3N0IjoiLmFoLm5sIn0=; cookie-consent={%22consent%22:%22yes%22%2C%22version%22:%224.1%22%2C%22gtmContainerVersion%22:%221262%22%2C%22date%22:%2220250410%22%2C%22host%22:%22.ah.nl%22%2C%22social%22:%224.1%22%2C%22ad%22:%224.1%22}; bm_ss=ab8e18ef4e; _abck=A0D00C43F60448EF2DA32982AD1AA207~-1~YAAQDxjdWHX/rxeWAQAAzwxFJQ1Sr47lCP5P54XXhANIVRR24eSXPqfb1LWifbSyBmsDJoaGmkgiR2uKf4jCOZuBLq2dHq+EA8+EQwzeBD77c+AG91//DGUUxkOO+vifChfRjhRgJWz8r9ou7EcDZOCbmscUBOWewbNFXH+hmI5CAmHP4RonR4FBY1wU53JoKjPzXdv98p4/pHsc+7zIg173YW1lx7GMhmSjQYBuA2VoDgmtnO3mi/tegZ2aMq62Eb8WqMerAY1fxqPMPZUiivepAUYXT8Utc65bH7KjNEfypcz/Fem35f6UQ2FAdgP8I8Dexvo5wRFE0j00m95+Jzqb6e+cIqojzJIhNWri0eCVt6CzOcPF2BoY/bkxIagAeO+K+SidZ9XQio851NhWKSO1nasJ405jLLhyim5Lb4OTz27MOceGSDHK4fyEQ7MNJeWNVBijw4SJEvAWiweW6hbPVQXwQieYPSps0+8kXJN2yFAdZrdV4UCqjOioWNrbMVsVczIGHtSvWcu8DII2DD6J/0oGr8S5dZB08XgoEHEvBW87bFJTEZj7lwSilPyeYA5KoFUKQP8vKSHsQB6WWVRP2mhYiKPOxrlYiryLuJLzhCwAv087GQTADAprmQN0/XYQJa/r1wEFZmWggvxxpe/herNtEeO56n2djNID9C1toJBjS4ozpLJjJMzLfnYPksyl9iKEP6Dy~-1~-1~-1; bm_sz=1A471A9F60146EC72511A5E848D6EA03~YAAQDxjdWHf/rxeWAQAAzwxFJRt6gDS6spFYq/HPcRyNFats60CZ3jpQNEGkmwVaNRIzHC6B0RE56XxRsrS9NPyJidEFbscXSj3fwVKDfzTDzbFoXHIbWuUTM2DiGBd+EAg9dPTeBQSn3UZxxAIn8VzIqPStTdO7OvqL+w68s9MO+kHqGy0Dr+MjaWum8W+8sV/thpAMhF5QePd34vpfTgj0/caLPABCzWy9J7dNGYeKq+BXBv+jIn6ACLUz+5t745SWJxj1FCONy+XwnwfgQiB6MikR4ZbPdasnEixcWqxagMDz9tBmexQ2mBqGdcqSeZF5gFbawYWdEx3CgRVk/ltHIv+/6h5SzuFvFCZ5kynu6GEn+A==~3160134~3355700; SSSC=4.G7485497495737433114.7|3242.59013:3264.59385:3275.59486:3308.60134:3320.60242:3321.60267:3326.60302:3327.60307:3338.60397:3348.60456:3351.60480:3355.60506:3357.60519:3366.60608; ASC=P1-eb5f3f37-b767-44c8-a6df-77017e5e46fb; _csrf=wBY3OfR__JJ9DydMQiShuUoR; Ahonlnl-Prd-01-DigitalDev-F1=!iqneWymL9ozb+I8Eqm88LdtY5yE1NNn29lUdS91r5HCE0FfI7hFcxrpjjbCT/6W+OI+szu33szrNt4Q=; bm_mi=452E9169B17885FB2295AC2DA45966CB~YAAQYgcQAofL2R2WAQAAA2hXJRuYOJQTqLrWK6NAx+1TFakXe+RKIl/gF03kWRfNYo8JSUcEhMmJs9ZFI75p1MMErjrYI3OBOOK00YoIp1epKwIBBNMu1d2v/lopDBXQ1+iNxWSeVWbu00nqPfZpONCTfZ+I30YPRaHZ3JXS5Vl1R1Cobla21PqmZVUK/TUkXWApYX9cA6AO67WoV9JsxR1JAGC4CEWYsRo8HkKwOeFjq9CPH/UceEfgp6/vqmpTPQEpU2jlv1l53aqf8VYPgSMiRloygYq9B8/J+XZ/o1oaD8L+khxiD9adlXnyH+PLpt/BPVDEj+aa6AiAxvR8jw==~1; SSID=CQDsWx3EAAgAAABQ1OFnGnyBAFDU4WcHAAAAAAB8PKRrMSj5ZwBUmv4MAAGO6wAAMSj5ZwEA7AwAAebqAAAxKPlnAQAdDQABZ-wAADEo-WcBABcNAANA7AAAMSj5ZwEA_wwAAZPrAAAxKPlnAQAbDQABWuwAADEo-WcBAMAMAAP55wAAUNThZwcAqgwAA4XmAABQ1OFnBwAKDQAB7esAADEo-WcBAPgMAANS6wAAUNThZwcA-QwAA2vrAABQ1OFnBwAUDQABKOwAADEo-WcBACYNAAHA7AAAMSj5ZwEAywwAAV7oAAAxKPlnAQDwDAAABQ0AAA; ak_bmsc=9B3FA4FEBC15A18B0EF7BB88072D5D4D~000000000000000000000000000000~YAAQVQcQAhAIJCOWAQAAnKVXJRsf8/c/Dg/ZvDJ9SOC+anBbbOTF3q3QG7PI36seO/W/GqnLaXC5KJiBQJDM+8CX/CiNNflsdbLRd3a2gTCXHRmYiRnJ+mzYOrhEBFoN+lc9LvMXVUCysnBGqFlTb4SKpPvybjhrPcgFVf30SvFMymlAt8Nw9zFKboz4X82FRLq/XzqXe1xl7Ls6rDp3pzm2I4NJICsn4diPBl8QJk5GyqsyiXTI4nOqoPXscVXpsAIG90+3xqN+e3i1ATpURxX79CIf7D3qqvUT1NE3BxWhtgafCRWGV9e9DJjzr3ZU6dGw5ndcS4m4Z9z5gP0eGGbKVDrQALTw2mWbV+5gPg0ulpTe0XAz1dl67MdYRecHXeIHROHc6QwxnbfIkepwRHTVZWV3Iw0oou91YtvmynXt4OfOnoX1jCy9h19rKXxRA96G4DycH6tW7XQwu7wniX99A4o28WJab+mun7GI8/f9TSSIEh79o4yNaPc=; bm_sv=9CDBF30CD6C0EBC97DB9FF2944A291C1~YAAQVQcQArsJJCOWAQAAbKhXJRsocYw8dV0cjpjmAA8lQ5EXtxow+6UKQY1alzRS3Qx7yrFSntP1DKP5Q85QR8en9sSIgif+TspPKPaOSQYcwhkEZlMnySwQ7hsay4UccihsAFT8X8f8pjkJCA0kIF5gb9VSSa71h0pt3miEzstS2d7mhti/Kj3xJT9efrvw/bCGxj3DGKWdHEStVnr4HffPZJ487vazyOaDrIjqE4l53KNBpGbRDeGvq2yWYGvZ~1; bm_so=7EDE0C2DF65C1EC8A122EE89D9463AC0A1AFAADEB4C4EEBF803BD2A6597BDB84~YAAQVQcQAqh8JyOWAQAApnNdJQPBwLrVsgTKrueK3QiazUBetz/HY5Twsv4RqWSdt8o7pV7tn0ZeR+iH0L5XIp7Q6LHVU3NwE00oD3ZmvkJjw9NK1mEHz5ttB6bqgrEuiYvyJPebCLIWofxEyk4FLff7LtF57G20ghofeH3nlHMtz9KEIPkHtBupVF68owlHK6eJXb44NxbwXGEtmmbnZA4ceDztrQrdvWIhLR5C7wtu07r0g8GGkwqLSzktIkRoaURbSuhjIItWkDLbpIyLuhVev0RItFQq4+kb/MloAVSttIZsi28xn4Hu3h1MvZwJotqzeSxVf3vNVHZHmfXoMFoYjLmUzBsGaGPp6DKXbcCI8fckrVJ8c2tiJYogaJcIP18oWFSyFWA1IPxbktcy86IEGDOyXluC3vEknX5uZYVETVwFwHaYl4cCUBHiCtx/h05qFrQ/V+KQbw==; bm_s=YAAQVQcQAk9+JyOWAQAAK3ZdJQPKf7iSNJM2WFhage4myvA+pl0y0lDQHzl8dqM5VbiXvsGVb/8YIE+jjdIzjcc1Ik/9lS3hTK7sHcQ/hlfp7gfeK8HauPBTuD0s5MlahI8VFRwdmbWlc+1Z2pHg/fM5VjXH9vaMw8y98rWj5WTQLp9PPwH2JPAWFcrv2amKtB/ZpeVRAh3wFajlTduHXGfKWD3Ufun5jZCMzHmlFYw2Hxcw4PKreWfie5fhsl1CMaKqbbUGqAt8X0yf/LfU4RZAGjuWTI2grYI8jU6HFHA5c17pLphlcKaFXp5nG4TWo4krEw2CuiEqUx7Rsx/604wzKSxi/U8hScg/IdyP3UJr2LqKSec6kFC/defjKqPdI1jrx+XOOaReQAB37809bsZ44NCdrTP7OjR/EBB3HDPxok3CjhM6nyarVzA1u3W7pYppySuQY2X0DDPBp5NpLCLPEu4p; bm_lso=7EDE0C2DF65C1EC8A122EE89D9463AC0A1AFAADEB4C4EEBF803BD2A6597BDB84~YAAQVQcQAqh8JyOWAQAApnNdJQPBwLrVsgTKrueK3QiazUBetz/HY5Twsv4RqWSdt8o7pV7tn0ZeR+iH0L5XIp7Q6LHVU3NwE00oD3ZmvkJjw9NK1mEHz5ttB6bqgrEuiYvyJPebCLIWofxEyk4FLff7LtF57G20ghofeH3nlHMtz9KEIPkHtBupVF68owlHK6eJXb44NxbwXGEtmmbnZA4ceDztrQrdvWIhLR5C7wtu07r0g8GGkwqLSzktIkRoaURbSuhjIItWkDLbpIyLuhVev0RItFQq4+kb/MloAVSttIZsi28xn4Hu3h1MvZwJotqzeSxVf3vNVHZHmfXoMFoYjLmUzBsGaGPp6DKXbcCI8fckrVJ8c2tiJYogaJcIP18oWFSyFWA1IPxbktcy86IEGDOyXluC3vEknX5uZYVETVwFwHaYl4cCUBHiCtx/h05qFrQ/V+KQbw==^1744383604849; SSRT=eS75ZwIDAA; SSPV=-poAAAAAAAAAaAAAAAAAAAAAAAcAAAAAAAAAAAAA; Ahonlnl-Prd-01-DigitalDev-B2=!TUuwbNhv3isnPsH9WY2Hw9/zqHtxXm+gDA6UEoZj0cAfHzAalra5ag6RUb3na51iRgd0PDFTuFPdAA==; ah_cid_cs=%7B%22sct%22%3A6%2C%22cid%22%3A%22ah.1.1742853202772.2691968525%22%2C%22cid_t%22%3A1742853202772%2C%22sid%22%3A1744382005525%2C%22sid_t%22%3A1744383613903%2C%22pct%22%3A6%2C%22seg%22%3A1%7D',
}
    response = requests.request("GET", url, headers=headers, data=payload)
    dom = ET.HTML(response.text)
    product_name = ''.join(dom.xpath('//h1//text()'))
    product_descripion = '\n'.join(dom.xpath('//div[@data-testhook="pdp-hero-nutriscore"]//text()'))
    descripiton = '\n'.join(dom.xpath("//h2[text()='Omschrijving']//following-sibling::div[1]/ul//text()"))
    Extra_informatie = '\n'.join(dom.xpath("//h4[text()='Extra informatie']//following-sibling::div[1]//text()"))
    Ingrediënten = ' '.join(dom.xpath("//h2[text()='Ingrediënten']//following-sibling::p//text()"))
    Allergie_informatie_Bevat = ' '.join(dom.xpath("//dt[text()='Bevat: ']/following-sibling::dd//text()"))
    Allergie_informatie_kan_bevatten = ' '.join(dom.xpath("//dt[text()='Kan bevatten: ']/following-sibling::dd//text()"))
    Energie = ' '.join(dom.xpath("//td[text()='Energie']//following-sibling::td//text()"))
    Vet = ' '.join(dom.xpath("//td[text()='Vet']//following-sibling::td//text()"))
    waarvan_verzadigd = ' '.join(dom.xpath("//td[text()='waarvan verzadigd']//following-sibling::td//text()"))
    waarvan_onverzadigd = ' '.join(dom.xpath("//td[text()='waarvan onverzadigd']//following-sibling::td//text()"))
    Koolhydraten = ' '.join(dom.xpath("//td[text()='Koolhydraten']//following-sibling::td//text()"))
    waarvan_suikers = ' '.join(dom.xpath("//td[text()='waarvan suikers']//following-sibling::td//text()"))
    Voedingsvezel = ' '.join(dom.xpath("//td[text()='Voedingsvezel']//following-sibling::td//text()"))
    Eiwitten = ' '.join(dom.xpath("//td[text()='Eiwitten']//following-sibling::td//text()"))
    Zout = ' '.join(dom.xpath("//td[text()='Zout']//following-sibling::td//text()"))
    Kenmerken = ', '.join(re.findall(r'typename":"ProductTradeItemResourceIcon","id":"[^"]*","title":"(.*?)"', response.text))
    new_row = [
        product_name,
        product_descripion,
        descripiton,
        Extra_informatie,
        Kenmerken,
        Ingrediënten,
        Allergie_informatie_Bevat,
        Allergie_informatie_kan_bevatten,
        Energie,
        Vet,
        waarvan_verzadigd,
        waarvan_onverzadigd,
        Koolhydraten,
        waarvan_suikers,
        Voedingsvezel,
        Eiwitten,
        Zout,
        url,
        id
    ]

    write_to_csv(new_row)

    print(f'id number {ids.index(id) + 1} is done')

df = pd.read_csv(f'{file_name}.csv')
df.to_excel(f'{file_name}.xlsx', index=False)