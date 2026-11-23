# Jewllion Questions

`questions.json` contains the current pack. Upload previous playable JSON packs
directly into `packs/`, using a unique filename for each pack, for example
`packs/jewish-trivia-05.json`.

The **Update Previous Packs** GitHub Action automatically rebuilds
`packs/index.json` after packs are added, updated, or removed on `main`.
The website uses this catalog for its pack picker. No Netlify deployment is
needed for subsequent pack uploads, once the archive-enabled website is deployed.
GitHub's raw-file cache may take several minutes to show updates.

- Both native pack JSON and the website's `{"pack": {...}}` wrapper are supported.
- Keep packs directly in `packs/`, not in nested folders.
- Do not name a pack `index.json`; that file is generated automatically.
- Removing a pack from `packs/` removes it from the picker after indexing.
- Uploading an archived pack does not change the default `questions.json`.
- Do not upload private data: questions, answers, and the catalog are public.

The action needs GitHub Actions enabled and permission to commit to `main`.
If branch protection prevents the bot from pushing, run the generator locally
and submit its updated catalog through the repository's normal review process.
Malformed JSON or missing pack metadata fails indexing rather than silently
omitting the pack. The website also fully validates each pack before play.

To regenerate and test locally:

```sh
python -B -m unittest test_pack_index
python -B build_pack_index.py
```
