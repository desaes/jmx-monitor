# jmx-monitor
A small and simple class that allows you to monitor/collect objects and attributes from a JVM using remote+http. This was developed with JBOSS in mind. The jboss-client.jar is not provided and you must provide it. This may work with other JAVA Application Servers that uses JMX remote+http.

# requirements
* jdk/openjdk
* make
* maven
* jboss-client.jar

# build
```make build```

# install
```make install```\
\
It will copy all files to /opt/jmx-monitor

# run example 
```
java -cp \
"\
/opt/jmx-monitor/jmx-monitor-1.0-SNAPSHOT.jar:\
/opt/jmx-monitor/lib/commons-cli-1.3.1.jar:\
/opt/jmx-monitor/lib/jboss-client.jar" \
br.com.sonda.App \
-o \
"\
java.lang:type=Runtime/Uptime;\
java.lang:type=Threading/CurrentThreadCpuTime,CurrentThreadUserTime;\
java.lang:type=Memory/HeapMemoryUsage.used,HeapMemoryUsage.committed,HeapMemoryUsage.max,\
NonHeapMemoryUsage.used,NonHeapMemoryUsage.committed,NonHeapMemoryUsage.max;\
java.lang:name=G1 Young Generation,type=GarbageCollector/CollectionTime\
" \
-h jboss_host -p jboss_port -u appuser -n apppass 2> /dev/null
```
\
Query format:
Object/Attribute01,Attribute02;Object/Attribute01,Attribute02
