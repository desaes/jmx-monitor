TS := $(shell date +'%Y%m%d%H%M%S')
build:
        mvn package
        mvn dependency:copy-dependencies

install:
        @mkdir -p /opt/jmx-remote/lib
        @if [ -e target/jmx-monitor-1.0-SNAPSHOT.jar ];then \
                cp -f /opt/jmx-monitor/jmx-monitor-1.0-SNAPSHOT.jar /opt/jmx-monitor/$(TS).jmx-monitor-1.0-SNAPSHOT.jar.bkp; \
        fi
        @cp -f target/jmx-monitor-1.0-SNAPSHOT.jar /opt/jmx-monitor
        @cp -f target/dependency/commons-cli-1.3.1.jar /opt/jmx-monitor/lib
        @echo Check out /opt/jmx-monitor
