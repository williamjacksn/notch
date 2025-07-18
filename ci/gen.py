import json
import pathlib


THIS_FILE = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path().resolve())
)


def gen(content: dict, target: str):
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_dependabot(target: str):
    def update(ecosystem: str) -> dict:
        return {
            "package-ecosystem": ecosystem,
            "allow": [{"dependency-type": "all"}],
            "directory": "/",
            "schedule": {"interval": "daily"},
        }

    ecosystems = ["github-actions", "uv"]
    content = {
        "version": 2,
        "updates": [update(e) for e in ecosystems],
    }

    gen(content, target)


def gen_github_workflows(target: str):
    content = {
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}",
        },
        "name": "Publish the package to PyPI",
        "on": {"release": {"types": ["published"]}},
        "jobs": {
            "publish": {
                "name": "Publish the package to PyPI",
                "runs-on": "ubuntu-latest",
                "environment": {
                    "name": "pypi-release",
                    "url": "https://pypi.org/p/notch",
                },
                "permissions": {"id-token": "write"},
                "steps": [
                    {"name": "Check out the repository", "uses": "actions/checkout@v4"},
                    {"name": "Publish the package to PyPI", "run": "sh ci/publish.sh"},
                ],
            },
        },
    }

    gen(content, target)


def main():
    gen_dependabot(".github/dependabot.yaml")
    gen_github_workflows(".github/workflows/publish.yaml")


if __name__ == "__main__":
    main()
