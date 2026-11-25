#!/bin/zsh
# Builds the standalone AI Brain Installer download from the Founder OS copy of the skill.
# One home: edit .claude/skills/build-your-ai-brain here, then run this to make the zip
# for the free lead magnet / paid download. Output: dist/build-your-ai-brain.zip
set -e
cd "${0:A:h}/.."
mkdir -p dist
rm -f dist/build-your-ai-brain.zip
cd .claude/skills
zip -qr ../../dist/build-your-ai-brain.zip build-your-ai-brain -x '*.DS_Store'
cd ../..
echo "Built dist/build-your-ai-brain.zip ($(du -h dist/build-your-ai-brain.zip | cut -f1))"
