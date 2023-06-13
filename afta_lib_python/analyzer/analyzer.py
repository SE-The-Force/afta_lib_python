import httpx
from afta_lib_python.analyzer.amharic_normalizer import AmharicNormalizer

class Analyzer:
    def __init__(self, analyzer_url):
        self.analyzer_url = analyzer_url

    @staticmethod
    def tokens(text):
        return text.split(' ')

    async def preprocess(self, text):
        text = AmharicNormalizer.remove_punctuation(text)
        text = AmharicNormalizer.remove_non_amharic_chars(text)
        text = AmharicNormalizer.remove_extra_spaces(text)
        text = AmharicNormalizer.remove_stop_words(text)
        return AmharicNormalizer.normalize(text)

    async def analyze(self, text):
        preprocessed_text = await self.preprocess(text)
        tokens = Analyzer.tokens(preprocessed_text)

        try:
            response = await httpx.post(self.analyzer_url, json={"words": tokens})

            if response.status_code == 200:
                return response.json()["rootWords"]
            else:
                return []
        except httpx.HTTPError:
            return []

    async def analyze_all(self, texts):
        preprocessed_texts = [self.preprocess(text) for text in texts]
        all_tokens = [token for text in preprocessed_texts for token in Analyzer.tokens(text)]

        try:
            response = await httpx.post(self.analyzer_url, json={"words": all_tokens})

            if response.status_code == 200:
                root_words = response.json()["rootWords"]
                analyzed_tokens = []
                i = 0
                
                for text_tokens in preprocessed_texts:
                    chunk_size = len(text_tokens)
                    chunk = root_words[i: i + chunk_size]
                    analyzed_tokens.append(chunk)
                    i += chunk_size

                return analyzed_tokens
            else:
                return [[] for _ in texts]
            
        except httpx.HTTPError:
            return [[] for _ in texts]
