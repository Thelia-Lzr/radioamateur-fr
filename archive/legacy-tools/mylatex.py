#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unicode-maths -> LaTeX body converter shared by every conversion pass.

tex(expr) returns the *body* of a formula (no delimiters).  Wrap it
yourself with \\( \\) or \\[ \\].
"""
import re

# ---------------------------------------------------------------- symbols
GREEK = {
    "λ": r"\lambda", "Λ": r"\Lambda", "π": r"\pi", "Π": r"\Pi",
    "τ": r"\tau", "μ": r"\mu", "µ": r"\mu", "ε": r"\varepsilon",
    "Ω": r"\Omega", "ω": r"\omega", "Ω": r"\Omega",
    "ρ": r"\rho", "η": r"\eta", "θ": r"\theta", "Θ": r"\Theta",
    "φ": r"\varphi", "ϕ": r"\phi", "Φ": r"\Phi", "Δ": r"\Delta",
    "δ": r"\delta", "β": r"\beta", "α": r"\alpha", "γ": r"\gamma",
    "σ": r"\sigma", "ν": r"\nu",
}

OPS = {
    "·": r" \cdot ", "⋅": r" \cdot ", "×": r" \times ", "÷": r" \div ",
    "−": "-", "–": "-", "—": "-", "≈": r" \approx ", "≤": r" \leq ",
    "≥": r" \geq ", "≠": r" \neq ", "⇒": r" \Rightarrow ",
    "⟹": r" \Longrightarrow ", "→": r" \rightarrow ", "∝": r" \propto ",
    "∞": r"\infty", "±": r" \pm ", "≪": r" \ll ", "≫": r" \gg ",
}

SUP = {"²": "^2", "³": "^3", "¹": "^1", "⁰": "^0", "⁴": "^4",
       "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9",
       "⁻": "^-", "⁺": "^+"}

# multi-char subscripts written inline in the source
SUBSCRIPTS = [
    ("càc", "c\\`ac"), ("eff_total", "eff\\_total"),
    ("eff", "eff"), ("max", "max"), ("mini", "mini"), ("moy", "moy"),
    ("cont", "cont"), ("bouchon", "bouchon"), ("série", "s\\'erie"),
    ("courbe", "courbe"), ("ligne", "ligne"),
]

UNIT_WORDS = {
    "V", "A", "W", "J", "C", "F", "H", "T", "Wb", "Hz", "dB", "dBm",
    "rad", "m", "mm", "cm", "km", "s", "ms", "µs", "ns", "pF", "nF",
    "µF", "mF", "mH", "µH", "nH", "kΩ", "MΩ", "Ω", "mV", "kV",
    "mA", "µA", "µW", "mW", "kW", "kΩ", "MHz", "kHz", "GHz", "VA",
    "Wb", "A/m", "V/m", "rad/s", "pF/m", "H/m",
}


def _restore_html_subsup(expr):
    """<sub>x</sub> -> _{x} , <sup>x</sup> -> ^{x}"""
    expr = re.sub(r"<sub>\s*([^<]*?)\s*</sub>", r"_{\1}", expr)
    expr = re.sub(r"<sup>\s*([^<]*?)\s*</sup>", r"^{\1}", expr)
    return expr


def _symbols(expr):
    for k, v in GREEK.items():
        expr = expr.replace(k, v + " ")
    for k, v in SUP.items():
        expr = expr.replace(k, v)
    for k, v in OPS.items():
        expr = expr.replace(k, v)
    return expr


def _sqrt(expr):
    """√(...) , √[...] , √token  ->  \\sqrt{...}"""
    out = []
    i = 0
    while i < len(expr):
        if expr[i] == "√":
            j = i + 1
            while j < len(expr) and expr[j] == " ":
                j += 1
            if j < len(expr) and expr[j] in "([":
                close = ")" if expr[j] == "(" else "]"
                depth = 0
                k = j
                while k < len(expr):
                    if expr[k] in "([":
                        depth += 1
                    elif expr[k] in ")]":
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                inner = expr[j + 1:k]
                out.append("\\sqrt{%s}" % tex(inner, nested=True))
                i = k + 1
                continue
            m = re.match(r"[A-Za-z0-9_^{}]+", expr[j:])
            if m:
                out.append("\\sqrt{%s}" % tex(m.group(0), nested=True))
                i = j + len(m.group(0))
                continue
        out.append(expr[i])
        i += 1
    return "".join(out)


ATOM = r"(?:\([^()]*\)|\[[^\[\]]*\]|[A-Za-z0-9_^{}\\\.\s\+\-]+)"


def _fractions(expr):
    """A / B -> \\frac{A}{B}, but leave pure numeric division alone."""
    def repl(m):
        num, den = m.group(1).strip(), m.group(2).strip()
        if not num or not den:
            return m.group(0)
        if not re.search(r"[A-Za-z\\]", num + den):
            return m.group(0)          # 300/7 stays 300/7
        return "\\frac{%s}{%s}" % (tex(num, nested=True), tex(den, nested=True))

    pat = re.compile(r"(%s)\s*/\s*(%s)" % (ATOM, ATOM))
    prev = None
    while prev != expr:
        prev = expr
        expr = pat.sub(repl, expr)
    return expr


def tex(expr, nested=False):
    """Convert one plain-text formula body to LaTeX."""
    expr = _restore_html_subsup(expr)
    expr = _symbols(expr)
    expr = _sqrt(expr)
    if not nested:
        expr = _fractions(expr)
    # subscripts written as bare names
    expr = re.sub(r"\b([A-Z])càc\b", r"\1_{c\\`ac}", expr)
    expr = re.sub(r"\b([A-Z])(eff|max|mini|moy|cont|bouchon|ligne)\b",
                  r"\1_{\2}", expr)
    # units in parentheses -> \text{}
    expr = re.sub(r"\(\s*([A-Za-zµΩ][A-Za-z0-9µΩ/²]*)\s*\)",
                  lambda m: r"\,(\text{%s})" % m.group(1))
    expr = re.sub(r"\s{2,}", " ", expr)
    return expr.strip()


if __name__ == "__main__":
    import sys
    for line in sys.argv[1:]:
        print(repr(line), "->", tex(line))
