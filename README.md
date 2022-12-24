# jmx-monitor
A small class that allow you to monitor a JVM using remote+http. The jboss-client.jar is not provided and you must have it.

# build
```make build```

# install
It will copy all files to /opt/jmx-monitor
```make install```

# run example
java -cp "/opt/jmx-monitor/jmx-monitor-1.0-SNAPSHOT.jar:/opt/jmx-monitor/lib/commons-cli-1.3.1.jar:/opt/jmx-monitor/lib/jboss-client.jar" br.com.sonda.App -o "java.lang:type=Runtime/Uptime;java.lang:type=Threading/CurrentThreadCpuTime,CurrentThreadUserTime;java.lang:type=Memory/HeapMemoryUsage.used,HeapMemoryUsage.committed,HeapMemoryUsage.max,NonHeapMemoryUsage.used,NonHeapMemoryUsage.committed,NonHeapMemoryUsage.max;java.lang:name=G1 Young Generation,type=GarbageCollector/CollectionTime" -h jboss_host -p jboss_port -u appuser -n apppass 2> /dev/null
