# encoding: utf-8
"""Use the HTMLParser library to parse HTML files that aren't too bad."""
from __future__ import annotations

__license__ = "MIT"

__all__ = [
    "HTMLParserTreeBuilder",
]

from html.parser import HTMLParser
from typing import (
    Any, Callable, cast, Dict, Iterable, List, Optional, TYPE_CHECKING,
    Tuple, Type, Union,
)

from bs4.element import (
    AttributeDict, CData, Comment, Declaration, Doctype, ProcessingInstruction,
)
from bs4.dammit import EntitySubstitution, UnicodeDammit
from bs4.builder import (
    DetectsXMLParsedAsHTML, HTML, HTMLTreeBuilder, STRICT,
)
from bs4.exceptions import ParserRejectedMarkup

if TYPE_CHECKING:
    from bs4 import BeautifulSoup
    from bs4.element import NavigableString
    from bs4._typing import (
        _Encoding, _Encodings, _RawMarkup,
    )

HTMLPARSER = "html.parser"
_DuplicateAttributeHandler = Callable[[Dict[str, str], str, str], None]


class BeautifulSoupHTMLParser(HTMLParser, DetectsXMLParsedAsHTML):
    REPLACE = "replace"
    IGNORE = "ignore"

    def __init__(
        self,
        soup: BeautifulSoup,
        *args: Any,
        on_duplicate_attribute: Union[str, _DuplicateAttributeHandler] = REPLACE,
        **kwargs: Any,
    ):
        self.soup = soup
        self.on_duplicate_attribute = on_duplicate_attribute
        self.attribute_dict_class = soup.builder.attribute_dict_class
        HTMLParser.__init__(self, *args, **kwargs)
        self.already_closed_empty_element = []
        self._initialize_xml_detector()

    def error(self, message: str) -> None:
        raise ParserRejectedMarkup(message)

    def handle_startendtag(
        self, name: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        self.handle_starttag(name, attrs, handle_empty_element=False)
        self.handle_endtag(name)

    def handle_starttag(
        self,
        name: str,
        attrs: List[Tuple[str, Optional[str]]],
        handle_empty_element: bool = True,
    ) -> None:
        """Handle an opening tag like <tag>"""

        if self.soup.builder.replacer:
            name = self.soup.builder.replacer.replace(name)

        attr_dict: AttributeDict = self.attribute_dict_class()
        for key, value in attrs:
            if value is None:
                value = ""
            if key in attr_dict:
                on_dupe = self.on_duplicate_attribute
                if on_dupe == self.IGNORE:
                    pass
                elif on_dupe in (None, self.REPLACE):
                    attr_dict[key] = value
                else:
                    on_dupe = cast(_DuplicateAttributeHandler, on_dupe)
                    on_dupe(attr_dict, key, value)
            else:
                attr_dict[key] = value

        sourceline: Optional[int]
        sourcepos: Optional[int]
        if self.soup.builder.store_line_numbers:
            sourceline, sourcepos = self.getpos()
        else:
            sourceline = sourcepos = None

        tag = self.soup.handle_starttag(
            name, None, None, attr_dict, sourceline=sourceline, sourcepos=sourcepos
        )

        if tag and tag.is_empty_element and handle_empty_element:
            self.handle_endtag(name, check_already_closed=False)
            self.already_closed_empty_element.append(name)

        if self._root_tag_name is None:
            self._root_tag_encountered(name)

    def handle_endtag(self, name: str, check_already_closed: bool = True) -> None:
        if check_already_closed and name in self.already_closed_empty_element:
            self.already_closed_empty_element.remove(name)
        else:
            self.soup.handle_endtag(name)

    def handle_data(self, data: str) -> None:
        self.soup.handle_data(data)

    def handle_charref(self, name: str) -> None:
        if name.startswith("x") or name.startswith("X"):
            real_name = int(name.lstrip("xX"), 16)
        else:
            real_name = int(name)

        data = None
        if real_name < 256:
            for encoding in (self.soup.original_encoding, "windows-1252"):
                if not encoding:
                    continue
                try:
                    data = bytearray([real_name]).decode(encoding)
                except UnicodeDecodeError:
                    pass

        if not data:
            try:
                data = chr(real_name)
            except (ValueError, OverflowError):
                data = "\uFFFD"
        self.handle_data(data)

    def handle_entityref(self, name: str) -> None:
        character = EntitySubstitution.HTML_ENTITY_TO_CHARACTER.get(name)
        data = character if character is not None else f"&{name}"
        self.handle_data(data)

    def handle_comment(self, data: str) -> None:
        self.soup.endData()
        self.soup.handle_data(data)
        self.soup.endData(Comment)

    def handle_decl(self, data: str) -> None:
        self.soup.endData()
        data = data[len("DOCTYPE ") :] if data.startswith("DOCTYPE ") else data
        self.soup.handle_data(data)
        self.soup.endData(Doctype)

    def unknown_decl(self, data: str) -> None:
        cls: Type[NavigableString]
        if data.upper().startswith("CDATA["):
            cls = CData
            data = data[len("CDATA[") :]
        else:
            cls = Declaration
        self.soup.endData()
        self.soup.handle_data(data)
        self.soup.endData(cls)

    def handle_pi(self, data: str) -> None:
        self.soup.endData()
        self.soup.handle_data(data)
        self._document_might_be_xml(data)
        self.soup.endData(ProcessingInstruction)


class HTMLParserTreeBuilder(HTMLTreeBuilder):
    is_xml: bool = False
    picklable: bool = True
    NAME: str = HTMLPARSER
    features: Iterable[str] = [NAME, HTML, STRICT]
    parser_args: Tuple[Iterable[Any], Dict[str, Any]]
    TRACKS_LINE_NUMBERS: bool = True

    def __init__(
        self,
        parser_args: Optional[Iterable[Any]] = None,
        parser_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        self.replacer = kwargs.pop("replacer", None)

        extra_parser_kwargs = dict()
        for arg in ("on_duplicate_attribute",):
            if arg in kwargs:
                value = kwargs.pop(arg)
                extra_parser_kwargs[arg] = value

        super(HTMLParserTreeBuilder, self).__init__(**kwargs)
        parser_args = parser_args or []
        parser_kwargs = parser_kwargs or {}
        parser_kwargs.update(extra_parser_kwargs)
        parser_kwargs["convert_charrefs"] = False
        self.parser_args = (parser_args, parser_kwargs)

    def prepare_markup(
        self,
        markup: _RawMarkup,
        user_specified_encoding: Optional[_Encoding] = None,
        document_declared_encoding: Optional[_Encoding] = None,
        exclude_encodings: Optional[_Encodings] = None,
    ) -> Iterable[Tuple[str, Optional[_Encoding], Optional[_Encoding], bool]]:
        if isinstance(markup, str):
            yield (markup, None, None, False)
            return

        known_definite_encodings: List[_Encoding] = []
        if user_specified_encoding:
            known_definite_encodings.append(user_specified_encoding)

        user_encodings: List[_Encoding] = []
        if document_declared_encoding:
            user_encodings.append(document_declared_encoding)

        dammit = UnicodeDammit(
            markup,
            known_definite_encodings=known_definite_encodings,
            user_encodings=user_encodings,
            is_html=True,
            exclude_encodings=exclude_encodings,
        )

        if dammit.unicode_markup is None:
            raise ParserRejectedMarkup(
                "Could not convert input to Unicode, and html.parser will not accept bytestrings."
            )
        else:
            yield (
                dammit.unicode_markup,
                dammit.original_encoding,
                dammit.declared_html_encoding,
                dammit.contains_replacement_characters,
            )

    def feed(self, markup: _RawMarkup) -> None:
        args, kwargs = self.parser_args
        assert isinstance(markup, str)
        assert self.soup is not None
        parser = BeautifulSoupHTMLParser(self.soup, *args, **kwargs)
        try:
            parser.feed(markup)
            parser.close()
        except AssertionError as e:
            raise ParserRejectedMarkup(e)
        parser.already_closed_empty_element = []