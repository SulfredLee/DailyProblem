content_st = """
syntax = "proto3";

package {{ project_name }};

// The {{ project_name }} service definition.
service {{ project_name_capitalize }} {
    // Unary - request and respond
    rpc HealthCheck (Ping) returns (Pong);
}

message Ping {
    string message = 1;
}

message Pong {
    string message = 1;
}
"""
