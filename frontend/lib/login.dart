import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:soganglink/home.dart';

import 'homepage.dart';



class Login extends StatefulWidget{
  const Login({Key? key}) : super(key:key);
  @override
  _Login createState() => _Login();
}


class _Login extends State<Login>{
  final idcontroller = TextEditingController();
  final passwordcontroller = TextEditingController();


  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.only(top: 60.0),
            child: Center(
              child: Container(
                  width: 200,
                  height: 150,
                  /*decoration: BoxDecoration(
                        color: Colors.red,
                        borderRadius: BorderRadius.circular(50.0)),*/
                  child: Icon(Icons.logo_dev),
              ),
            ),
          ),
          Padding(
            //padding: const EdgeInsets.only(left:15.0,right: 15.0,top:0,bottom: 0),
            padding: EdgeInsets.symmetric(horizontal: 15),
            child: TextField(
              controller: idcontroller,
              decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'id',
                  hintText: 'Enter id'),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(
                left: 15.0, right: 15.0, top: 15, bottom: 0),
            //padding: EdgeInsets.symmetric(horizontal: 15),
            child: TextField(
              obscureText: true,
              controller: passwordcontroller,
              decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Password',
                  hintText: 'Enter secure password'),

            ),
          ),
          SizedBox(
            height: 200,
          ),
          Container(
            height: 50,
            width: 250,
            decoration: BoxDecoration(
                color: Colors.blue, borderRadius: BorderRadius.circular(20)),
            child: TextButton(
              onPressed: () {

                //id -> idcontroller.text
                //password -> passwordcontroller.text
                Navigator.pushAndRemoveUntil(context, MaterialPageRoute(builder: (BuildContext context) => Home()) , (route) => false);
              },
              child: Text(
                'Login',
                style: TextStyle(color: Colors.white, fontSize: 25),
              ),
            ),
          ),
        ],
      ),
    );
  }

}
