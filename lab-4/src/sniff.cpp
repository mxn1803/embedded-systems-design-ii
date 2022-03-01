#include <cstdio>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>

std::string exec(const char* cmd) {
    std::array<char, 128> buffer;
    std::string result;
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd, "r"), pclose);
    if (!pipe) {
        throw std::runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

std::string sniff(const std::string addr) {
    std::string cmd = "/fusion2/rwmem.elf " + addr;
    std::string output = exec(cmd.c_str());
    std::string value = output.substr(21);
    return value;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::cout << sniff(argv[1]);
    return 0;
}