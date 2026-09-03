import json

from grid import Grid
from judge import Judge
from labels import LabelNormalizer
from mac_unit import MacUnit


class PatternAnalyzer:
    """data.json을 읽고, 각 패턴을 필터와 비교해 판정 결과를 만든다."""

    def __init__(self, data_file):
        self.data_file = data_file

    def load(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ {self.data_file} 파일을 찾을 수 없습니다.")
            return None
        except json.JSONDecodeError as error:
            print(f"⚠️ data.json 파일이 손상되었습니다: {error}")
            return None

    @staticmethod
    def get_pattern_size(case_id):
        """'size_5_1' 같은 케이스 키에서 크기(N)를 추출한다. 형식이 다르면 None."""
        parts = case_id.split("_")
        if len(parts) >= 2 and parts[0] == "size" and parts[1].isdigit():
            return int(parts[1])
        return None

    @staticmethod
    def sort_key(case_id):
        """케이스 키를 숫자 기준으로 정렬하기 위한 키 (size_5_1 < size_5_2 < size_13_1 ...)."""
        numbers = [int(part) for part in case_id.split("_") if part.isdigit()]
        return numbers if numbers else [case_id]

    @staticmethod
    def has_filter_pair(filter_set):
        has_cross = filter_set is not None and LabelNormalizer.find_filter(filter_set, LabelNormalizer.CROSS) is not None
        has_x = filter_set is not None and LabelNormalizer.find_filter(filter_set, LabelNormalizer.X) is not None
        return has_cross and has_x

    def analyze(self, case_id, case, filters):
        """패턴 하나를 분석해 결과를 딕셔너리로 반환한다. 실패해도 예외를 던지지 않고 reason에 사유를 남긴다."""
        result = {
            "cross_score": None,
            "x_score": None,
            "verdict": None,
            "expected": None,
            "passed": False,
            "reason": None,
        }

        n = self.get_pattern_size(case_id)
        if n is None:
            result["reason"] = "케이스 이름에서 크기(N)를 추출할 수 없음"
            return result

        filter_key = f"size_{n}"
        filter_set = filters.get(filter_key)
        if filter_set is None:
            result["reason"] = f"{filter_key} 필터를 찾을 수 없음"
            return result

        pattern_input = case.get("input")
        if pattern_input is None or len(pattern_input) != n or any(len(row) != n for row in pattern_input):
            result["reason"] = f"패턴 크기가 {filter_key}(과)와 일치하지 않음"
            return result

        cross_filter = LabelNormalizer.find_filter(filter_set, LabelNormalizer.CROSS)
        x_filter = LabelNormalizer.find_filter(filter_set, LabelNormalizer.X)
        if cross_filter is None or x_filter is None:
            result["reason"] = f"{filter_key}에 Cross/X 필터가 모두 존재하지 않음"
            return result

        pattern = Grid.from_rows(pattern_input)
        result["cross_score"] = MacUnit.compute(pattern, cross_filter)
        result["x_score"] = MacUnit.compute(pattern, x_filter)
        result["verdict"] = Judge.decide("Cross", result["cross_score"], "X", result["x_score"])

        expected = LabelNormalizer.normalize(case.get("expected"))
        if expected is None:
            result["reason"] = f"expected 값 '{case.get('expected')}'을(를) 정규화할 수 없음"
            return result

        result["expected"] = expected
        result["passed"] = result["verdict"] == expected
        if not result["passed"]:
            if result["verdict"] == "UNDECIDED":
                result["reason"] = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            else:
                result["reason"] = f"판정({result['verdict']})이 expected({expected})와 다름"

        return result
