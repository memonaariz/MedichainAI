import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class NearbyHospitalsScreen extends StatefulWidget {
  const NearbyHospitalsScreen({Key? key}) : super(key: key);

  @override
  State<NearbyHospitalsScreen> createState() => _NearbyHospitalsScreenState();
}

class _NearbyHospitalsScreenState extends State<NearbyHospitalsScreen> {
  final List<Map<String, dynamic>> hospitals = [
    {
      'name': 'Apollo Hospitals',
      'type': 'Private',
      'distance': '2.5 km',
      'phone': '1860-500-1066',
      'address': 'Delhi, India',
      'emergency': true,
      'rating': 4.8,
    },
    {
      'name': 'Max Healthcare',
      'type': 'Private',
      'distance': '3.2 km',
      'phone': '1800-180-1000',
      'address': 'Delhi, India',
      'emergency': true,
      'rating': 4.7,
    },
    {
      'name': 'Government Medical College Hospital',
      'type': 'Government',
      'distance': '4.1 km',
      'phone': '011-2658-8500',
      'address': 'Delhi, India',
      'emergency': true,
      'rating': 4.2,
    },
  ];

  void _callHospital(String phone) async {
    final url = 'tel:$phone';
    if (await canLaunchUrl(Uri.parse(url))) {
      await launchUrl(Uri.parse(url));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Nearby Hospitals'),
        backgroundColor: Colors.blue,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(15),
        itemCount: hospitals.length,
        itemBuilder: (context, index) {
          final hospital = hospitals[index];
          return Card(
            margin: const EdgeInsets.only(bottom: 15),
            child: Padding(
              padding: const EdgeInsets.all(15),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              hospital['name'],
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 5),
                            Text(
                              hospital['type'],
                              style: const TextStyle(color: Colors.grey, fontSize: 12),
                            ),
                          ],
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: Colors.yellow.shade100,
                          borderRadius: BorderRadius.circular(5),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.star, size: 16, color: Colors.orange),
                            const SizedBox(width: 5),
                            Text('${hospital['rating']}'),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      const Icon(Icons.location_on, size: 16, color: Colors.grey),
                      const SizedBox(width: 5),
                      Text('${hospital['distance']} away'),
                    ],
                  ),
                  const SizedBox(height: 5),
                  Row(
                    children: [
                      const Icon(Icons.phone, size: 16, color: Colors.grey),
                      const SizedBox(width: 5),
                      Text(hospital['phone']),
                    ],
                  ),
                  const SizedBox(height: 10),
                  if (hospital['emergency'])
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.red.shade100,
                        borderRadius: BorderRadius.circular(5),
                      ),
                      child: const Text(
                        '🚨 Emergency Available',
                        style: TextStyle(fontSize: 12, color: Colors.red),
                      ),
                    ),
                  const SizedBox(height: 10),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () => _callHospital(hospital['phone']),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                      child: const Text(
                        'Call Now',
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
