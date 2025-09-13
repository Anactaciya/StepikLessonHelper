from dataclasses import dataclass
from typing import List


# Оба класса пока как прототип и нигде не используются
@dataclass
class Step:
    title: str
    content: str
    step_type: str = "text"

@dataclass
class Lesson:
    lesson_id: int
    title: str
    abstract: str
    steps: List[Step]
    # Можно добавить другие переменные урока позже
    # course_id: Optional[int] = None
    # is_draft: bool = True