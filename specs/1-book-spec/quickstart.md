# Quickstart Guide: Physical AI & Humanoid Robotics — Technical Book

This guide will help you set up and run the Docusaurus project for the "Physical AI & Humanoid Robotics" technical book locally.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Node.js**: Version 18 or later (LTS recommended)
*   **npm**: Version 8 or later (comes with Node.js)
*   **Git**: For cloning the repository

## 1. Clone the Repository

First, clone the project repository from GitHub:

```bash
git clone [YOUR_REPOSITORY_URL]
cd [YOUR_REPOSITORY_NAME]
```

## 2. Install Dependencies

Navigate to the project root and install the necessary Node.js dependencies using npm:

```bash
npm install
```

## 3. Start the Development Server

Once the dependencies are installed, you can start the Docusaurus development server:

```bash
npm run start
```

This command will build the static assets and launch a local development server. The book will typically be accessible at `http://localhost:3000` in your web browser.

Any changes you make to the markdown/MDX content (`docs/` directory) or Docusaurus configuration (`.docusaurus/` and `src/` directories) will automatically trigger a rebuild and refresh in your browser.

## 4. Build for Production

To build the book for production (e.g., for deployment to GitHub Pages), run the following command:

```bash
npm run build
```

This will generate static content in the `build/` directory. This content can then be deployed to a static hosting service like GitHub Pages.

## 5. Better Auth and Personalization Setup (Optional for Local Development)

For local development of interactive features (user authentication, personalization, Urdu translation toggle), you will need to set up Better Auth and a Neon Postgres database.

1.  **Create a Neon Postgres Database:** Sign up for Neon and create a new Postgres database. Obtain your connection string.
2.  **Configure Better Auth:** Follow the Better Auth documentation to set up a project and integrate it with your Neon Postgres database. Obtain your API keys and configuration details.
3.  **Environment Variables:** Create a `.env` file in the project root and add the necessary environment variables for Better Auth and your database connection string. Consult Better Auth documentation for required variables.

Example `.env` file:

```
BETTER_AUTH_API_KEY=your_better_auth_api_key
DATABASE_URL="postgres://user:password@host:port/database"
```

**Note**: Interactive features will gracefully degrade or be disabled if Better Auth and database configurations are not present during local development.
