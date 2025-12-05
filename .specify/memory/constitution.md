<!--
Sync Impact Report:
Version change: 0.0.0 → 1.0.0
List of modified principles:
  - PRINCIPLE_1_NAME → I. Technical Accuracy
  - PRINCIPLE_2_NAME → II. Clear and Structured Writing
  - PRINCIPLE_3_NAME → III. Balanced Coverage
  - PRINCIPLE_4_NAME → IV. Consistent Terminology and Design
  - PRINCIPLE_5_NAME → V. Modular Content
Added sections: Standards, Content Scope, Constraints, Success Criteria, AI Behavioral Rules
Removed sections: PRINCIPLE_6_NAME, PRINCIPLE_6_DESCRIPTION, SECTION_2_CONTENT, SECTION_3_CONTENT
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending (Constitution Check alignment)
  - .specify/templates/spec-template.md: ⚠ pending (Alignment with Standards, Content Scope, Constraints, Success Criteria, AI Behavioral Rules)
  - .specify/templates/tasks-template.md: ⚠ pending (Influence on task definition and validation)
  - .specify/templates/commands/sp.constitution.md: ✅ updated
  - .specify/templates/commands/sp.phr.md: ⚠ pending (General PHR adherence to constitution)
Follow-up TODOs: none
-->
# Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. Technical Accuracy
All explanations MUST be verifiable and aligned with actual robotics systems (ROS2, sensors, kinematics, locomotion, control). No hallucinated components, sensors, libraries, or APIs.

### II. Clear and Structured Writing
Clear, structured, and pedagogically sound writing. Consistent terminology, formatting, and design across all chapters.

### III. Balanced Coverage
Balanced coverage of theory, architecture, and hands-on implementation.

### IV. Consistent Terminology and Design
Consistent terminology, formatting, and design across all chapters.

### V. Modular Content
Modular content that CAN be read independently.

## Standards

All explanations MUST be verifiable and aligned with actual robotics systems (ROS2, sensors, kinematics, locomotion, control).
Code samples MUST be syntactically correct and realistically runnable.
Markdown output MUST follow Docusaurus conventions (frontmatter, headings, folder structure).
Zero plagiarism; all text MUST be originally generated.
No hallucinated components, sensors, libraries, or APIs.

## Content Scope

Foundations of Physical AI and embodied intelligence.
Humanoid robot design principles.
Kinematics, dynamics, locomotion, balance, and control.
Perception systems (vision, IMU, depth, tactile sensing).
Actuators, motors, mechanical fundamentals.
ROS2 examples and simulation workflows (Gazebo, Isaac Sim).

## Governance
Constitution supersedes all other practices; Amendments REQUIRE documentation, approval, migration plan. All PRs/reviews MUST verify compliance; Complexity MUST be justified; Use [GUIDANCE_FILE] for runtime development guidance.

### Constraints
Output MUST successfully build with `npm run build`.
Only markdown (.md, .mdx) and allowed assets SHOULD be generated.
All technical statements MUST remain within established robotics research.
Maintain consistent tone, clarity, and educational flow.

### Success Criteria
Completed and well-structured Docusaurus book.
Accurate, readable, and consistent chapters.
Build passes without warnings or errors.
Ready for deployment on GitHub Pages.

### AI Behavioral Rules
Prioritize accuracy, clarity, and reproducibility.
Follow the constitution for every chapter and section.
Do not hallucinate technical details.
Request clarification only when context is insufficient.

**Version**: 1.0.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
