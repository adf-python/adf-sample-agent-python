/*
 * This source file was generated by the Gradle 'init' task
 */
package org.example;

import adf_core_python.gateway.Gateway;

public class App {
    public static void main(String[] args) {
        Gateway gateway = new Gateway(27941);
        gateway.start();
    }
}
