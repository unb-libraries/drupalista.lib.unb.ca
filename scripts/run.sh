#!/usr/bin/env sh
for i in /scripts/pre-init.d/*sh
do
  if [ -e "${i}" ]; then
    echo "[i] pre-init.d - processing $i"
    . "${i}"
  fi
done

if [ "$SLACK_TOKEN" == "NULL" ]; then
  echo "The SLACK_TOKEN environment variable is not set!"
  exit 1
fi

echo "SLACK_TOKEN: $SLACK_TOKEN" >> /app/rtmbot.conf
rtmbot
