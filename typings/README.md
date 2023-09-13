# Typings

The typings folder offers supplementary type stubs to enhance the clarity and type safety of our codebase. Notably, we expanded upon the default type stubs for the `js` module, provided by Pyodide, to facilitate safer interactions with web APIs and the DOM. Our extensions for the `js` module type stubs are based on [the Mozilla Web API documentation](https://developer.mozilla.org/en-US/docs/Web/API).

## Features

**Clarity and Cohesion**: By providing explicit type information, the typings module aids in maintaining a clean and understandable codebase.

**No Runtime Impact**: Type stubs are only available in the editor and during CI, ensuring type safety without altering the original code structure.

## Usage

To use the extended type stubs, simply import the `js` module directly:

```python
from js import JsDomElement, document, ... # extended type stubs are recognized automatically
```

## Note

Always ensure that, when integrating new features that rely on untyped web APIs, the type stubs in this module are appropriately extended.
