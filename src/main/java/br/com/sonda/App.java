package br.com.sonda;

import org.apache.commons.cli.*;
import javax.management.MBeanServerConnection;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;
import javax.management.openmbean.CompositeData;
import javax.management.ObjectName;
import java.util.*;


public class App
{
    public static void main( String[] args )
    {
        Options options = new Options();

        Option host = new Option("h", "host", true, "jmx host");
        host.setRequired(true);
        options.addOption(host);

        Option port = new Option("p", "port", true, "jmx port");
        port.setRequired(true);
        options.addOption(port);

        Option object = new Option("o", "object", true, "jmx object");
        object.setRequired(true);
        options.addOption(object);

        /*
        Option object = new Option("o", "object", true, "jmx object");
        object.setRequired(false);
        options.addOption(object);

        Option attribute = new Option("a", "attribute", true, "jmx attribute");
        attribute.setRequired(false);
        options.addOption(attribute);
        */

        Option username = new Option("u", "username", true, "username");
        username.setRequired(true);
        options.addOption(username);

        Option password = new Option("n", "password", true, "password");
        password.setRequired(true);
        options.addOption(password);

        CommandLineParser parser = new PosixParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd = null;//not a good practice, it serves it purpose

        try {
            cmd = parser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("utility-name", options);
            System.exit(1);
        }

        String hostParam = cmd.getOptionValue("host");
        String portParam = cmd.getOptionValue("port");
        String objtParam = cmd.getOptionValue("object");
        //String attrParam = cmd.getOptionValue("attribute");
        String userParam = cmd.getOptionValue("username");
        String passParam = cmd.getOptionValue("password");

        try {
            HashMap env = new HashMap();
            String[] credentials = new String[] { userParam , passParam };
            env.put("jmx.remote.credentials", credentials);
            String urlString = System.getProperty("jmx.service.url","service:jmx:remote+http://" + hostParam + ":" + portParam);
            JMXServiceURL serviceURL = new JMXServiceURL(urlString);
            JMXConnector jmxConnector = JMXConnectorFactory.connect(serviceURL, env);
            MBeanServerConnection connection = jmxConnector.getMBeanServerConnection();
            String[] querys;
            querys = objtParam.split(";");
            for (String query : querys) {
                String[] params;
                params = query.split("/");
                String[] attrList;
                if (params[1].indexOf(",") > 0) {
                    attrList = params[1].split(",");
                    for (String attr : attrList) {
                        if (attr.indexOf(".") > 0) {
                            String[] attrs = attr.split("\\.");
                            Object o = jmxConnector.getMBeanServerConnection().getAttribute(new ObjectName(params[0]), attrs[0]);
                            CompositeData cd = (CompositeData) o;
                            System.out.println(params[0] + ": " + attrs[0] + "." + attrs[1] + ": " + cd.get(attrs[1]));
                        } else {
                            Object o = jmxConnector.getMBeanServerConnection().getAttribute(new ObjectName(params[0]), attr);
                            System.out.println(params[0] + ": " + attr + ": " + o);
                        }
                    }
                } else {
                    if (params[1].indexOf(".") > 0) {
                        String[] attrs = params[1].split("\\.");
                        Object o = jmxConnector.getMBeanServerConnection().getAttribute(new ObjectName(params[0]), attrs[0]);
                        CompositeData cd = (CompositeData) o;
                        System.out.println(params[0] + ": " + attrs[0] + "." + attrs[1] + ": " + cd.get(attrs[1]));
                    } else {
                        Object o = jmxConnector.getMBeanServerConnection().getAttribute(new ObjectName(params[0]), params[1]);
                        System.out.println(params[0] + ": " + params[1] + ": " + o);
                    }
                }
            }
            jmxConnector.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
            System.exit(1);
        }
    }
}
