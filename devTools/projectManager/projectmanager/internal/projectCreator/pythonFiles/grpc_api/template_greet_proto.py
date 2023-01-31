content_st = """
syntax = "proto3";

package greet;

// The greeting service definition.
service Greeter {
    // Unary - request and respond
    rpc SayHello (HelloRequest) returns (HelloReply);
    rpc HealthCheck (Ping) returns (Pong);

    // Server Streaming
    rpc ParrotSaysHello (HelloRequest) returns (stream HelloReply);

    // Client Streaming
    rpc ChattyClientSaysHello (stream HelloRequest) returns (DelayedReply);

    // Both Streaming
    rpc InteractingHello (stream HelloRequest) returns (stream HelloReply);
}

// The request message containing the user's name.
message HelloRequest {
    string name = 1;
    string greeting = 2;
}

// The response message containing the greetings.
message HelloReply {
    string message = 1;
}

message DelayedReply {
    string message = 1;
    repeated HelloRequest request = 2;
}

message Ping {
    string message = 1;
}

message Pong {
    string message = 1;
}
"""
