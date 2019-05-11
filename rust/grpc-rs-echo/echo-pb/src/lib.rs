#[allow(dead_code)]
pub mod echo {
    include!(concat!(env!("OUT_DIR"), "/echo.rs"));
    include!(concat!(env!("OUT_DIR"), "/wrapper_echo.rs"));
}
