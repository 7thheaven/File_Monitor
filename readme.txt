1090310620 Little7 's Note

于excalibur note.txt中记录了所需知识备忘录。

思路：

A.修改内核相关系统调用，编译更新内核。


问题：编译更新内核，速度太慢，经常出错（甚至系统崩溃），调试困难。


B.直接利用/proc系统获取所需信息。

问题：可以得知进程打开了哪些文件，但无法实时获得进程对文件的读写操作。


C.调用inotify模块监视文件。

问题：可以实时知道文件的状态，但是不能得知具体是哪个进程对文件进行了相应操作。