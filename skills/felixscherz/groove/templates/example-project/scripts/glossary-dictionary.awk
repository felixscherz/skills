# Turns the Banned lines of GLOSSARY.md into a codespell dictionary:
# "- **Banned:** bill, statement" under "## Invoice" becomes "bill->invoice".
/^## / { term = tolower(substr($0, 4)) }
/^- \*\*Banned:\*\*/ {
  sub(/^- \*\*Banned:\*\* */, "")
  n = split($0, words, / *, */)
  for (i = 1; i <= n; i++) print words[i] "->" term
}
