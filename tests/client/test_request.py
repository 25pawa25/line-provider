from clients.grpc.proto.line_provider import line_provider_pb2

events_request = line_provider_pb2.GetEventsRequest()
check_event_request = line_provider_pb2.CheckIfEventExistsRequest(event_id="78b88230-93ca-4a49-b318-ed7bccd9bf57")