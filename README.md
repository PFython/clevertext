# `CleverText`

## Work in progress... copied from CleverDict

<br>
<p align="center">
    <a href="https://pypi.python.org/pypi/clevertext"><img alt="PyPI" src="https://img.shields.io/pypi/v/clevertext.svg"></a>
	<a href="https://pypi.python.org/pypi/clevertext"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/clevertext.svg"></a>
    <a href="https://pepy.tech/project/clevertext"><img alt="Downloads" src="https://pepy.tech/badge/clevertext"></a>
    <a href="#Contribution" title="Contributions are welcome"><img src="https://img.shields.io/badge/contributions-welcome-green.svg"></a>
    <a href="https://github.com/pfython/clevertext/releases" title="clevertext"><img src="https://img.shields.io/github/release-date/pfython/clevertext?color=green&label=updated"></a>
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/clevertext">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/clevertext">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/pfython/clevertext">
    <a href="https://twitter.com/@appawsom" title="Follow us on Twitter"><img src="https://img.shields.io/twitter/follow/appawsom.svg?style=social&label=Follow"></a>
</p>

![clevertext cartoon](https://raw.githubusercontent.com/PFython/clevertext/master/clevertext%20cartoon.png)

## >CONTENTS

1. [OVERVIEW](#1.-OVERVIEW)
2. [INSTALLATION](#2.-INSTALLATION)
3. [INPUT METHODS](#3.-IMPORTING-TO-CleverText)
4. [OUTPUT METHODS](#4.-EXPORTING-FROM-CLEVERICT)
5. [ATTRIBUTE NAMES AND ALIASES](#5.-ATTRIBUTE-NAMES-AND-ALIASES)
6. [DEEPER DIVE INTO ATTRIBUTE NAMES](#6.-DEEPER-DIVE-INTO-ATTRIBUTE-NAMES)
7. [SETTING AN ATTRIBUTE WITHOUT CREATING A DICTIONARY ITEM](#7.-SETTING-AN-ATTRIBUTE-WITHOUT-CREATING-A-DICTIONARY-ITEM)
8. [THE AUTO-SAVE FEATURE](#8.-THE-AUTO-SAVE-FEATURE)
9. [CREATING YOUR OWN AUTO-SAVE FUNCTION](#9.-CREATING-YOUR-OWN-AUTO-SAVE-FUNCTION)
10. [CONTRIBUTING](#10.-CONTRIBUTING)
11. [CREDITS](#11.-CREDITS)


## 1. OVERVIEW

`CleverText` is a convenience class that behaves almost exactly like regular Python string but also contain its own self-contained version history and record of actions.  It is mainly intented for recording and comparing different states of text (string, HTML, JSON, code etc) as various transformations (replacements, deletions, validation, parsing) are applied to it. Built in `CleverText` methods (e.g. `diff()`) are readily available for ETL style processing, and can be added easily and consistently, allowing you to segregate common text manipulation function from your main control code for example.


## 2. INSTALLATION

Very lightweight install via `pip`. No dependencies.

    python -m pip install clevertext --upgrade

Then from your Python shell just import the class...

    >>> from clevertext import CleverText


## 3. INPUT METHODS

You can create a `CleverText` instance using keyword arguments:

    >>> x = CleverText("This is the my first draft")


## 4. OUTPUT METHODS



## 5. ATTRIBUTES




## 6. BUILT-IN METHODS



## 7. ADDING YOUR OWN METHODS



## 8. ENABLING AUTO-SAVE


## 9. CREATING YOUR OWN AUTO-SAVE/AUTO-DELETE FUNCTION

As well as autosave/autodelete options baked in to `CleverText`, you can set pretty much any custom function to run **automatically** when a `CleverText` value is *created, changed, or deleted*, for example to update a database, save to a file, or synchronise with cloud storage etc.  Less code for you, and less chance you'll forget to explicitly call that crucial update function...

This can be enabled at a *class* level, or by creating subclasses of `CleverText` with different options, or an *object/instance* level.  We strongly recommend the *object/instance* approach wherever possible, but you have the choice.

### **Autosaving a particular object/instance:**

You can either overwrite the `.save()` / `.delete()` methods when you create your object, or use `.set_autosave()` / `.set_autodelete()` after the event:

### **Autosaving at a class level:**

Simple to do, but beware this could change all existing `CleverText` instances as well as all future ones:

    >>> CleverText.save = your_save_function
    >>> CleverText.delete = your_delete_function

### **Creating Subclasses:**

If you create a subclass of `CleverText` remember to call `super().__init__()` *before* trying to set any further class or object attributes, otherwise you'll run into trouble:

    class AutoStore(CleverText):
        def __init__(self, *args, **kwargs):
            self.setattr_direct('index', [])
            super().__init__(*args, **kwargs)

        def save(self, name, value):
            """ Keep a separate 'store' for data in .index """
            self.index.append((name, value))

    class AutoConfirm(CleverText): pass
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def save(self, name, value):
            """ Print confirmation of the latest change """
            print(f"{name.title()}: {value.upper()}")

### CONTRIBUTING METHODS AS PULL REQUESTS


## 10. CONTRIBUTING TO THE CORE DESIGN

We'd love to see Pull Requests (and relevant tests) from other contributors, particularly if you can help:

* Evolve `CleverText` to make it play nicely with other classes and formats.  [For example: `datetime`](https://github.com/PFython/clevertext/issues/5).
* Put the finishing touches on the **docstrings** to enable autocompletion in modern IDEs (this is neither the author's strong suit nor his passion!).
* Improve the structure and coverage of `test_clevertext.py`.

For a list of all outstanding **Feature Requests** and (heaven forbid!) actual *Issues* please have a look here and maybe you can help out?

https://github.com/PFython/clevertext/issues?q=is%3Aopen+is%3Aissue


## 11. CREDITS
`CleverText` was conceived by Peter Fison and co-developed with the expert assistance of Ruud van der Ham from the friendly and excellent Pythonista Cafe forum (www.pythonistacafe.com).

It follows on from the success of [`CleverDict`](https://github.com/PFython/cleverdict) which is similar in concept and well worth checking out if you haven't already.

If you find `clevertext` helpful, please feel free to:

<a href="https://www.buymeacoffee.com/pfython" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/arial-yellow.png" alt="Buy Me A Coffee" width="217px" ></a>


