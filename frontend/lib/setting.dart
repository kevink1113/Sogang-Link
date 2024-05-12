import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:soganglink/data/courses/takes.dart';
import 'package:soganglink/data/login/User.dart';
import 'package:soganglink/login.dart';
import 'package:soganglink/storage.dart';
import 'package:wakelock/wakelock.dart';
import 'package:screen_brightness/screen_brightness.dart';
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
          title: Text(
            '공통',
          ),
          tiles: <SettingsTile>[
            SettingsTile.switchTile(
              title: Text('개인정보동의'),
              initialValue: info,
              onToggle: (value) {
                setState(() {
                  info = !info;
                });
              },
              leading: Icon(Icons.vibration),
            ),
          ],
        ),
        SettingsSection(
          title: Text('계정'),
          tiles: <SettingsTile>[
            SettingsTile.navigation(
              leading: Icon(Icons.logout),
              title: Text('로그아웃'),
              onPressed: ((context) {
                SecureStorage.deleteToken();
                Navigator.pushReplacement(
                    context, MaterialPageRoute(builder: (_) => Login()));
              }),
            ),
          ],
        )
      ],
    );
  }
}
