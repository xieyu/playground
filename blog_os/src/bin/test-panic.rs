#![cfg_attr(not(test), no_std)]
#![cfg_attr(not(test), no_main)]
#![cfg_attr(test, allow(unused_imports))]

use blog_os::println;
use blog_os::serial_println;
use blog_os::exit_qemu;
use core::panic::PanicInfo;

#[cfg(not(test))]
#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    serial_println!("ok");
    unsafe { exit_qemu();}
    loop{}
}

#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn _start() -> !{
    panic!();
    unsafe { exit_qemu();}
    loop{}
}

