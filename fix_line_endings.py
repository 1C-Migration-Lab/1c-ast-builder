#!/usr/bin/env python
"""
Скрипт для исправления окончаний строк в файле setup.py
"""


def fix_line_endings(filename):
    """Исправляет окончания строк в файле, заменяя CRLF на LF"""
    with open(filename, "rb") as f:
        content = f.read()

    # Заменяем CRLF на LF
    content = content.replace(b"\r\n", b"\n")

    with open(filename, "wb") as f:
        f.write(content)

    print(f"Окончания строк в файле {filename} исправлены")


if __name__ == "__main__":
    fix_line_endings("setup.py")
