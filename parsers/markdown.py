from pprint import pprint
from pyparsing import (
    Group, ZeroOrMore, Suppress, AtLineStart,
    Dict, Optional, Word, alphanums, restOfLine,
    SkipTo, Literal, Combine, LineStart, OneOrMore, pyparsing_common,
    QuotedString, alphas, oneOf, MatchFirst
)
import sys
from pathlib import Path


project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


# потом создать классы Lesson и Step
from models import Lesson, Step


class MarkdownParser:
    def __init__(self):
        # Парсеры для названий
        lesson_title = AtLineStart(Suppress('#')) + restOfLine("title")
        step_title = AtLineStart(
            Suppress(Literal('## '))) + restOfLine("step_title")
        
        content_parser = MatchFirst([
            QuotedString('"""', multiline=True),
            QuotedString("'''", multiline=True),
            SkipTo(AtLineStart(Literal('## ')) | '$END')
            ])("text")

        # Парсер для переменных (name = value)
        variable_name = Word(alphanums + "_")
        full_expression = (AtLineStart(variable_name) + Suppress('=') +
                           restOfLine('variable_name'))

        self.lesson_grammar = Dict(
            Group(lesson_title)("lesson_title") +
            ZeroOrMore(Group(full_expression))("variables") +
            ZeroOrMore(Group(step_title + Optional(content_parser)))("steps")
        )
        self.allowed_step_types = ['TEXT', 'NUMBER', 'SKIP']

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
                step_res = self.parse_step(
                    step['step_title'], step['text'])
                if step_res:
                    parsed_data.append(self.parse_step(
                        step['step_title'], step['text']))

        return parsed_data

    def parse_step(self, header: str, content: str):
        header_pars = (Optional(oneOf(self.allowed_step_types), default="TEXT") + restOfLine).parseString(header)

        res = {
            "step_title": header_pars[1].strip(),
            "step_type": header_pars[0]
        }
        step_type = header_pars[0]

        if step_type == "NUMBER":
            answer_prefix = Suppress("ANSWER" + Optional('=') + Optional(':'))
            number = Combine(pyparsing_common.number +
                             Optional(Suppress(Optional(" ")) + "+-" +
                                      Suppress(Optional(" ")) + pyparsing_common.number))
            answer = answer_prefix + number

            grammar = Dict(
                Group(
                    SkipTo(answer) +
                    OneOrMore(answer))
            )

            parse_res = grammar.parse_string(content)

            res["step_description"] = parse_res[0][0]
            res["step_answers"] = parse_res[0][1::]
        elif step_type == "SKIP":
            return None
        else:
            res["step_description"] = content

        return res


if __name__ == "__main__":
    parser = MarkdownParser()
    res = parser.parse_file("./examples/simple_lesson3.md")
    pprint(res)
