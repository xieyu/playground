extern crate protoc_rust;

use std::env;
use std::fs::{self, File};
use std::io::Write;

use std::path::{Path, PathBuf};

use grpcio_compiler::codegen as grpc_gen;
use prost::Message;

use protoc_rust::Customize;
