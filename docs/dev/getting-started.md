# Developer Onboarding

Follow these steps the first time you set up the monorepo:

1. **Install prerequisites**
   - Python 3.11+
   - [Poetry](https://python-poetry.org/docs/#installation) (via `pipx install poetry`)
   - Node.js 20+
   - [pnpm](https://pnpm.io/installation) (`npm install -g pnpm`)
   - [pre-commit](https://pre-commit.com/#install) (`pipx install pre-commit`)
   - Docker (for integration tests)
   - `kubeseal`, `kubectl`, `terraform`, etc., if you work on infra

2. **Bootstrap the workspace**
   ```bash
   make setup            # runs scripts/bootstrap.sh (checks tooling, installs deps)
   make install-python   # poetry install --no-root
   make install-js       # pnpm install
   ```

3. **Run validation**
   ```bash
   make lint
   make test
   ```

4. **Configure secrets**
   - Copy `.env.example` files to `.env` locally.
   - Request sealed secrets for shared environments via `docs/ops/secrets.md`.

5. **Read the policies**
   - Coding standards (`docs/dev/standards.md`, when available)
   - Third-party dependency policy (`third_party/policy.md`)

Questions? Reach out in the `#monorepo` channel or tag the relevant code owners.
