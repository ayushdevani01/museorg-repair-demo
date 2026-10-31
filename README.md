# MuseOrg repair demo

A disposable public acceptance fixture. The website has a deliberately seeded missing entry point. MuseOrg's coworker must diagnose it, repair it, pass the independent HTTP regression check, open a PR and merge only its green reviewed head. GitHub Pages publishes the result. This is a disclosed test incident, not a customer outage.

Run the check with `python3 -m unittest discover -s tests -v`. The initial failing result is intentional. Site changes belong in `docs/`; the coworker cannot edit the workflow or test through its scoped delivery connection.
