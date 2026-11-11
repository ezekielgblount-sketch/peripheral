#!/bin/bash
# Packages the standalone Mac (Apple Silicon) app into Builds/. Usage: Scripts/package_mac.sh
P="$(cd "$(dirname "$0")/.." && pwd)"
"/Users/Shared/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun -project="$P/Peripheral_POC.uproject" \
  -noP4 -utf8output -platform=Mac -architecture=arm64 -clientconfig=Development -installed \
  -build -cook -allmaps -stage -pak -package -archive -archivedirectory="$P/Builds" > "$P/Saved/Logs/package_mac.log" 2>&1
echo "exit $?" >> "$P/Saved/Logs/package_mac.log"
