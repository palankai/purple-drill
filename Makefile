all:
	@
	@echo "Usage:"
	@echo "  make build-dev - Build dev images"
	@echo "  make purge-dev - remove dev images, containers, demo database"

build-dev:
	docker build -t purple-drill-store -f deploy/purple-drill-store/Dockerfile .
	docker run --name purple-drill-store purple-drill-store || true
	docker build -t purple-drill-demo -f deploy/purple-drill-demo/Dockerfile .

purge-dev:
	docker rm -f purple-drill-store || true
	docker rmi -f purple-drill-store || true
	docker rmi -f purple-drill-demo || true
	dropdb purple-drill-demo || true
