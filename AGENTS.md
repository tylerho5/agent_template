# AGENTS.md

## Build/Lint/Test Commands
- Build: `npm run build`
- Lint: `npm run lint` (ESLint)
- Type Check: `npm run typecheck`
- Test All: `npm test`
- Test Single File: `npm test -- tests/unit/<file>.test.ts`

## Code Style Guidelines
- **Imports**: Group external > parent > sibling > same-level; sort alphabetically
- **Formatting**: Prettier (2-space), no trailing commas
- **Types**: Strict TypeScript, no implicit `any`
- **Naming**: camelCase (vars), PascalCase (components)
- **Errors**: Log with context via structured logger

## Special Instructions
- **Cursor Rules**: None found
- **Copilot**: None configured
- **Pre-commit**: Husky runs lint-staged
- **Security**: Never log secrets, validate all inputs