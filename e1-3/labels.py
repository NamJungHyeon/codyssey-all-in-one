from grid import Grid


class LabelNormalizer:
    """expected 값과 필터 키를 표준 라벨(Cross/X)로 통일한다."""

    CROSS = "Cross"
    X = "X"

    @classmethod
    def normalize(cls, raw):
        text = str(raw).strip().lower()
        if text in ("+", "cross"):
            return cls.CROSS
        if text == "x":
            return cls.X
        return None

    @classmethod
    def find_filter(cls, filter_set, label):
        """filter_set의 키(cross/x 등, 대소문자 무관)를 정규화해서 표준 라벨과 일치하는 필터를 찾는다."""
        for key, rows in filter_set.items():
            if cls.normalize(key) == label:
                return Grid.from_rows(rows)
        return None
