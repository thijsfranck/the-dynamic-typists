# ruff: noqa
# Pyodide already has a js.pyi but it is not complete for us,
# and is not even able to be used.

# Use https://developer.mozilla.org/en-US/docs/Web/API as reference.

from collections.abc import Callable, Iterable
from typing import Any, Generic, Literal, Sequence, TypeAlias, TypeVar, overload

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
    def closest(self, selectors: str) -> JsDomElement: ...
    @overload
    def getElementsByTagName(self, tagName: Literal["img"]) -> JsArray[JsImgElement]: ...
    @overload
    def getElementsByTagName(self, tagName: str) -> JsArray[JsDomElement]: ...
    def getElementsByTagName(self, tagName: str) -> JsArray[JsDomElement]: ...
    def hasAttribute(self, attrName: str) -> bool: ...
    def removeAttribute(self, attrName: str) -> None: ...
    def getBoundingClientRect(self) -> DOMRect: ...
    # These are on Node, which an Element is.
    # As far as this project is concerned, they are just elements.
    firstChild: JsDomElement | None
    nextSibling: JsDomElement | None
    def removeChild(self, child: JsDomElement) -> None: ...
    def insertBefore(self, newChild: JsDomElement, refChild: JsDomElement) -> None: ...
    def contains(self, otherNode: JsDomElement) -> bool: ...

class JsImgElement(JsDomElement):
    src: str
    width: int
    height: int
    naturalWidth: int
    naturalHeight: int

class JsCanvasElement(JsDomElement):
    width: int
    height: int
    @overload
    def getContext(self, contextId: Literal["2d"]) -> CanvasRenderingContext2D: ...
    @overload
    def getContext(self, contextId: str) -> JsProxy: ...
    def getContext(self, contextId: str) -> JsProxy: ...

class DOMRect(JsProxy):
    top: float
    left: float
    bottom: float
    right: float
    width: float
    height: float

class CanvasRenderingContext2D(JsProxy):
    canvas: JsCanvasElement
    @overload
    def drawImage(self, image: JsImgElement, dx: int, dy: int) -> None: ...
    @overload
    def drawImage(
        self, image: JsImgElement, dx: int, dy: int, dWidth: int, dHeight: int
    ) -> None: ...
    def drawImage(
        self, image: JsImgElement, dx: int, dy: int, dWidth: int = ..., dHeight: int = ...
    ) -> None: ...
    def translate(self, x: int | float, y: int | float) -> None: ...
    def rotate(self, angle: int | float) -> None: ...

class DOMTokenList(JsProxy):
    def add(self, token: str) -> None: ...
    def remove(self, *tokens: str) -> None: ...
    def contains(self, token: str) -> bool: ...

class CSSStyleDeclaration(JsProxy):
    def removeProperty(self, name: str) -> None: ...
    def setProperty(self, name: str, value: str) -> None: ...
    def __setattr__(self, name: str, value: str) -> None: ...

ElementT = TypeVar("ElementT", bound=JsDomElement)

class LoadEvent(JsProxy, Generic[ElementT]):
    target: ElementT

class Event(JsProxy):
    target: JsDomElement
    def preventDefault(self) -> None: ...

class UIEvent(Event): ...

class MouseEvent(Event):
    relatedTarget: JsDomElement
    pageX: float
    pageY: float

class DragEvent(MouseEvent):
    dataTransfer: DataTransfer

class DataTransfer(JsProxy):
    dropEffect: str
    def setData(self, format: str, data: str) -> None: ...
    def setDragImage(self, image: JsDomElement, x: int, y: int) -> None: ...
    def getData(self, format: str) -> str: ...

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
    @staticmethod
    def getElementById(id: str) -> JsDomElement: ...
    @overload
    @staticmethod
    def createElement(tagName: Literal["img"]) -> JsImgElement: ...
    @overload
    @staticmethod
    def createElement(tagName: Literal["canvas"]) -> JsCanvasElement: ...
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
