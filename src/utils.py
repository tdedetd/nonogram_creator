def endswith(s: str, endings: list[str]) -> bool:
    for end in endings:
        if s.endswith(end):
            return True

    return False


def remove_dublicates(l: list) -> list:
    return list(set(l))
