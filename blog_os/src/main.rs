#![no_std]
#![no_main]

mod vga_buffer;
use core::panic::PanicInfo;

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    println!("{}", info);
    loop{}
}

// 程序的入口_start
// no_mangle, 函数名以C的格式导出
#[no_mangle]
pub extern "C" fn _start() -> !{
    println!("hello, world");
    panic!("some panic message");
    //write!(vga_buffer::WRITER.lock(), "hello").unwrap();
    loop{}
}
