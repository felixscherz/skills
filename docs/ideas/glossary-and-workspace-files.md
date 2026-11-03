Instead of having a complex feature map, workspace map and so on, have a single toplevel CONTEXT.md
and if required this maps out to more files, ideally in docs/ folder. So CONTEXT.md could reference
a docs/feature_map.md that takes the role of the existing feature map. It can then reference more code
and docs. If there are multiple contexts a toplevel CONTEXT.md references other CONTEXT.md and so on.


A workspace map should go completely, that is more about adding instructions to the harness so it has
context information around the folder structure, really can't put that in a skill. The reason I built
it is so I can reference a workspace map in other skills, lets see if that was useful.

GLOSSARY.md is then at docs/glossary.md and referenced by the CONTEXT.md.

AGENTS.md points to CONTEXT.md to find something or gather information.
