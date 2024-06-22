#include <iostream>
#include <stdio.h>
#include <winsock.h>
#include <windows.h>
#include <string.h>
#include <string>
#include <io.h>
#include <sstream>

using std::cout;
using std::endl;
using std::string;
using std::stringstream;

bool registeredDisk[26];

void DfsListFolderFiles(string path) {
	_finddata_t file_info;
	string current_path = path + "\\*.*";
	int handle = _findfirst(current_path.c_str(), &file_info);
	//返回值为-1则查找失败
	if (-1 == handle) {
		cout << "cannot match the path" << endl;
		return;
	}
	
	do {
		//目录
		if (file_info.attrib == _A_SUBDIR) {
			//.是当前目录，..是上层目录，须排除掉这两种情况
			if (strcmp(file_info.name, "..") != 0 && strcmp(file_info.name, ".") != 0)
				DfsListFolderFiles(path + "\\" + file_info.name);
		} else {
			cout << path + "\\" + file_info.name << endl;
		}
	} while (!_findnext(handle, &file_info));
	//关闭文件句柄
	_findclose(handle);
}


int main() {
	for (wchar_t driveLetter = 'A'; driveLetter <= 'Z'; driveLetter++) {
		wchar_t letterTemp[3] = {driveLetter, ':', '\0'};
		UINT driveType = GetDriveTypeW(letterTemp);
		switch (driveType) {
		case DRIVE_NO_ROOT_DIR:
			break;
		default:
			registeredDisk[driveLetter - 'A'] = 1;
			break;
		}
	}
	for (char i = 'A'; i <= 'Z'; i++) {
		cout << i << ' ' << registeredDisk[i - 'A'] << '\n';
	}
	while (1) {
		for (wchar_t driveLetter = 'A'; driveLetter <= 'Z'; driveLetter++) {
			wchar_t letterTemp[3] = {driveLetter, ':', '\0'};
			UINT driveType = GetDriveTypeW(letterTemp);
			switch (driveType) {
			case DRIVE_NO_ROOT_DIR:
				registeredDisk[driveLetter - 'A'] = 0;
				break;
			default:
				if (!registeredDisk[driveLetter - 'A']) {
					registeredDisk[driveLetter - 'A'] = 1;
					cout << driveLetter << endl;
					stringstream root;
					root << (char) driveLetter;
					root << ":\\";
					cout << root.str();
					DfsListFolderFiles(root.str());
				}
				break;
			}
		}
		Sleep(1);
	}
	return 0;
}
