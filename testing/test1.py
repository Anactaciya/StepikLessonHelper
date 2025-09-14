import pprint
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from parsers.markdown import MarkdownParser

# Проверка парса на три составляющие
# (Первое задание)

parser = MarkdownParser()
# res = parser.parse_file("./examples/simple_lesson.md")
res = parser.parse_file("./examples/simple_lesson2.md")
# res = parser.parse_file("./examples/markdown_example.md")
pprint.pprint(res)
