#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <Windows.h>
#include <direct.h>

class File {
private:
    std::string filePath;

public:
    File(const std::string& path) : filePath(path) {}

    void create() {
        std::ofstream file(filePath);
        if (file) {
            std::cout << "File created successfully.\n";
        } else {
            std::cout << "Failed to create file.\n";
        }
    }

    void remove() {
        if (std::remove(filePath.c_str()) == 0) {
            std::cout << "File deleted successfully.\n";
        } else {
            std::cout << "Failed to delete file.\n";
        }
    }

    void read() {
        std::ifstream file(filePath);
        if (file) {
            std::cout << "File content:\n";
            std::string line;
            while (std::getline(file, line)) {
                std::cout << line << "\n";
            }
        } else {
            std::cout << "Failed to open file for reading.\n";
        }
    }

    void write() {
        std::ofstream file(filePath, std::ios::app);
        if (file) {
            std::cout << "Enter file content. Enter 'exit' on a new line to finish.\n";
            std::string line;
            while (true) {
                std::getline(std::cin, line);
                if (std::cin.eof()) {
                    // End-of-file reached, exit the loop.
                    break;
                }
                if (line == "exit") {
                    // User entered 'exit', terminate input.
                    break;
                }
                file << line << "\n";
            }
            std::cout << "File written successfully.\n";
        } else {
            std::cout << "Failed to open file for writing.\n";
        }
    }

    void openInTextEditor() {
        ShellExecuteA(nullptr, "open", filePath.c_str(), nullptr, nullptr, SW_SHOWNORMAL);
    }
};

class FileSystem {
private:
    std::string currentDirectory;

public:
    FileSystem(const std::string& initialDirectory) : currentDirectory(initialDirectory) {}

    void createDirectory(const std::string& directoryPath) {
        if (_mkdir(directoryPath.c_str()) == 0) {
            std::cout << "Directory created successfully.\n";
        } else {
            std::cout << "Failed to create directory.\n";
        }
    }

    void removeDirectory(const std::string& directoryPath) {
        if (_rmdir(directoryPath.c_str()) == 0) {
            std::cout << "Directory deleted successfully.\n";
        } else {
            std::cout << "Failed to delete directory.\n";
        }
    }

    void listDirectoryContents(const std::string& directoryPath) {
        std::cout << "Directory contents:\n";

        WIN32_FIND_DATAA findData;
        HANDLE hFind = FindFirstFileA((directoryPath + "\\*").c_str(), &findData);
        if (hFind != INVALID_HANDLE_VALUE) {
            do {
                std::string file_name = findData.cFileName;
                if (file_name != "." && file_name != "..") {
                    std::cout << file_name << "\n";
                }
            } while (FindNextFileA(hFind, &findData) != 0);
            FindClose(hFind);
        } else {
            std::cout << "Failed to open directory.\n";
        }
    }

    void changeDirectory(const std::string& directoryPath) {
        if (SetCurrentDirectoryA(directoryPath.c_str())) {
            char cwd[MAX_PATH];
            if (GetCurrentDirectoryA(MAX_PATH, cwd) != 0) {
                currentDirectory = cwd;
                std::cout << "Changed directory to: " << currentDirectory << "\n";
            } else {
                std::cout << "Failed to get current directory.\n";
            }
        } else {
            std::cout << "Directory not found.\n";
        }
    }

    std::string getCurrentDirectory() const {
        return currentDirectory;
    }

    std::vector<std::string> findFiles(const std::string& directory, const std::string& fileName) {
        std::vector<std::string> foundFiles;
        findFilesRecursive(directory, fileName, foundFiles);
        return foundFiles;
    }

private:
    void findFilesRecursive(const std::string& directory, const std::string& fileName, std::vector<std::string>& foundFiles) {
        WIN32_FIND_DATAA findData;
		
        HANDLE hFind = FindFirstFileA((directory + "\\*").c_str(), &findData);
        if (hFind != INVALID_HANDLE_VALUE) {
            do {
                if (findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
                    std::string subdirectory = findData.cFileName;
                    if (subdirectory != "." && subdirectory != "..") {
                        std::string subdirectoryPath = directory + "\\" + subdirectory;
                        findFilesRecursive(subdirectoryPath, fileName, foundFiles);
                    }
                } else {
                    std::string file = findData.cFileName;
                    if (file == fileName) {
                        std::string filePath = directory + "\\" + file;
                        foundFiles.push_back(filePath);
                    }
                }
            } while (FindNextFileA(hFind, &findData) != 0);
            FindClose(hFind);
        }
    }
};

