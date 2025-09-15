
AVARE_VERSION ?= 3.12.11

IMAGE_NAME_REPO ?= avare_repo
IMAGE_NAME_WEATHER ?= avare_weather

COMPOSE_ALPINE = docker compose run --rm alpine

dir_prefix = $(PWD)

.EXPORT_ALL_VARIABLES:

all: build_repo build_weather

build_repo:
	cd ${dir_prefix}/repo
	docker build \
		--tag "${IMAGE_NAME_REPO}:${AVARE_VERSION}" \
		--tag "${IMAGE_NAME_REPO}:latest" \
		-f ./repo/Dockerfile .

build_weather:

	docker build \
		--tag "${IMAGE_NAME_WEATHER}:${AVARE_VERSION}" \
		--tag "${IMAGE_NAME_WEATHER}:latest" \
		-f ${dir_prefix}/weather/Dockerfile .
