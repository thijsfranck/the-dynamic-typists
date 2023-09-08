# ruff: noqa
# Pyodide already has a js.pyi but it is not complete for us,
# and is not even able to be used.

from collections.abc import Callable, Iterable
from typing import Any, Literal, Sequence, TypeAlias, overload

from _pyodide._core_docs import _JsProxyMetaClass
from pyodide.ffi import (
    JsArray,
    JsDomElement as OldJSDomElement,
    JsException,
    JsFetchResponse,
    JsProxy,
    JsTypedArray,
)
from pyodide.webloop import PyodideFuture

class JsDomElement(OldJSDomElement):
    classList: DOMTokenList
    style: CSSStyleDeclaration

    @property
    def children(self) -> Sequence[JsDomElement]:
        return []
    def getAttribute(self, name: str) -> str: ...
    def setAttribute(self, name: str, value: str) -> None: ...
    # These are on Node, which an Element is.
    # As far as this project is concerned, they are just elements.
    firstChild: JsDomElement | None
    nextSibling: JsDomElement | None
    def removeChild(self, child: JsDomElement) -> None: ...
    def insertBefore(self, newChild: JsDomElement, refChild: JsDomElement) -> None: ...

class JsImgElement(JsDomElement):
    src: str

class DOMTokenList(JsProxy):
    def add(self, token: str) -> None: ...
    def remove(self, token: str) -> None: ...

class CSSStyleDeclaration(JsProxy):
    def removeProperty(self, name: str) -> None: ...
    def setProperty(self, name: str, value: str) -> None: ...

def eval(code: str) -> Any: ...

# in browser the cancellation token is an int, in node it's a special opaque
# object.
_CancellationToken: TypeAlias = int | JsProxy

def setTimeout(cb: Callable[[], Any], timeout: int | float) -> _CancellationToken: ...
def clearTimeout(id: _CancellationToken) -> None: ...
def setInterval(cb: Callable[[], Any], interval: int | float) -> _CancellationToken: ...
def clearInterval(id: _CancellationToken) -> None: ...
def fetch(
    url: str,
    options: JsProxy | None = None,
) -> PyodideFuture[JsFetchResponse]: ...

self: Any = ...
window: Any = ...

# Shenanigans to convince skeptical type system to behave correctly:
#
# These classes we are declaring are actually JavaScript objects, so the class
# objects themselves need to be instances of JsProxy. So their type needs to
# subclass JsProxy. We do this with a custom metaclass.

class _JsMeta(_JsProxyMetaClass, JsProxy): ...
class _JsObject(metaclass=_JsMeta): ...

class XMLHttpRequest(_JsObject):
    response: str

    @staticmethod
    def new() -> XMLHttpRequest: ...
    def open(self, method: str, url: str, sync: bool) -> None: ...
    def send(self, body: JsProxy | None = None) -> None: ...

class Object(_JsObject):
    @staticmethod
    def fromEntries(it: Iterable[JsArray[Any]]) -> JsProxy: ...

class Array(_JsObject):
    @staticmethod
    def new() -> JsArray[Any]: ...

class ImageData(_JsObject):
    @staticmethod
    def new(width: int, height: int, settings: JsProxy | None = None) -> ImageData: ...

    width: int
    height: int

class _TypedArray(_JsObject):
    @staticmethod
    def new(
        a: int | Iterable[int | float] | JsProxy | None,
        byteOffset: int = 0,
        length: int = 0,
    ) -> JsTypedArray: ...

class Uint8Array(_TypedArray):
    BYTES_PER_ELEMENT = 1

class Float64Array(_TypedArray):
    BYTES_PER_ELEMENT = 8

class JSON(_JsObject):
    @staticmethod
    def stringify(a: JsProxy) -> str: ...
    @staticmethod
    def parse(a: str) -> JsProxy: ...

class document(_JsObject):
    body: JsDomElement
    children: list[JsDomElement]
    @overload
    @staticmethod
    def createElement(tagName: Literal["img"]) -> JsImgElement: ...
    @overload
    @staticmethod
    def createElement(tagName: str) -> JsDomElement: ...
    @staticmethod
    def createElement(tagName: str) -> JsDomElement: ...
    @staticmethod
    def appendChild(child: JsDomElement) -> None: ...

class ArrayBuffer(_JsObject):
    @staticmethod
    def isView(x: Any) -> bool: ...

class DOMException(JsException): ...
