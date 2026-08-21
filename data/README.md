# Data

## Sample data

The `sample/` directory contains deterministic synthetic data generated for product development and automated testing. It does not describe real people, accounts, campaigns, or business results.

Generate or refresh it with:

```powershell
node scripts/generate_sample_data.mjs
```

Validate it with:

```powershell
$env:PYTHONPATH="src"
python -m influencertrust.data_validation data/sample
```

## Privacy and licensing

- Do not commit private exports to this repository.
- Do not add scraped data that violates a platform's terms.
- Record the source and license before adding any public dataset.
- Remove direct personal identifiers unless they are necessary and lawfully usable.
- The repository's MIT License does not automatically apply to third-party data.

Directories named `raw/` and `private/` are excluded by `.gitignore`.
