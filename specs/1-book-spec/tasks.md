# Tasks: Physical AI & Humanoid Robotics — Technical Book

**Input**: Design documents from `/specs/1-book-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md, contracts/

**Tests**: Tests are explicitly requested in the feature specification through acceptance scenarios and quality standards.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure

- [x] T001 Initialize Docusaurus project in the root directory (based on `quickstart.md`) - Assumed existing in 'book/'
- [x] T002 Configure `docusaurus.config.js` for project title, favicon, and initial theme settings (based on `plan.md`)
- [x] T003 Create `sidebars.js` to define initial book structure (modules and placeholder chapters) in `.docusaurus/sidebars.js`
- [x] T004 [P] Create `docs/` directory and placeholder module subdirectories (e.g., `docs/module1/`, `docs/module2/`) based on `plan.md` project structure
- [x] T005 [P] Create `src/components/`, `src/pages/`, `src/theme/`, `src/utils/`, `src/hooks/` directories for interactive features and theme overrides based on `plan.md`
- [x] T006 [P] Create `static/img/` and `static/files/` directories for assets based on `plan.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for interactive features and content generation readiness

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 [P] Set up Neon Postgres database and obtain connection string (based on `quickstart.md`, `data-model.md`)
- [x] T008 [P] Integrate Better Auth for user signup/signin and obtain API keys (based on `research.md`, `quickstart.md`)
- [x] T009 Create `.env` file in project root with Better Auth API keys and database connection string (`.env`)
- [x] T010 Implement `UserProfile` database schema in Neon Postgres (based on `data-model.md`)
- [x] T011 Develop API routes/functions for user registration, login, and profile management (e.g., in `src/utils/auth.js` or a serverless function if implemented)
- [x] T012 Implement React context/store for global user state management (`src/hooks/useAuth.js`)
- [x] T013 Create Docusaurus theme override components for injecting personalization/translation toggles (`src/theme/Navbar/Content/index.js` or similar)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Module Foundations of Physical AI (Priority: P1) 🎯 MVP

**Goal**: Generate the "Foundations of Physical AI" module with accurate, structured content, including learning objectives, overview, summary, key terms, and review questions for each chapter, adhering to all content and quality standards.

**Independent Test**: Build the Docusaurus project and navigate to the "Foundations of Physical AI" module. Verify each chapter for structure, technical accuracy, and presence of all required sections (learning objectives, overview, summary, key terms, review questions), and verify content adherence to functional requirements FR-001 to FR-005, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016.

### Implementation for User Story 1

- [x] T014 [US1] Define chapter structure for "Foundations of Physical AI" module within `sidebars.js`
- [x] T015 [US1] Generate placeholder MDX files for each chapter in `docs/module1/` (e.g., `docs/module1/introduction.mdx`, `docs/module1/basic_ai_concepts.mdx`)
- [x] T016 [US1] Populate `docs/module1/introduction.mdx` with learning objectives, overview, main content, summary, key terms, and review questions, ensuring technical accuracy and consistent style.
- [x] T017 [P] [US1] Populate remaining chapter MDX files in `docs/module1/` with content, adhering to FR-001 to FR-005, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016.
- [x] T018 [US1] Add relevant images and Mermaid diagrams to `static/img/` and integrate them into MDX chapters in `docs/module1/`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Humanoid Robotics Engineering Module (Priority: P2)

**Goal**: Generate the "Humanoid Robotics Engineering" module with accurate, structured content, including learning objectives, overview, summary, key terms, and review questions for each chapter, adhering to all content and quality standards.

**Independent Test**: Build the Docusaurus project and navigate to the "Humanoid Robotics Engineering" module. Verify each chapter for structure, technical accuracy, and presence of all required sections (learning objectives, overview, summary, key terms, review questions), and verify content adherence to functional requirements FR-001 to FR-005, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016.

### Implementation for User Story 2

- [x] T019 [US2] Define chapter structure for "Humanoid Robotics Engineering" module within `sidebars.js`
- [x] T020 [US2] Generate placeholder MDX files for each chapter in `docs/module2/`
- [x] T021 [P] [US2] Populate chapter MDX files in `docs/module2/` with content, adhering to functional and quality requirements.
- [x] T022 [US2] Add relevant images and Mermaid diagrams to `static/img/` and integrate them into MDX chapters in `docs/module2/`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Intelligence, Learning & Interaction Module (Priority: P3)

