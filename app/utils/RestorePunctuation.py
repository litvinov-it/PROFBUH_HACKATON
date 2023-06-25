# pipenv install punctuators

from typing import List
from punctuators.models import PunctCapSegModelONNX

m: PunctCapSegModelONNX = PunctCapSegModelONNX.from_pretrained(
    "1-800-BAD-CODE/xlm-roberta_punctuation_fullstop_truecase"
)

def restore_punctuation(raw_text):

    input_texts: List[str] = [raw_text]

    results: List[List[str]] = m.infer(
        texts=input_texts, apply_sbd=True
    )

    return results
