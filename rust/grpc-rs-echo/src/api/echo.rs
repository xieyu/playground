use grpcio::{Environment, RpcContext, ServerBuilder, UnarySink};
use pb::echo::{EchoReq, EchoResp};
use pb::echo_grpc::{self, EchoService};

use futures::Future;
use std::sync::Arc;

#[derive(Clone)]
struct ImplEchoService {}

impl EchoService for ImplEchoService {
    fn echo(&mut self, ctx: RpcContext<'_>, req: EchoReq, sink: UnarySink<EchoResp>) {
        println!("get req {:?}", req);
        let msg = format!("hello {}", req.get_msg());
        let mut resp = EchoResp::new();
        resp.set_msg(msg);
        let f = sink
            .success(resp)
            .map_err(move |e| println!("fail to repl {:?}: {:?}", req, e));
        ctx.spawn(f)
    }
}

pub fn register_service(mut& builder: ServerBuilder) {
    let echo_service = echo_grpc::create_echo_service(ImplEchoService {});
    builder.register_service(echo_service)
}
