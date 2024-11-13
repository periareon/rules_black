"""# rules_black

## Overview

Bazel rules for the Python formatter [black][blk].

### Setup

To setup the rules for `black`, define a [py_black_toolchain](#py_black_toolchain) within your
project and register it within your workspace. For example say you have the following `BUILD.bazel`
file in the root of your workspace:

```python
load("@rules_black//python/black:defs.bzl", "py_black_toolchain")

package(default_visibility = ["//visibility:public"])

py_black_toolchain(
    name = "py_black_toolchain",
    black = "@pip_deps//:black",
)

toolchain(
    name = "toolchain",
    toolchain = ":py_black_toolchain",
    toolchain_type = "@rules_black//python/black:toolchain_type",
)
```

You would then add the following to your `WORKSPACE.bazel` file.

```python
register_toolchains("//tools/black:toolchain")
```

With dependencies loaded in the workspace, python code can be formatted by simply running:
`bazel run @rules_black//python/black`.

In addition to this formatter, a check can be added to your build phase using the [py_black_aspect](#py_black_aspect)
aspect. Simply add the following to a `.bazelrc` file to enable this check.

```text
build --aspects=@rules_black//python/black:defs.bzl%py_black_aspect
build --output_groups=+py_black_checks
```

These rules use a global flag to determine the location of the configuration file to use with black. To wire up a custom
config file, simply add the following to your `.bazelrc` file

```text
build build --@rules_black//python/black:config=//:pyproject.toml
```

Note the flag above assumes you have a `pyproject.toml` in the root of your repository.

It's recommended to only enable this aspect in your CI environment so formatting issues do not
impact user's ability to rapidly iterate on changes.


[blk]: https://black.readthedocs.io/en/stable/index.html

## Rules

- [py_black_aspect](#py_black_aspect)
- [py_black_test](#py_black_test)
- [py_black_toolchain](#py_black_toolchain)

---

---
"""

load(
    "//python/black/private:black.bzl",
    _py_black_aspect = "py_black_aspect",
    _py_black_test = "py_black_test",
)
load(
    "//python/black/private:black_toolchain.bzl",
    _py_black_toolchain = "py_black_toolchain",
)

py_black_aspect = _py_black_aspect
py_black_test = _py_black_test
py_black_toolchain = _py_black_toolchain
