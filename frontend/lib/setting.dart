import 'package:flutter/material.dart';
import 'package:soganglink/login.dart';
import 'package:soganglink/storage.dart';
import 'package:settings_ui/settings_ui.dart';

var info = false;

class Setting extends StatefulWidget {
  const Setting({Key? key}) : super(key: key);
  @override
  _Setting createState() => _Setting();
}

class _Setting extends State<Setting> {
  List<Widget> courses = [];
  int semester = 2024010;
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    void initState() {
      // TODO: implement initState
      super.initState();
    }

    // TODO: implement build
    return SettingsList(
      sections: [
        SettingsSection(
          title: const Text(
            '공통',
          ),
          tiles: <SettingsTile>[
            SettingsTile.switchTile(
              title: const Text('개인정보동의'),
              initialValue: info,
              onToggle: (value) {
                setState(() {
                  info = !info;
                });
              },
              leading: const Icon(Icons.vibration),
            ),
          ],
        ),
        SettingsSection(
          title: const Text('계정'),
          tiles: <SettingsTile>[
            SettingsTile.navigation(
              leading: const Icon(Icons.logout),
              title: const Text('로그아웃'),
              onPressed: ((context) {
                SecureStorage.deleteToken();
                Navigator.pushReplacement(
                    context, MaterialPageRoute(builder: (_) => const Login()));
              }),
            ),
          ],
        )
      ],
    );
  }
}
