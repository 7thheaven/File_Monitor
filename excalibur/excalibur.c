#include <linux/module.h>
#include <linux/init.h>
#include <linux/fcntl.h>
#include <linux/syscalls.h>

int __init excalibur_init (void)
{
	int talk;
	printk("HelloWorld\n");
//	talk=sys_open("talk.txt",O_CREAT|O_TRUNC|O_RDWR,0666);
	return 0;
}

void __exit excalibur_exit(void)
{
    printk("GoodBye\n");
}

MODULE_AUTHOR("little7");
MODULE_DESCRIPTION("text");
MODULE_LICENSE("GPL");

module_init(excalibur_init);
module_exit(excalibur_exit);