int main() {
    std::string initialDirectory;
    std::cout << "Enter the initial directory: ";
    std::getline(std::cin, initialDirectory);

    FileSystem fileSystem(initialDirectory);

    while (true) {
        std::cout << "\nMenu:\n";
        std::cout << "1. Create a directory\n";
        std::cout << "2. Delete a directory\n";
        std::cout << "3. List directory contents\n";
        std::cout << "4. Change directory\n";
        std::cout << "5. Create a file\n";
        std::cout << "6. Delete a file\n";
        std::cout << "7. Read a file\n";
        std::cout << "8. Write to a file\n";
        std::cout << "9. Open a file in a text editor\n";
        std::cout << "10. Search for a file\n";
        std::cout << "11. Current directory\n";
        std::cout << "12. Exit\n";
        std::cout << "Enter your choice: ";

        std::string choiceStr;
        std::getline(std::cin, choiceStr);

        try {
            int choice = std::stoi(choiceStr);

            switch (choice) {
                case 1: {
                    std::cout << "Enter the directory path: ";
                    std::string directoryPath;
                    std::getline(std::cin, directoryPath);
                    fileSystem.createDirectory(directoryPath);
                    break;
                }
                case 2: {
                    std::cout << "Enter the directory path: ";
                    std::string directoryPath;
                    std::getline(std::cin, directoryPath);
                    fileSystem.removeDirectory(directoryPath);
                    break;
                }
                case 3: {
                    std::cout << "Enter the directory path: ";
                    std::string directoryPath;
                    std::getline(std::cin, directoryPath);
                    fileSystem.listDirectoryContents(directoryPath);
                    break;
                }
                case 4: {
                    std::cout << "Enter the directory path: ";
                    std::string directoryPath;
                    std::getline(std::cin, directoryPath);
                    fileSystem.changeDirectory(directoryPath);
                    break;
                }
                case 5: {
                    std::cout << "Enter the file path: ";
                    std::string filePath;
                    std::getline(std::cin, filePath);
                    File file(filePath);
                    file.create();
                    break;
                }
                case 6: {
                    std::cout << "Enter the file path: ";
                    std::string filePath;
                    std::getline(std::cin, filePath);
                    File file(filePath);
                    file.remove();
                    break;
                }
                case 7: {
                    std::cout << "Enter the file path: ";
                    std::string filePath;
                    std::getline(std::cin, filePath);
                    File file(filePath);
                    file.read();
                    break;
                }
                case 8: {
                    std::cout << "Enter the file path: ";
                    std::string filePath;
                    std::getline(std::cin, filePath);
                    File file(filePath);
                    file.write();
                    break;
                }
                case 9: {
                    std::cout << "Enter the file path: ";
                    std::string filePath;
                    std::getline(std::cin, filePath);
                    File file(filePath);
                    file.openInTextEditor();
                    break;
                }
                case 10: {
                    std::cout << "Enter the file name: ";
                    std::string fileName;
                    std::getline(std::cin, fileName);
                    std::vector<std::string> foundFiles = fileSystem.findFiles("C:\\Users\\DELL\\OneDrive\\Documents", fileName);
                    if (foundFiles.empty()) {
                        std::cout << "File not found.\n";
                    } else {
                        std::cout << "Found files:\n";
                        for (const std::string& filePath : foundFiles) {
                            std::cout << filePath << "\n";
                        }
                    }
                    break;
                }
                case 11:
                    std::cout << "Current directory: " << fileSystem.getCurrentDirectory() << "\n";
                    break;
                case 12:
                    return 0;
                default:
                    std::cout << "Invalid choice. Please try again.\n";
            }
        } catch (const std::invalid_argument& e) {
            std::cout << "Invalid choice. Please try again.\n";
        }
    }
}