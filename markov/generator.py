import random

class MarkovGenerator:
    def __init__(self, store, max_words=30):
        self.store = store
        self.max_words = max_words
        self.end_tokens = {".", "!", "?"}

    def generate(self, seed=None):
        # If no seed, pick a random sentence-starting pair
        if seed:
            state1, state2 = seed
        else:
            state1, state2 = self._random_start()
            if not state1:
                return None

        tokens = [state1, state2]

        for _ in range(self.max_words):
            next_word = self._choose_next(state1, state2)
            if not next_word:
                break

            tokens.append(next_word)

            if next_word in self.end_tokens:
                break

            state1, state2 = state2, next_word

        return self._format(tokens)

    # -------------------------
    # Choose a next word weighted by count
    # -------------------------
    def _choose_next(self, state1, state2):
        rows = self.store.get_next_words(state1, state2)
        if not rows:
            return None

        words = [r[0] for r in rows]
        weights = [r[1] for r in rows]

        return random.choices(words, weights=weights, k=1)[0]

    # -------------------------
    # Pick a random starting state beginning with __START__
    # -------------------------
    def _random_start(self):
        row = self.store.conn.execute(
            """
            SELECT state1, state2
            FROM transitions
            WHERE state1 = '__START__'
            ORDER BY RANDOM()
            LIMIT 1
            """
        ).fetchone()

        return row if row else (None, None)

    # -------------------------
    # Convert tokens to human-readable sentence
    # -------------------------
    def _format(self, tokens):
        sentence = ""
        first_word = True

        for token in tokens:
            if token == "__START__":
                continue  # skip start token

            if first_word:
                token = token.capitalize()  # capitalize first real word
                first_word = False

            if token in self.end_tokens:
                sentence = sentence.rstrip() + token + " "
            else:
                sentence += token + " "

        return sentence.strip()