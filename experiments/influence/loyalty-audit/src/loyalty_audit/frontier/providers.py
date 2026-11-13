"""Provider-agnostic chat wrappers so the black-box eval runs on closed and open frontier models
behind one interface. Each factory returns a `Generate` callable (system, user) -> text, matching
`detectors.blackbox_judge.Generate`.

Keys are read from the environment and never hardcoded: OPENAI_API_KEY, ANTHROPIC_API_KEY,
DEEPSEEK_API_KEY. DeepSeek exposes an OpenAI-compatible endpoint, so it reuses the OpenAI client with
a different base_url. No key, no call: a missing key raises at factory time, before any network use.

Frontier access reality: OpenAI and Anthropic are closed (no weight or activation access), so the
black-box behavioral protocol is the only thing that runs on them. DeepSeek is also reachable by API
here, and its open weights additionally admit the white-box stage18 measurement on its distilled
models, which is the bridge between the two arms.
"""

from __future__ import annotations

import os
from collections.abc import Callable

Generate = Callable[[str, str], str]


def _require(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        raise RuntimeError(f"{key} is not set; export it before running the frontier eval")
    return val


def openai_generate(model: str = "gpt-4.1", temperature: float = 0.0, max_tokens: int = 512) -> Generate:
    from openai import OpenAI

    client = OpenAI(api_key=_require("OPENAI_API_KEY"))

    def gen(system: str, user: str) -> str:
        r = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return r.choices[0].message.content or ""

    return gen


def deepseek_generate(model: str = "deepseek-chat", temperature: float = 0.0, max_tokens: int = 512) -> Generate:
    from openai import OpenAI

    client = OpenAI(api_key=_require("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

    def gen(system: str, user: str) -> str:
        r = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        )
        return r.choices[0].message.content or ""

    return gen


def anthropic_generate(model: str = "claude-sonnet-4-5", temperature: float = 0.0, max_tokens: int = 512) -> Generate:
    import anthropic

    client = anthropic.Anthropic(api_key=_require("ANTHROPIC_API_KEY"))

    def gen(system: str, user: str) -> str:
        r = client.messages.create(
            model=model,
            system=system,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": user}],
        )
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")

    return gen


# Map a provider name to its factory. The caller picks the concrete model id.
FACTORIES: dict[str, Callable[..., Generate]] = {
    "openai": openai_generate,
    "deepseek": deepseek_generate,
    "anthropic": anthropic_generate,
}


def make_generate(provider: str, model: str, **kw) -> Generate:
    if provider not in FACTORIES:
        raise ValueError(f"unknown provider {provider!r}; choose from {sorted(FACTORIES)}")
    return FACTORIES[provider](model=model, **kw)
