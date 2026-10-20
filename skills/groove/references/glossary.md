# Glossary and shared names

## The rule

Every domain concept has exactly one canonical term, defined in
`docs/glossary.md` and linked from the repository's `CONTEXT.md`. There is
one glossary for the whole repository: the modules of a Groove codebase are
parts of one bounded context and share its language.

- Use the canonical term everywhere the concept appears: class, function,
  variable, field, module, test name, docstring, README, log message, error
  message, commit message, and your replies to the user.
- Never use a banned synonym, in any casing or inflection.
- When no term fits, do not invent a name and move on. Add a `proposed` entry
  to the glossary in the same change and tell the user.
- When a term is renamed, rename every occurrence in the same change and move
  the old name to the banned list.

### What belongs in the glossary

Concepts a domain expert would recognize: entities (`Invoice`), value objects
(`Money`), states (`issued`), roles (`Customer`), events (`InvoiceIssued`),
and domain verbs (`issue` an invoice, not `send`, `finalize`, or `submit`).
Verbs matter as much as nouns: they become function names.

Technical concepts stay out: `repository`, `adapter`, `retry`, `cache`. Their
names follow normal Python conventions, not the glossary.

### Entry format

```markdown
## Invoice

A request for payment sent to a Customer for one or more Line Items.

- **Code:** `Invoice`, `invoice`, `invoice_id`
- **Banned:** bill, statement
- **Status:** accepted
```

- **Heading:** the term in its natural-language form.
- **Definition:** one or two sentences. Refer to other terms by their
  headings, capitalized, so readers can follow the links.
- **Code:** the identifier forms in use. Snake case for functions,
  variables, and modules; Pascal case for classes; plurals as needed.
- **Banned:** synonyms that agents or humans have reached for. Grows over
  time. Every rename adds the old name here.
- **Status:** `accepted`, or `proposed` for terms an agent added that a human
  has not reviewed yet.

Optional lines: **Not to be confused with:** for neighbouring terms, and
**External names:** for what external systems call it (see below).

### Using terms in identifiers

- Compose from terms: `issued_invoices`, `InvoiceIssued`, `issue_invoice`.
- Do not abbreviate a term unless the abbreviation is listed under **Code**.
  `inv`, `cust`, and `li` are as bad as synonyms.
- Do not qualify a term with vague words: `invoice_data`, `invoice_info`,
  `invoice_obj`, `InvoiceManager`. Either the bare term is right, or a
  distinct concept exists and needs its own entry.

### Proposing a term

1. Search the glossary for the concept under every name you can think of. It
   may exist under a term you did not expect.
2. If it exists, use it.
3. If not, add an entry with `**Status:** proposed`, a definition, and the
   banned synonyms you considered.
4. Mention the proposal in the Groove feedback section of your reply.

If a term you need already exists but means something different in the part
of the code you are working on, stop and ask the user. Do not add a second
meaning, and do not pick a near-synonym to dodge the clash.

### External vocabulary

External systems have their own names (a payment provider's `charge`, an
API's `client`). Those names may appear only in the adapter that talks to
that system. The adapter translates into glossary terms at the boundary, so
the rest of the code never sees the external name. Record the external name
under **External names:** so the translation is documented.

## Why

Agents pick names by pattern-matching on what is nearby and on their
training data. Without a single source, each session picks a slightly
different word, and after a few weeks the code says `client`, `customer`,
`account`, and `user` for one concept. Every later reader, agent or human,
then has to work out whether those are the same thing. Search stops working,
because grepping for `customer` misses the `client` code paths.

A glossary turns a judgement call ("what should I call this?") into a lookup.
The banned list records the mistakes already made, so they are not made
again.

## Example

The glossary defines **Customer** (banned: client, buyer) and **Issue**
(banned: send, finalize).

Bad:

```python
def finalize_bill(client_id: str, bill: dict[str, object]) -> dict[str, object]:
    bill["state"] = "sent"
    return bill
```

Good:

```python
def issue(invoice: Invoice, now: datetime) -> Invoice:
    return replace(invoice, status=InvoiceStatus.ISSUED, issued_at=now)
```

## Codify it

Not codified yet, on purpose: the glossary's format is still open. Do not
add or propose a check for it. Review names by hand instead.

## Review by hand

No tool checks the glossary yet, so every name is reviewed by hand.

- For each identifier, test name, and doc line your change added that names
  a domain concept, find its glossary entry.
- Check that each new concept has a `proposed` entry.
- Search your change for the banned synonyms of each term it touches,
  inside identifiers too (`finalize_bill`, `clientBill`).
- When you notice a near-synonym that is not banned yet, add it to
  **Banned** so the next agent avoids it.
- Ask: would a domain expert reading this code recognize every noun and verb?
