# Forcing a no-cache Docker build (Render troubleshooting)

If Render's build logs show a missing remote build cache (errors mentioning `buildcache: not found`), you can force a fresh build locally and/or clear Render's cache:

- Clear the build cache in the Render dashboard: Service → Deploys → More → Clear build cache, then Redeploy.

- Build locally without cache (helper script included):

```bash
./scripts/render_no_cache_build.sh ai-app-compiler:local
```

- To reproduce Render's build environment locally, run the script and then push the resulting image to the registry Render uses (if you manage the registry credentials).

Notes:
- `render.yaml` is included as a service manifest example; use Render dashboard or Infrastructure-as-Code tooling to configure your service if you rely on `render.yaml`.
- If Render continues trying to import a missing cache, clearing the cache in the dashboard is the fastest fix.
