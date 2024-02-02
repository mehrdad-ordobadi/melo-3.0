curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer " \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/mehrdad-ordobadi/melo-3.0/actions/workflows/testing.yml/dispatches \
  -d '{"ref":"testing","inputs":{}'