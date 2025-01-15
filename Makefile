# Wake up docker containers
up:
	docker-compose -f docker-compose.yml up -d

# Shut down docker containers
down:
	docker-compose -f docker-compose.yml down

create-network:
	docker network create storage_default || echo "Network already exists"

# Start tests in container
test-events:
	docker-compose -f docker-compose.yml exec -e DEBUG=True line_provider sh -c "cd .. && pytest -vv -s tests/test_GRPCAsyncServerEvents.py"

test-existing-event:
	docker-compose -f docker-compose.yml exec -e DEBUG=True line_provider sh -c "cd .. && pytest -vv -s tests/test_GRPCAsyncServerCheckEvent.py"


# Show logs of each container
logs:
	docker-compose -f docker-compose.yml logs

# Restart all containers
restart: down up

# Build and up docker containers
build:
	docker-compose -f docker-compose.yml build --force-rm

# Build and up docker containers
rebuild:  build up

check-linters:
	docker-compose run --rm lint

proto-line-provider:
	python3 -m grpc_tools.protoc -I=protobuf/ --python_out=src/clients/grpc/proto/line_provider --grpc_python_out=src/clients/grpc/proto/line_provider protobuf/line_provider.proto
	cd src/clients/grpc/proto/line_provider && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py

proto-bet:
	python3 -m grpc_tools.protoc -I=protobuf/ --python_out=src/clients/grpc/proto/bet --grpc_python_out=src/clients/grpc/proto/bet protobuf/bet.proto
	cd src/clients/grpc/proto/bet && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py
