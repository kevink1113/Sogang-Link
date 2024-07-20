import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:soganglink/login.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Sogang Link",
      theme: ThemeData(
          useMaterial3: true,
          fontFamily: GoogleFonts.notoSansKr().fontFamily,
          // fontFamily: GoogleFonts.ibmPlexSans().fontFamily,
          // Define the default brightness and colors.
          scaffoldBackgroundColor: const Color(0xFFf5f5f5),
          dialogBackgroundColor: const Color(0xFFf5f5f5),
          cardColor: Colors.white,
          // scaffoldBackgroundColor: Colors.grey.shade200,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF9e2a2f),
            // brightness: Brightness.dark,
            // seedColor: Colors.white,
            // TRY THIS: Change to "Brightness.light"
            //           and see that all colors change
            //           to better contrast a light background.
            // brightness: Brightness.dark,
          ),
          textTheme: const TextTheme(
            titleLarge: TextStyle(
              // color: Colors.black,
              fontSize: 18,
              fontWeight: FontWeight.w600,
              // letterSpacing: 2.0,
            ),
            // bodyMedium: GoogleFonts.notoSansKr(),
          )
          // Define the default `TextTheme`. Use this to specify the default
          // text styling for headlines, titles, bodies of text, and more.
          // textTheme: TextTheme(
          //   displayLarge: const TextStyle(
          //     fontSize: 72,
          //     fontWeight: FontWeight.bold,
          //   ),
          //   // TRY THIS: Change one of the GoogleFonts
          //   //           to "lato", "poppins", or "lora".
          //   //           The title uses "titleLarge"
          //   //           and the middle text uses "bodyMedium".
          //   titleLarge: GoogleFonts.oswald(
          //     fontSize: 30,
          //     fontStyle: FontStyle.italic,
          //   ),
          //   bodyMedium: GoogleFonts.notoSansKr(
          //     fontSize: 16,
          //     fontWeight: FontWeight.w500,
          //   ),
          //   displaySmall: GoogleFonts.pacifico(),
          // ),
          ),
      home: const Login(),
    );
  }
}
