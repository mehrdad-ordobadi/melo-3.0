curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/mehrdad-ordobadi//actions/workflows/WORKFLOW_ID/dispatches \
  -d '{"ref":"testing","inputs":{}'