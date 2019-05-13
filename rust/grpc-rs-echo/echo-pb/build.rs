extern crate protoc_grpcio;

fn main() {
    let proto_dir = "proto";
    let out_dir = "src/";
    println!("cargo:return-if-changed={}", proto_dir);
    protoc_grpcio::compile_grpc_protos(&["echo/echo.proto"], &[proto_dir], &out_dir, None)
        .expect("fail to compile grpc definations");
}
