AI Compiler - Next.js Dashboard

This folder contains a minimal Next.js (app router) dashboard scaffold for the AI Application Compiler.

Pages included:
- `/` Prompt Input
- `/pipeline` Pipeline Viewer
- `/validation` Validation Viewer
- `/repair` Repair Viewer
- `/runtime` Runtime Preview
- `/metrics` Metrics Dashboard

Notes:
- Components use Tailwind CSS utility classes; ensure Tailwind is configured in the project.
- This is a UI scaffold with placeholder interactions. Connect to the backend API (`/v1/...`) and wire data fetching in the client components.

Run (from repository root) - example:

```bash
cd web
npm install
npm run dev
```

Adjust based on your monorepo tooling (pnpm, Turborepo, Next workspace settings).
