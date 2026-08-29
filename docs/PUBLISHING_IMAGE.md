# Publishing the Backend Docker Image

This project uses GitHub Actions to automatically build and publish the
backend Docker image to GitHub Container Registry (GHCR).

## When the Image Is Published

The workflow is triggered in two ways:

- **Automatically when a GitHub Release is published.**
- **Manually using `workflow_dispatch`** from the GitHub Actions page.

Publishing a release is the easiest way to run app image
because the workflow generates both a `latest` tag and a tag based on
the release version.

## Publishing a New Version

1. Make sure all changes intended for the release are committed and
   pushed to the repository.
2. Create a new Git tag for the version, for example:

``` bash
git tag v1.0.0
git push origin v1.0.0
```

3. Open the repository on GitHub and create a new Release based on that
   tag.
4. Publish the Release.
5. GitHub Actions will automatically start the **Build and publish BE
   image** workflow.
6. The workflow builds the Docker image using the repository root as
   the Docker build context and pushes it to GHCR.

## Published Image

The registry and image name are configured in the workflow:

``` yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: kinggred/app
```

Therefore, the resulting image is published as:

``` text
ghcr.io/kinggred/app
```

The workflow authenticates to GHCR using the automatically provided
`GITHUB_TOKEN`. The job requires the following permissions:

``` yaml
permissions:
  contents: read
  packages: write
```

No separate GHCR password or Personal Access Token is required for this
workflow.

## Image Tags

The workflow uses `docker/metadata-action` to generate image tags:

``` yaml
tags: |
  type=raw,value=latest
  type=ref,event=tag
  type=sha,prefix=sha-
```

For a release created from tag `v1.0.0`, the published image can include
tags such as:

``` text
ghcr.io/kinggred/app:latest
ghcr.io/kinggred/app:v1.0.0
ghcr.io/kinggred/app:sha-<commit-sha>
```

This provides three useful ways to reference an image:

- `latest` --- the most recently published image.
- `v1.0.0` --- a specific released version.
- `sha-<commit-sha>` --- an image tied to a specific Git commit.

For deployments, using a version tag such as `v1.0.0` is recommended
when reproducibility is important. `latest` is convenient when the
deployment should always use the newest published release.

## Manual Build

The workflow can also be started manually without publishing a release:

1. Open the repository on GitHub.
2. Go to **Actions**.
3. Select **Build and publish BE image**.
4. Click **Run workflow**.

Because a manually triggered workflow is not associated with a Git tag
event, the `type=ref,event=tag` tag will not be generated. The `latest`
and commit SHA tags can still be generated.

## Build Process

The workflow performs the following operations:

``` text
Checkout repository
        ↓
Authenticate with GHCR
        ↓
Generate image metadata and tags
        ↓
Build Docker image
        ↓
Push image to GHCR
```

The actual image build and push is handled by
`docker/build-push-action`:

``` yaml
- name: Build and push image
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
```

The workflow therefore expects a valid `Dockerfile` to be available in
the repository build context.

## Changing the Image Name

Before using this workflow in project, update:

``` yaml
IMAGE_NAME: kinggred/app
```

For example:

``` yaml
IMAGE_NAME: kinggred/meal-list-api
```

The resulting image would then be available under:

``` text
ghcr.io/kinggred/meal-list-api:<tag>
```
