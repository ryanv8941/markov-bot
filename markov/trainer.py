import re

class MarkovTrainer:
    def __init__(self, store, order=2):
        if order != 2:
            raise ValueError("Only order-2 Markov is supported")

        self.store = store

    def train(self, text):
        tokens = self._tokenize(text)
        tokens = ['__START__'] + tokens

        if len(tokens) < 3:
            return

        for i in range(len(tokens) - 2):
            self.store.record_transition(
                tokens[i],
                tokens[i + 1],
                tokens[i + 2]
            )

    def _tokenize(self, text):

        text = re.sub(r"https?://\S+", "", text)
        # text = re.sub(r"<@!?\d+>", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Regex to split into sentences including punctuation
        sentence_endings = re.compile(r'([.!?])')
        pieces = sentence_endings.split(text)

        # Recombine into sentence chunks with punctuation
        sentences = []
        for i in range(0, len(pieces) - 1, 2):
            sentence = pieces[i].strip()
            punct = pieces[i + 1]
            sentences.append(sentence + punct)
        # Handle any leftover text without punctuation
        if len(pieces) % 2 != 0:
            leftover = pieces[-1].strip()
            if leftover:
                sentences.append(leftover)

        # Tokenize each sentence and prepend __START__
        tokens = []
        for sentence in sentences:
            sentence_tokens = re.findall(r"\b\w+(?:['-]\w+)?\b|[.!?]|[\U0001F300-\U0001FAFF\U00002600-\U000027BF]", sentence)
            tokens.append('__START__')
            tokens.extend(sentence_tokens)

        return tokens