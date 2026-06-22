import json
import xml.etree.ElementTree as element_tree
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class Printer(ABC):
    @abstractmethod
    def print(self, book: Book) -> None:
        pass


class ConsolePrinter(Printer):
    def print(self, book: Book) -> None:
        print(f"Printing the book: {book.title}...")
        print(book.content)


class ReversePrinter(Printer):
    def print(self, book: Book) -> None:
        print(f"Printing the book in reverse: {book.title}...")
        print(book.content[::-1])


class Serializer(ABC):
    @abstractmethod
    def serialize(self, book: Book) -> str:
        pass


class JsonSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        return json.dumps({"title": book.title, "content": book.content})


class XmlSerializer(Serializer):
    def serialize(self, book: Book) -> str:
        root = element_tree.Element("book")
        element_tree.SubElement(root, "title").text = book.title
        element_tree.SubElement(root, "content").text = book.content
        return element_tree.tostring(root, encoding="unicode")


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    printers = {
        "console": ConsolePrinter(),
        "reverse": ReversePrinter()
    }
    serializers = {
        "json": JsonSerializer(),
        "xml": XmlSerializer()
    }

    for cmd, method_type in commands:
        if cmd == "display" or cmd == "print":
            printers[method_type].print(book)
        elif cmd == "serialize":
            return serializers[method_type].serialize(book)


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
