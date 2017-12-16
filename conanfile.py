#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class PixmanConan(ConanFile):
    name = "pixman"
    version = "0.34.0"
    url = "https://github.com/bincrafters/conan-pixman"
    description = "Pixman is a low-level software library for pixel manipulation, providing features such as image compositing and trapezoid rasterization."
    license = "GNU Lesser General Public License (LGPL) version 2.1 or the Mozilla Public License (MPL) version 1.1"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    #use static org/channel for libs in conan-center
    #use dynamic org/channel for libs in bincrafters
    #requires = "OpenSSL/1.0.2l@conan/stable", \
    #    "zlib/1.2.11@conan/stable", \
    #    "websocketpp/0.7.0@%s/%s" % (self.user, self.channel)

    def source(self):
        source_url = "https://www.cairographics.org/releases/"
        tools.get("{0}-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")
        #Rename to "sources" is a convention to simplify later steps

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False # example
        cmake.configure(source_dir="sources")
        cmake.build()

    def package(self):
        with tools.chdir("sources"):
            self.copy(pattern="LICENSE")
            self.copy(pattern="*", dst="include", src="include")
            self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
            self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
