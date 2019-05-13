use grpcio::{Environment, RpcContext, ServerBuilder, UnarySink};
use pb::echo::{EchoReq, EchoResp};
use pb::echo_grpc::{self, EchoService};

use futures::sync::oneshot;
use futures::Future;
use std::io::Read;
use std::sync::Arc;
use std::{io, thread};

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

fn main() {
    let echo_service = echo_grpc::create_echo_service(ImplEchoService {});
    let env = Arc::new(Environment::new(1));
    let mut builder = ServerBuilder::new(env);
    builder = builder.register_service(echo_service);

    let mut server = builder.bind("127.0.0.1", 50051).build().unwrap();
    server.start();

    for &(ref host, port) in server.bind_addrs() {
        println!("listen on {}:{}", host, port);
    }
    let (tx, rx) = oneshot::channel();
    thread::spawn(move || {
        println!("press enter to exit");
        io::stdin().read(&mut [0]).unwrap();
        tx.send(())
    });

    let _ = rx.wait();
    let _ = server.shutdown().wait();
}
