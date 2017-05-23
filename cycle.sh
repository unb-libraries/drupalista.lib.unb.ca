#!/usr/bin/env bash
docker-compose kill; docker-compose rm -f -v --all; docker-compose up -d --build; docker-compose logs -f
