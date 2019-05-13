use grpcio::{ChannelBuilder, EnvBuilder};
use pb::echo::EchoReq;
use pb::echo_grpc::EchoServiceClient;
use std::sync::Arc;

fn main() {
    let env = Arc::new(EnvBuilder::new().build());
    let ch = ChannelBuilder::new(env).connect("localhost:50051");
    let client = EchoServiceClient::new(ch);
    let mut req = EchoReq::new();
    req.set_msg("hello".to_owned());
    let resp = client.echo(&req).expect("rpc");
    println!("echo service receive: {}", resp.get_msg());
}
