from transformers import MT5ForConditionalGeneration, MT5Tokenizer

def load_model(model_card="persiannlp/mt5-base-parsinlu-opus-translation_fa_en"):
    tokenizer = MT5Tokenizer.from_pretrained(model_card)
    model = MT5ForConditionalGeneration.from_pretrained(model_card)
    return model, tokenizer

def translate(input_string, **generator_args):
    model, tokenizer = load_model()
    input_ids = tokenizer.encode(input_string, return_tensors="pt")
    res = model.generate(input_ids, **generator_args)
    output = tokenizer.batch_decode(res, skip_special_tokens=True)
    return output[0]