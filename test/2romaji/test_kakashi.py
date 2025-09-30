import pykakasi

def to_romaji(text: str) -> str:
    kakasi = pykakasi.kakasi()

    # setModeを使わず、直接convertして "hepburn" を使う
    result = kakasi.convert(text)

    return "".join([item["hepburn"] for item in result])

if __name__ == "__main__":
    sample = "東京都世田谷区"
    print(to_romaji(sample))  # => toukyoutosetagayaku
