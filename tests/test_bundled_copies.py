"""The kit carries copies of a few course files so it works on its own.

For maintainers who keep this repo next to the course repo
(projects/prep-kit and projects/resolvo-workshop), these tests check the copies
still match the originals. Anywhere else, they skip.
"""
import pytest

from providers import KIT_DIR


def _find_course_repo():
    for candidate in (KIT_DIR.parent / "resolvo-workshop", KIT_DIR.parent):
        if (candidate / "checkpoints").is_dir() and (candidate / "shared").is_dir():
            return candidate
    return None


REPO = _find_course_repo()

COPIES = {
    "data/tickets.json": "shared/data/tickets.json",
    "mock_api/app.py": "shared/mock_order_api/app.py",
    "mock_api/orders_seed.json": "shared/mock_order_api/orders_seed.json",
    "slides/session-00.html": "slides/session-00.html",
    "slides/deck.css": "slides/deck.css",
    "slides/deck.js": "slides/deck.js",
    "slides/session-00.pptx": "slides/pptx/session-00.pptx",
}


@pytest.mark.skipif(REPO is None, reason="course repo not next to the kit; nothing to compare")
@pytest.mark.parametrize("copy, original", COPIES.items())
def test_copy_matches_the_course_repo(copy, original):
    assert (KIT_DIR / copy).read_bytes() == (REPO / original).read_bytes(), (
        f"prep-kit/{copy} is out of date. From the folder holding both repos: "
        f"copy resolvo-workshop\\{original.replace('/', chr(92))} prep-kit\\{copy.replace('/', chr(92))}")


def test_kit_has_everything_it_needs():
    for copy in COPIES:
        assert (KIT_DIR / copy).is_file(), f"missing prep-kit/{copy}"
