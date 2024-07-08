import 'package:flutter/material.dart';
import 'package:soganglink/login.dart';

class CalcGrade extends StatefulWidget {
  const CalcGrade({Key? key}) : super(key: key);
  @override
  _CalcGrade createState() => _CalcGrade();
}

class _CalcGrade extends State<CalcGrade> {
  TextEditingController subjectController = TextEditingController();
  TextEditingController gradeController = TextEditingController();
  TextEditingController creditController = TextEditingController();
  List<Map<String, dynamic>> subjects = [];

  void _addSubject() {
    setState(() {
      String subject = subjectController.text;
      String credit = creditController.text;
      String grade = gradeController.text;
      subjects.add({
        'subject': subject,
        'grade': grade,
        'credit': credit,
        'checked': true
      });
      subjectController.clear();
      gradeController.clear();
      creditController.clear();
    });
  }

  double _calculateGPA() {
    double totalGrade = 0;
    double totalCredit = 0;
    for (var subject in subjects) {
      if (subject['checked']) {
        if (_calculateGradePoint(subject['grade']) != 0) {
          totalGrade +=
              _calculateGradePoint(subject['grade']) * subject['credit'];
          totalCredit += subject['credit'];
        }
      }
    }
    return totalCredit != 0 ? totalGrade / totalCredit : 0.0;
  }

  double _calculateGradePoint(String grade) {
    switch (grade) {
      case 'A+':
        return 4.3;
      case 'A0':
        return 4.0;
      case 'A-':
        return 3.7;
      case 'B+':
        return 3.3;
      case 'B0':
        return 3.0;
      case 'B-':
        return 2.7;
      case 'C+':
        return 2.3;
      case 'C0':
        return 2.0;
      case 'C-':
        return 1.7;
      case 'D+':
        return 1.3;
      case 'D0':
        return 1.0;
      case 'F':
        return 0.0;
      default:
        return 0.0;
    }
  }

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    for (var lecture in takes.cousrses_takes) {
      setState(() {
        String subject = lecture.course.name;
        String? grade = lecture.final_grade;
        int credit = lecture.course.credit;
        subjects.add({
          'subject': subject,
          'grade': grade,
          'credit': credit,
          'checked': true
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('성적 계산기'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: subjectController,
              decoration: const InputDecoration(labelText: '과목명'),
            ),
            TextField(
              controller: gradeController,
              decoration: const InputDecoration(labelText: '성적'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: creditController,
              decoration: const InputDecoration(labelText: '학점'),
              keyboardType: TextInputType.number,
            ),
            ElevatedButton(
              onPressed: _addSubject,
              child: const Text('추가'),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView.builder(
                itemCount: subjects.length,
                itemBuilder: (context, index) {
                  return CheckboxListTile(
                    title: Text(
                        '${subjects[index]['subject']} - ${subjects[index]['grade']}'),
                    value: subjects[index]['checked'],
                    onChanged: (value) {
                      setState(() {
                        subjects[index]['checked'] = value!;
                      });
                    },
                  );
                },
              ),
            ),
            Text(
              '평균 학점: ${_calculateGPA().toStringAsFixed(2)}',
              style: const TextStyle(fontSize: 20),
            ),
          ],
        ),
      ),
    );
  }
}
