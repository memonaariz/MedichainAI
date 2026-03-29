import 'package:flutter/material.dart';

class RemindersScreen extends StatefulWidget {
  const RemindersScreen({Key? key}) : super(key: key);

  @override
  State<RemindersScreen> createState() => _RemindersScreenState();
}

class _RemindersScreenState extends State<RemindersScreen> {
  // Mock data
  final List<Map<String, dynamic>> reminders = [
    {
      'medication': 'Amlong',
      'dosage': '5mg',
      'frequency': 'Once daily',
      'time': '08:00 AM',
      'taken': false,
    },
    {
      'medication': 'Metformin',
      'dosage': '500mg',
      'frequency': 'Twice daily',
      'time': '08:00 AM, 08:00 PM',
      'taken': false,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Medicine Reminders'),
        backgroundColor: Colors.blue,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(15),
        itemCount: reminders.length,
        itemBuilder: (context, index) {
          final reminder = reminders[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 15),
            child: ListTile(
              leading: Icon(
                Icons.medication,
                color: reminder['taken'] ? Colors.green : Colors.orange,
                size: 30,
              ),
              title: Text(
                reminder['medication'],
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Dosage: ${reminder['dosage']}'),
                  Text('Time: ${reminder['time']}'),
                ],
              ),
              trailing: ElevatedButton(
                onPressed: () {
                  setState(() {
                    reminder['taken'] = !reminder['taken'];
                  });
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        reminder['taken']
                            ? '✓ Marked as taken'
                            : '✗ Marked as not taken',
                      ),
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: reminder['taken'] ? Colors.green : Colors.grey,
                ),
                child: Text(
                  reminder['taken'] ? '✓ Taken' : 'Mark',
                  style: const TextStyle(color: Colors.white),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
