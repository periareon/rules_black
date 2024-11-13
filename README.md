<!-- Generated with Stardoc: http://skydoc.bazel.build -->

# rules_black

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

<a id="py_black_test"></a>

## py_black_test

<pre>
py_black_test(<a href="#py_black_test-name">name</a>, <a href="#py_black_test-config">config</a>, <a href="#py_black_test-target">target</a>)
</pre>

A rule for running black on a Python target.

**ATTRIBUTES**


| Name  | Description | Type | Mandatory | Default |
| :------------- | :------------- | :------------- | :------------- | :------------- |
| <a id="py_black_test-name"></a>name |  A unique name for this target.   | <a href="https://bazel.build/concepts/labels#target-names">Name</a> | required |  |
| <a id="py_black_test-config"></a>config |  The config file (`pyproject.toml`) containing black settings.   | <a href="https://bazel.build/concepts/labels">Label</a> | optional |  `"@rules_black//python/black:config"`  |
| <a id="py_black_test-target"></a>target |  The target to run `black` on.   | <a href="https://bazel.build/concepts/labels">Label</a> | required |  |


<a id="py_black_toolchain"></a>

## py_black_toolchain

<pre>
py_black_toolchain(<a href="#py_black_toolchain-name">name</a>, <a href="#py_black_toolchain-black">black</a>)
</pre>

A toolchain for the [black](https://black.readthedocs.io/en/stable/) formatter rules.

**ATTRIBUTES**


| Name  | Description | Type | Mandatory | Default |
| :------------- | :------------- | :------------- | :------------- | :------------- |
| <a id="py_black_toolchain-name"></a>name |  A unique name for this target.   | <a href="https://bazel.build/concepts/labels#target-names">Name</a> | required |  |
| <a id="py_black_toolchain-black"></a>black |  The black `py_library` to use with the rules.   | <a href="https://bazel.build/concepts/labels">Label</a> | required |  |


<a id="py_black_aspect"></a>

## py_black_aspect

<pre>
py_black_aspect(<a href="#py_black_aspect-name">name</a>)
</pre>

An aspect for running black on targets with Python sources.

**ASPECT ATTRIBUTES**



**ATTRIBUTES**


| Name  | Description | Type | Mandatory | Default |
| :------------- | :------------- | :------------- | :------------- | :------------- |
| <a id="py_black_aspect-name"></a>name |  A unique name for this target.   | <a href="https://bazel.build/concepts/labels#target-names">Name</a> | required |  |


