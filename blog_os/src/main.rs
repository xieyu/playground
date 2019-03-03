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
    println!("{}", info);
    loop{}
}

// 程序的入口_start
// no_mangle, 函数名以C的格式导出
#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn _start() -> !{
    println!("hello, world");
    serial_println!("hello Host{}", "!");
    blog_os::interrupts::init_idt();
    x86_64::instructions::int3();
    println!("It's not crash");
    unsafe { exit_qemu();}
    //write!(vga_buffer::WRITER.lock(), "hello").unwrap();
    loop{}
}

