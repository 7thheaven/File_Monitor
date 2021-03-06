#include <stdio.h>
 #include <unistd.h>
 #include <sys/inotify.h>
 #define MAX_BUF_SIZE 1024
 
 int main(){
     int fd, wd;
     int len, index;
     char buffer[1024];
     struct inotify_event *event;
     char *path="/tmp";
 
     fd = inotify_init();
     if(fd < 0){
         printf("Failed to initialize inotify.\n");
         return 1;
     }
     wd = inotify_add_watch(fd, path, IN_CLOSE_WRITE | IN_CREATE);
     if(wd < 0){
         printf("Can't add watch for %s", path);
         return 1;
     }
     while(len = read(fd, buffer, MAX_BUF_SIZE)){
         index = 0;
         while(index < len){
             event = (struct inotify_event *)(buffer+index);
             if(event->wd != wd)
                 continue;
             if(event -> mask & IN_CLOSE_WRITE)
                 printf("file %s is closed for write.\n", event -> name);
             index += sizeof(struct inotify_event)+event->len;
         }
     }
     return 0;
}
