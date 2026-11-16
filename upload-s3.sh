#!/usr/bin/env bash
# Upload the roadmap site to s3://mynests.io/ai/v2/
# Leaves the existing http://mynests.io/ai/ files untouched.
#
# Usage, from this folder:
#   ./upload-s3.sh
#
# Credentials: the AWS CLI default profile, or a .env file next to this
# script (that file is gitignored):
#   AWS_ACCESS_KEY_ID=your-key
#   AWS_SECRET_ACCESS_KEY=your-secret
#   AWS_DEFAULT_REGION=us-east-1

set -euo pipefail

BUCKET="mynests.io"
PREFIX="ai/v2"
REGION="us-east-1"

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "AWS CLI is not installed." >&2
  exit 1
fi

echo "Checking AWS credentials..."
if ! aws sts get-caller-identity --region "$REGION" >/dev/null; then
  echo "AWS credentials were rejected." >&2
  echo "Put AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in $ROOT/.env and run this again." >&2
  exit 1
fi

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
cp index.html style.css app.js favicon.svg "$STAGE/"
cp telugu-*.html "$STAGE/"

echo "Uploading site files to s3://${BUCKET}/${PREFIX}/"
(
  cd "$STAGE"
  aws s3 sync . "s3://${BUCKET}/${PREFIX}/" \
    --region "$REGION" \
    --cache-control "no-cache"
)

echo
echo "Uploaded. Existing s3://${BUCKET}/ai/ was not changed."
echo "Roadmap:  http://${BUCKET}/${PREFIX}/"
echo "Telugu:   http://${BUCKET}/${PREFIX}/telugu-index.html"
