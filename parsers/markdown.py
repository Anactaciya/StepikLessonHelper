from pyparsing import (
    Group, ZeroOrMore, Suppress,
    Dict, Optional, Word, alphanums, restOfLine,
    SkipTo, Literal
)

# потом создать классы Lesson и Step
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from models import Lesson, Step


class MarkdownParser:
    def __init__(self):
        # Парсеры для названий
        lesson_title = Suppress('#') + restOfLine("title")
        step_title = Suppress('##') + restOfLine("step_title")

        content_parser = SkipTo(Literal('##') | Literal('#') | '$END')("text")

        # Парсер для переменных (name = value)
        variable_name = Word(alphanums + "_")
        full_expression = (variable_name + Suppress('=') +
                           restOfLine('variable_name'))

        self.lesson_grammar = Dict(
            Group(lesson_title)("lesson_title") +
            ZeroOrMore(Group(full_expression))("variables") +
            ZeroOrMore(Group(step_title + Optional(content_parser)))("steps")
        )

    def parse_file(self, link: str):
        with open(link, 'r', encoding='utf-8') as file:
            content = file.read() + '\n$END'
        return self.parse(content)

    def parse(self, content: str):
        result = self.lesson_grammar.parseString(content)

        parsed_data = []
        parsed_data.append({'title': result.lesson_title[0].strip()})

        variables_dict = {}
        if hasattr(result, 'variables'):
            for var in result.variables:
                variables_dict[var[0]] = var[1].strip()
        if variables_dict:
            parsed_data.append({'variables': variables_dict})

        if hasattr(result, 'steps'):
            for step in result.steps:
                step_dict = {'step_title': step[0].strip()}
                if len(step) > 1:
                    step_dict['step_content'] = step[1].strip()
                else:
                    step_dict['step_content'] = ''
                parsed_data.append(step_dict)

        return parsed_data


if __name__ == "__main__":
    parser = MarkdownParser()
    res = parser.parse_file("./examples/simple_lesson.md")
    print(res)
