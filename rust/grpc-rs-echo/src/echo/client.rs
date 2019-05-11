use grpcio::{ChannelBuilder, EnvBuilder};
use echopb::echo::{EchoReq, EchoServiceClient};
use std::sync::Arc;

fn main() {
    let env = Arc::new(EnvBuilder::new().build());
    let ch = ChannelBuilder::new(env).connect("localhost:50051");
    let client = EchoServiceClient::new(ch);
    let mut req = EchoReq::new_();
    req.set_msg("hello".to_owned());
    let resp = client.echo(&req).export("rpc");
    println!("echo service receive: {}", resp.get_msg());
}

