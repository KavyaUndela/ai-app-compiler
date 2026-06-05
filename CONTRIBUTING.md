# Contributing Guide

Thank you for your interest in contributing to the AI Application Compiler!

## Getting Started

### Prerequisites
- Git
- Python 3.12+
- Node.js 18+
- Docker & Docker Compose (optional)

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/ai-compiler.git
cd ai-compiler

# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Additional dev tools

# Frontend setup
cd ../frontend
npm install

# Copy environment files
cp ../.env.example ../.env
cp .env.example .env.local
```

### Running Tests

```bash
# Backend tests
cd backend
pytest -v
pytest --cov=app tests/

# Frontend tests
cd ../frontend
npm test

# Backend pipeline test
cd ../backend
python test_pipeline.py
```

## Architecture

### 6-Stage Pipeline

Each stage is a independent service with clear interfaces:

```
Intent Extraction (Stage 1)
    ↓ Output: IntentSchema
System Design (Stage 2)
    ↓ Output: SystemDesignSchema
Schema Generation (Stage 3)
    ↓ Output: SchemaGenerationResult
Validation Engine (Stage 4)
    ↓ Output: ValidationResult
Repair Engine (Stage 5)
    ↓ Output: RepairResult
Runtime Simulator (Stage 6)
    ↓ Output: RuntimePreview
```

### Service Structure

Each service follows this pattern:

```python
# backend/app/services/[service_name].py

from app.models import InputSchema, OutputSchema

def process(input: InputSchema) -> OutputSchema:
    """
    Main processing function
    
    Args:
        input: Typed input model
        
    Returns:
        Typed output model
    """
    # Implementation
    return OutputSchema(...)
```

### Adding a New Stage

1. **Create service file:**
```python
# backend/app/services/my_new_stage.py

from uuid import uuid4
from app.models import InputSchema, OutputSchema

def process_stage(input: InputSchema) -> OutputSchema:
    """Process stage logic"""
    return OutputSchema(
        stage_id=str(uuid4()),
        # ... other fields
    )
```

2. **Update models:**
```python
# backend/app/models.py

class OutputSchema(BaseModel):
    stage_id: str
    # ... fields
    
class CompilationResult(BaseModel):
    # ... existing fields
    my_new_stage: OutputSchema | None = None
```

3. **Add to routes:**
```python
# backend/app/api/routes.py

from app.services.my_new_stage import process_stage

@app.post("/generate")
async def generate(request: GenerateRequest):
    # ... existing stages
    my_new_stage = process_stage(previous_output)
    # ... return result
```

4. **Add frontend page:**
```typescript
// frontend/src/pages/my-stage.tsx

export default function MyStage() {
  const compilation = useCompilerStore((s) => s.currentCompilation);
  
  if (!compilation?.my_new_stage) {
    return <div>No data</div>;
  }
  
  return (
    <Layout>
      {/* Display my_new_stage data */}
    </Layout>
  );
}
```

## Code Style

### Backend (Python)

- **PEP 8** compliant
- Type hints required
- Docstrings for all functions
- Max line length: 100

```python
def extract_entities(prompt: str) -> list[str]:
    """
    Extract entities from natural language prompt.
    
    Args:
        prompt: Natural language input
        
    Returns:
        List of extracted entities
        
    Examples:
        >>> extract_entities("Build a CRM")
        ["CRM"]
    """
    entities = []
    # Implementation
    return entities
```

### Frontend (TypeScript/React)

- **ESLint** configured
- **Prettier** for formatting
- Type definitions required
- Functional components with hooks

```typescript
interface MyComponentProps {
  data: CompilationResult;
  onUpdate: (data: CompilationResult) => void;
}

export function MyComponent({ data, onUpdate }: MyComponentProps) {
  const [state, setState] = useState<string>("");
  
  return (
    <div>
      {/* Component JSX */}
    </div>
  );
}
```

## Testing

### Backend Testing

```python
# backend/app/services/test_my_service.py

import pytest
from app.services.my_service import process_stage
from app.models import InputSchema, OutputSchema

def test_process_stage():
    """Test the process stage function"""
    input_data = InputSchema(...)
    result = process_stage(input_data)
    
    assert result.stage_id
    assert isinstance(result, OutputSchema)

def test_process_stage_error():
    """Test error handling"""
    with pytest.raises(ValueError):
        process_stage(invalid_input)
```

### Frontend Testing

```typescript
// frontend/src/components/MyComponent.test.tsx

import { render, screen } from "@testing-library/react";
import MyComponent from "./MyComponent";

describe("MyComponent", () => {
  it("renders correctly", () => {
    const data = { /* test data */ };
    render(<MyComponent data={data} />);
    
    expect(screen.getByText("Expected text")).toBeInTheDocument();
  });
});
```

## Commit Guidelines

Follow conventional commits:

```
feat(intent): add sentiment analysis to intent extraction
fix(validation): correct error message for missing PKs
docs(api): update endpoint documentation
test(repair): add confidence score tests
refactor(design): simplify module generation
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Make changes and commit:
   ```bash
   git commit -m "feat(stage): add new capability"
   ```
4. Push to branch:
   ```bash
   git push origin feature/my-feature
   ```
5. Open Pull Request with description:
   - What changes are made
   - Why the changes are needed
   - How to test the changes
   - Any breaking changes

## Performance Guidelines

### Backend

- Intent extraction: target < 200ms
- Schema generation: target < 100ms
- Validation: target < 50ms
- Use caching for repeated computations

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_operation(key: str) -> dict:
    # Cached result
    pass
```

### Frontend

- Page load: target < 2s
- API response handling: show loading state
- Use React.memo for expensive components

```typescript
const MyComponent = React.memo(({ data }: Props) => {
  return <div>{data}</div>;
});
```

## Documentation

### Code Comments

- Explain **why**, not what
- Bad: `i = i + 1  # Add 1 to i`
- Good: `i = i + 1  # Move to next batch item`

### Docstrings

```python
def my_function(param: str) -> int:
    """
    Brief description on one line.
    
    Longer description if needed, explaining
    the purpose and behavior.
    
    Args:
        param: Description of param
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param is empty
        
    Examples:
        >>> my_function("test")
        42
    """
    pass
```

## Release Process

1. Update version in:
   - `backend/app/main.py` (API_VERSION)
   - `frontend/package.json`
   - Top-level `VERSION` file

2. Create release notes in `CHANGELOG.md`

3. Tag release:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. Build and publish Docker images:
   ```bash
   docker build -t ai-compiler:1.0.0 .
   docker push ai-compiler:1.0.0
   ```

## Troubleshooting Development

### Issue: Backend won't start

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check port
lsof -i :8000
```

### Issue: Frontend build fails

```bash
# Clear Next.js cache
rm -rf frontend/.next

# Reinstall node_modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Issue: Tests fail

```bash
# Run with verbose output
pytest -vv tests/

# Run specific test
pytest tests/test_intent_extraction.py::test_extract_entities -vv
```

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Pydantic Docs](https://docs.pydantic.dev)
- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs)

## Code of Conduct

- Be respectful
- Be inclusive
- Give credit
- Focus on code, not personality
- Report issues to maintainers

## Questions?

- Open an issue
- Start a discussion
- Check existing documentation
- Review closed issues

---

Thank you for contributing! 🎉
