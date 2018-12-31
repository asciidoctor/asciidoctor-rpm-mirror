#!/bin/bash

ORIGIN_URL=https://src.fedoraproject.org/rpms/rubygem-asciidoctor.git
MIRROR_URL=https://github.com/asciidoctor/asciidoctor-rpm-mirror

set -e
# NOTE use --bare instead of --mirror since --mirror brings in pull request branches
git clone --bare $ORIGIN_URL
cd ${ORIGIN_URL##*/}
# NOTE prevent mirror branch from being removed
git remote add -t mirror -f github $MIRROR_URL
git branch mirror github/mirror
git remote remove github
git config credential.helper cache
git ls-remote -h https://$GITHUB_TOKEN:x-oauth-basic@${MIRROR_URL#https://} > /dev/null
git push --mirror $MIRROR_URL
git credential-cache exit
cd -
rm -rf ${ORIGIN_URL##*/}
