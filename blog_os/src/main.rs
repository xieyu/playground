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
    blog_os::hlt_loop();
}

// 程序的入口_start
// no_mangle, 函数名以C的格式导出
#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn _start() -> !{
    use blog_os::interrupts::PICS;
    println!("hello, world");
    serial_println!("hello Host{}", "!");
    blog_os::gdt::init();
    blog_os::interrupts::init_idt();
    unsafe {PICS.lock().initialize();}
    x86_64::instructions::interrupts::enable();

    use x86_64::registers::control::Cr3;
    let (level_4_page_table, _) = Cr3::read();
    println!("Level 4 page table at :{:?}", level_4_page_table.start_address());


    let level_4_page_table_pointer = 0xffff_ffff_ffff_f000 as *const u64;
    for i in 0..10 {
        let entry = unsafe{*level_4_page_table_pointer.offset(i)};
        println!("Entry {}: {:#x}", i, entry);
    }

    use x86_64::structures::paging::PageTable;
    let level_4_page_table_ptr = 0xffff_ffff_ffff_f000 as *const PageTable;
    let level_4_table = unsafe {&*level_4_page_table_ptr};
    for i in 0..10 {
        println!("Entry {}: {:?}", i, level_4_table[i]);
    }

    println!("It's not crash");
    let ptr = 0xdeadbeef as *mut u32;
    unsafe{let x = *ptr;}
    unsafe{*ptr=42;}
    println!("It did not crash");
    blog_os::hlt_loop();
}

