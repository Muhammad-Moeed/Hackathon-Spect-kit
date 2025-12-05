# Research Decisions: Physical AI & Humanoid Robotics — Technical Book

## Markdown vs MDX in Docusaurus

*   **Options:** Markdown, MDX
*   **Pros & Cons:**
    *   **Markdown:** Simpler to write, widely supported, faster initial content generation. Less interactive. Limited component integration.
    *   **MDX:** Allows embedding React components directly within markdown, enabling interactive features (personalization, translation toggles), richer content presentation. Steeper learning curve, requires more setup for components.
*   **Final Choice:** MDX
*   **Rationale:** To support the bonus interactive features (personalized content, Urdu translation toggle) and to create a richer, more dynamic educational experience, MDX is essential. While slightly more complex, its benefits for interactive elements outweigh the simplicity of pure Markdown for this project.

## Diagram Format: Mermaid vs PNG vs MDX Components

*   **Options:** Mermaid, PNG/JPG, Custom MDX Components
*   **Pros & Cons:**
    *   **Mermaid:** Text-based, version controllable, can be rendered dynamically in Docusaurus. Limited complexity for highly detailed diagrams.
    *   **PNG/JPG:** High fidelity, easy to create with external tools. Not version controllable in text, harder to update, larger file sizes.
    *   **Custom MDX Components:** Highly customizable, interactive diagrams possible, version controllable if logic is in code. Requires significant development effort.
*   **Final Choice:** Combination of Mermaid and PNG/JPG
*   **Rationale:** For standard flowcharts, sequence diagrams, and simpler architectural views, Mermaid offers version control and dynamic rendering within Docusaurus. For complex schematics, 3D renderings, or detailed anatomical diagrams of robots, high-fidelity PNG/JPG images will be used. MDX components will be considered for future interactive diagram needs if time permits, but are not a primary choice for initial content generation due to development overhead.

## GitHub Pages Deployment vs Alternative

*   **Options:** GitHub Pages, Netlify, Vercel, Self-hosted
*   **Pros & Cons:**
    *   **GitHub Pages:** Free, tightly integrated with GitHub (version control, CI/CD), simple setup for Docusaurus projects. Limited customizability for advanced server-side features.
    *   **Netlify/Vercel:** Excellent developer experience, robust CI/CD, serverless functions, custom domains. May incur costs for higher usage.
    *   **Self-hosted:** Full control over infrastructure. Requires significant DevOps effort and cost.
*   **Final Choice:** GitHub Pages
*   **Rationale:** Given the project's objective of generating an educational book and deploying it easily, GitHub Pages offers a free, straightforward, and well-integrated solution with Docusaurus. It aligns perfectly with the goal of an open-source, easily accessible technical book.

## Folder Structure for Modules and Interactive Features

*   **Options:** Flat structure, Module-based `docs/` hierarchy, `src/` for all interactive features, `plugins/` for Docusaurus plugins.
*   **Pros & Cons:**
    *   **Module-based `docs/` hierarchy:** Clear separation of book content by modules and chapters. Aligns with Docusaurus best practices for content organization.
    *   **`src/` for interactive features:** Standard Docusaurus approach for custom React components, pages, and theme overrides. Keeps interactive code separate from content.
*   **Final Choice:** Module-based hierarchy in `docs/` and standard Docusaurus `src/` for interactive features.
*   **Rationale:** This approach leverages Docusaurus's strengths for content organization while providing a clear separation for custom interactive components. It will ensure maintainability and scalability for both the book content and its interactive elements.

## Research Methodology: Phase-wise vs Full Upfront

*   **Options:** Research-concurrent (phase-wise), Full upfront research
*   **Pros & Cons:**
    *   **Research-concurrent (phase-wise):** Allows for iterative content generation, potentially faster initial drafts, and focused research on immediate needs. Risk of incomplete research or re-work if fundamental aspects change.
    *   **Full upfront research:** Ensures comprehensive understanding before writing, reduces re-work. Can delay initial content production and lead to analysis paralysis.
*   **Final Choice:** Research-concurrent (phase-wise)
*   **Rationale:** Given the iterative nature of AI-driven content generation with Claude Code and SpecKit Plus, a research-concurrent approach is more agile. This allows for research to be conducted as modules and chapters are being generated, ensuring up-to-date and targeted information while maintaining a steady production flow. Critical foundational research will be prioritized.

## Personalization Storage: Local vs Serverless (Neon Postgres)

*   **Options:** Local Storage (browser), Serverless Database (Neon Postgres), Dedicated Backend Service
*   **Pros & Cons:**
    *   **Local Storage:** Simplest to implement, client-side only, no backend required. Limited data size, not suitable for persistent or cross-device personalization, security concerns for sensitive data.
    *   **Serverless Database (Neon Postgres):** Scalable, persistent, cross-device data. Integrates well with serverless functions for authentication (Better Auth). Introduces cost and complexity of database management.
    *   **Dedicated Backend Service:** Full control, highly customizable. Significant operational overhead, higher cost.
*   **Final Choice:** Serverless Database (Neon Postgres) with Better Auth
*   **Rationale:** To provide robust, persistent, and cross-device user personalization, a serverless database like Neon Postgres integrated with Better Auth is the most appropriate solution. It balances scalability and persistence with reduced operational overhead compared to a dedicated backend, aligning with a GitHub Pages deployment model.

## How Urdu Translation is Implemented (Dynamic MDX vs Separate Files)

*   **Options:** Dynamic MDX rendering with content switching, Separate localized MDX files, External Translation API (real-time)
*   **Pros & Cons:**
    *   **Dynamic MDX rendering:** Single source of truth for content, translation logic embedded in components, cleaner file structure. Can be complex to implement robustly, potential performance impact for large content blocks.
    *   **Separate localized MDX files:** Clear separation of content for each language, simpler rendering logic. Duplication of content, higher maintenance for updates, increased file count.
    *   **External Translation API (real-time):** No manual translation effort, always up-to-date. Dependent on external service, potential cost, latency, and quality concerns.
*   **Final Choice:** Dynamic MDX rendering with content switching
*   **Rationale:** To avoid content duplication and simplify updates, dynamic MDX rendering with content switching is preferred. This allows the Urdu translation to be toggled within the same chapter, providing a seamless user experience. While it requires careful component design, it maintains a single source for content and improves maintainability over separate files. Manual translation for quality will be assumed, rather than real-time API.
