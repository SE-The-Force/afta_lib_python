class AnalyzerMock:
    def __init__(self):
        pass
    
    def tokens(self, text):
        return text.split(' ')
    
    async def analyze(self, text):
        tokens = self.tokens(text)
        # analyze
        return tokens
