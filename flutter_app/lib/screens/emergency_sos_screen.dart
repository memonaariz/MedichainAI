import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

class EmergencySosScreen extends StatefulWidget {
  const EmergencySosScreen({Key? key}) : super(key: key);

  @override
  State<EmergencySosScreen> createState() => _EmergencySosScreenState();
}

class _EmergencySosScreenState extends State<EmergencySosScreen> {
  String? _location;
  bool _isLoading = false;

  Future<void> _getLocation() async {
    try {
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        _location = '${position.latitude}, ${position.longitude}';
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not get location')),
      );
    }
  }

  void _triggerSOS() async {
    setState(() => _isLoading = true);

    await _getLocation();

    // Simulate SOS trigger
    await Future.delayed(const Duration(seconds: 2));

    setState(() => _isLoading = false);

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('🚨 SOS Alert sent to family members!'),
        backgroundColor: Colors.red,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Emergency SOS'),
        backgroundColor: Colors.red,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.emergency, size: 80, color: Colors.red),
            const SizedBox(height: 20),
            const Text(
              'Emergency Alert',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            const Text(
              'Press the button below to send SOS alert',
              style: TextStyle(fontSize: 14, color: Colors.grey),
            ),
            const SizedBox(height: 40),
            if (_location != null)
              Container(
                padding: const EdgeInsets.all(15),
                decoration: BoxDecoration(
                  color: Colors.blue.shade50,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Column(
                  children: [
                    const Text('📍 Location:'),
                    Text(_location!),
                  ],
                ),
              ),
            const SizedBox(height: 40),
            GestureDetector(
              onTap: _isLoading ? null : _triggerSOS,
              child: Container(
                width: 150,
                height: 150,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.red,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.red.withOpacity(0.5),
                      blurRadius: 20,
                      spreadRadius: 5,
                    ),
                  ],
                ),
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Icon(
                        Icons.emergency,
                        size: 60,
                        color: Colors.white,
                      ),
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'Tap the red button to send SOS',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