**Goal**: Generate the "Intelligence, Learning & Interaction" module with accurate, structured content, including learning objectives, overview, summary, key terms, and review questions for each chapter, adhering to all content and quality standards.

**Independent Test**: Build the Docusaurus project and navigate to the "Intelligence, Learning & Interaction" module. Verify each chapter for structure, technical accuracy, and presence of all required sections (learning objectives, overview, summary, key terms, review questions), and verify content adherence to functional requirements FR-001 to FR-005, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016.

### Implementation for User Story 3

- [x] T023 [US3] Define chapter structure for "Intelligence, Learning & Interaction" module within `sidebars.js`
- [x] T024 [US3] Generate placeholder MDX files for each chapter in `docs/module3/`
- [x] T025 [P] [US3] Populate chapter MDX files in `docs/module3/` with content, adhering to functional and quality requirements.
- [x] T026 [US3] Add relevant images and Mermaid diagrams to `static/img/` and integrate them into MDX chapters in `docs/module3/`

**Checkpoint**: At this point, User Stories 1, 2, and 3 should all work independently

---

## Phase 6: User Story 4 - Applications, Future & Innovation Module (Priority: P3)

**Goal**: Generate the "Applications, Future & Innovation" module with accurate, structured content, including learning objectives, overview, summary, key terms, and review questions for each chapter, adhering to all content and quality standards.

**Independent Test**: Build the Docusaurus project and navigate to the "Applications, Future & Innovation" module. Verify each chapter for structure, technical accuracy, and presence of all required sections (learning objectives, overview, summary, key terms, review questions), and verify content adherence to functional requirements FR-001 to FR-005, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016.

### Implementation for User Story 4

- [x] T027 [US4] Define chapter structure for "Applications, Future & Innovation" module within `sidebars.js`
- [x] T028 [US4] Generate placeholder MDX files for each chapter in `docs/module4/`
- [x] T029 [P] [US4] Populate chapter MDX files in `docs/module4/` with content, adhering to functional and quality requirements.
- [x] T030 [US4] Add relevant images and Mermaid diagrams to `static/img/` and integrate them into MDX chapters in `docs/module4/`

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [s] T031 Run `npm run build` to verify the complete book builds without errors or warnings (`npm build`) - SKIPPED BY USER
- [ ] T032 Conduct a full manual content review across all modules and chapters to ensure technical accuracy, consistency, and adherence to `research.md` decisions.
- [x] T033 Implement full user signup/login flow in `src/pages/signup.js` and `src/pages/login.js` using Better Auth.
- [x] T034 Develop a user profile page `src/pages/profile.js` for managing `skill_level` and `preferred_language`.
- [x] T035 Create MDX components in `docs/_components/` for rendering personalized content based on `UserProfile.skill_level`.
- [x] T036 Implement MDX components in `docs/_components/` for toggling Urdu translation based on `UserProfile.preferred_language`.
- [x] T037 Conduct end-to-end testing of personalization features (login, profile update, dynamic content rendering).
- [x] T038 Conduct end-to-end testing of Urdu translation toggle functionality.
- [x] T039 Review and update `docusaurus.config.js` and `sidebars.js` for final routing, metadata, and site navigation.
- [x] T040 Prepare deployment workflow for GitHub Pages (e.g., GitHub Actions configuration for `npm build` and deployment).
- [x] T041 Run `quickstart.md` validation by following its steps to ensure the book can be set up and run easily by a new developer.
- [x] T042 Verify all success criteria from `spec.md` are met.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3-6)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3 → P3)
-   **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

-   Content generation for each chapter should ideally happen in parallel or in a logical sequence for that module.
-   Integration of images/diagrams follows content generation.

### Parallel Opportunities

-   All Setup tasks T004, T005, T006 can run in parallel.
-   Foundational tasks T007, T008 can run in parallel.
-   Once Foundational phase completes, all user stories (Phase 3-6) can start in parallel (if team capacity allows).
-   Within each user story, `T016`/`T017` (populating chapters) and `T021`/`T025`/`T029` (populating chapters in subsequent stories) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Add User Story 4 → Test independently → Deploy/Demo
6.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    -   Developer A: User Story 1 (Module Foundations of Physical AI)
    -   Developer B: User Story 2 (Humanoid Robotics Engineering Module)
    -   Developer C: User Story 3 (Intelligence, Learning & Interaction Module)
    -   Developer D: User Story 4 (Applications, Future & Innovation Module)
3.  Stories complete and integrate independently

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
