# Holbertonschool HBnB – UML Deliverables

This repository contains the UML documentation for the HBnB project (Holberton). Diagrams are written in Mermaid and organized under `part1/`.

## Repository Structure
- `part1/` – all Part 1 UML assets.
  - `high-level_package_diagram.md` – three-layer architecture with Facade.
  - `class_diagram_for_business_logic_layer.md` – core domain class diagram (canonical); `business-logic-layer-class-diagram.md` is a duplicate reference.
  - Sequence diagrams: `user-registration.md`, `place-creation.md`, `review-submission.md`, `fetch-List-of-places.md`.
  - `sequence_diagrams_for_api_calls.md` – aggregated sequence diagrams.
  - `doc_compilation.md` – compiled technical document embedding the diagrams.
  - `README.md` – part-specific guide.

## Viewing the Diagrams
Open the Markdown files in a viewer that supports Mermaid (e.g., VS Code with Mermaid preview enabled). If Mermaid is disabled, turn it on or paste the code blocks into an online Mermaid renderer.

## Notes
- Diagrams are text-based for version control friendliness.
- Keep `class_diagram_for_business_logic_layer.md` as the single source for the business-logic class diagram to avoid divergence.
