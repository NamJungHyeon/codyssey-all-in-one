class Judge:
    """두 점수를 비교해 판정한다. 허용오차(epsilon) 이내 차이는 동점(UNDECIDED)."""

    EPSILON = 1e-9
    EPSILON_DISPLAY = "1e-9"

    @classmethod
    def decide(cls, label_a, score_a, label_b, score_b):
        if abs(score_a - score_b) < cls.EPSILON:
            return "UNDECIDED"
        return label_a if score_a > score_b else label_b
