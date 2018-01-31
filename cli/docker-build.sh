#!/bin/bash
TAG=${TAG:-"netsil/cli"}
docker build -t ${TAG} .
