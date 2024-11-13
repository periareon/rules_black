"""rules_black dependencies"""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

# buildifier: disable=unnamed-macro
def rules_black_dependencies():
    """Defines black dependencies"""
    maybe(
        http_archive,
        name = "rules_venv",
        integrity = "sha256-W6w2jYgQW1jA2WScHMSyxnKH+Pi2m/LmjUoGpJgD4Lg=",
        urls = ["https://github.com/periareon/rules_venv/releases/download/0.0.6/rules_venv-0.0.6.tar.gz"],
    )

# buildifier: disable=unnamed-macro
def register_black_toolchains(register_toolchains = True):
    """Defines pytest dependencies"""
    if register_toolchains:
        native.register_toolchains(
            str(Label("//python/black/toolchain")),
        )
