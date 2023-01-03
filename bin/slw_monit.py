#!/opt/jmx-monitor/.venv/bin/python3
import os
import untangle
import argparse
import subprocess
import requests

def print_jvm_stats(cmd, host, port):
    try:
        response = requests.get(f"http://{host}:{port}")
    except Exception as e:
        print(f"Error: unable to connect to {host} on port {port}, {e}")
    else:
        if response.status_code == 200:
            response_errors = ["WAITING", "refused", "jmx"]
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as proc:
                for line in proc.stdout.read().decode().split('\n'):
                    if line != "":
                        values = line.split(' ')
                        if values[-1] in response_errors:
                            print("Error: unable to retrieve a valid response from JVM")
                            exit(1)
                        print(f"Statistic.{values[-2].replace('.','_')} {values[-1]}")
                        print(f"Message.{values[-2].replace('.','_')} {values[-2].replace(':','')}")
        else:
            print(f"Error: unable to connect to ${host} on port ${port}, status code {response.status_code}")

def main():

    parser = argparse.ArgumentParser(
                    prog = 'monit.py',
                    )
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host', action='store')
    parser.add_argument('--server', action='store')
    parser.add_argument('--port', action='store')
    parser.add_argument('--username', action='store')
    parser.add_argument('--password', action='store')
    parser.add_argument('--batch', action='store')
    args = parser.parse_args()

    class_path = os.environ.get("CLASS_PATH")
    if class_path is None:
        print("Error: CLASS_PATH environment variable must be defined.")
        exit(1)

    jboss_config_path = os.environ.get("JBOSS_CONFIG_PATH")
    if jboss_config_path is None:
        print("Error: JBOSS_CONFIG_PATH environment variable must be defined.")
        exit(1)

    jboss_initial_offset = os.environ.get("JBOSS_INITIAL_OFFSET")
    if jboss_initial_offset is None:
        print("Error: JBOSS_INITIAL_OFFSET environment variable must be defined.")
        exit(1)

    jboss_config_files = [
        "host-master.xml",
        "host-slave.xml"
    ]

    jboss_metrics = {
        '01': ("java.lang:type=ClassLoading/LoadedClassCount,TotalLoadedClassCount,UnloadedClassCount;"
            "java.lang:type=Memory/ObjectPendingFinalizationCount;"
            "java.lang:type=Memory/HeapMemoryUsage.init,HeapMemoryUsage.used,HeapMemoryUsage.committed,HeapMemoryUsage.max"),
        '02': ("java.lang:type=Memory/NonHeapMemoryUsage.init,NonHeapMemoryUsage.used,NonHeapMemoryUsage.committed,NonHeapMemoryUsage.max;"
            "java.lang:type=Threading/TotalStartedThreadCount,ThreadCount,CurrentThreadCpuTime,CurrentThreadUserTime;"
            "java.lang:type=Runtime/Uptime;"
            "java.lang:type=Compilation/TotalCompilationTime")}
    

    server_port_map = {}
    for jboss_config_file in jboss_config_files:
        path = os.path.join(jboss_config_path, jboss_config_file)
        if os.path.isfile(path):
            try:
                config = untangle.parse(os.path.join(path))
                if hasattr(config.host, 'servers'):
                    for server in config.host.servers.server:
                        if hasattr(server, 'jvm'):
                            server_port_map[server['name']] = int(jboss_initial_offset) + int(server.socket_bindings['port-offset'])
                            if args.list == True:
                                print(f"server: {server['name']:<70}",
                                    f"port: {int(jboss_initial_offset) + int(server.socket_bindings['port-offset'])}"
                                    )
                    
            except Exception as e:
                print(e)
        else:
            print("Error: invalid path")
            exit(1)

    if (args.host is not None and
        args.username is not None and 
        args.password is not None and 
        args.batch is not None and
        args.list is not True):

        cmd = [
               "java",
               '-cp',
               f'{class_path}',
               "br.com.sonda.App",
               '-o',
               f'"{jboss_metrics[args.batch]}"',
               '-h',
               f'{args.host}',
               '-u',
               f'{args.username}',
               '-n',
               f'{args.password}',
               '-p'
        ]

        if args.server is not None:
            cmd.append(f"{server_port_map[args.server]}")
            port = server_port_map[args.server]
        elif args.port is not None:
            cmd.append(args.port)
            port = args.port

        print_jvm_stats(cmd, args.host, port)

if __name__ == "__main__":
    main()
