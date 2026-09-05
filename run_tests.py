from chatbot.nlp_utils import preprocess_text, detect_intent
from chatbot.response_generator import generate_response

examples = [
    "Show 5th semester subjects",
    "List Assistant Professors",
    "Faculty specialized in Image Processing",
    "supporting staff details",
    "Show lab details",
    "faculty details"
]

for e in examples:
    tokens = preprocess_text(e)
    intent = detect_intent(e)
    reply = generate_response(intent, tokens)
    print('INPUT:', e)
    print('INTENT:', intent)
    print('REPLY:\n', reply)
    print('\n'+'-'*60+'\n')
